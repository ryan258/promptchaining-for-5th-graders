# artifact_store.py - Persistent knowledge accumulation for prompt chains
# Every chain step can save artifacts that future chains can reuse

import json
import os
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import re
import hashlib

try:
    import chromadb
except Exception:
    chromadb = None


class ArtifactStore:
    """
    A knowledge store where chain outputs become reusable artifacts.

    Think of this like a library where each book (artifact) has a specific
    location (topic:step_name) so you can find it later.

    Example:
        After running concept_simplifier("Machine Learning"):
        - artifacts["machine_learning:components"] = {...}
        - artifacts["machine_learning:analogies"] = {...}

        Later chains can reference: {{artifact:machine_learning:components}}
    """

    def __init__(self, base_dir: str = "artifacts"):
        """
        Create or load an artifact store.

        Args:
            base_dir: Where to save artifacts on disk
        """
        self.base_dir = base_dir
        self.artifacts: Dict[str, Any] = {}  # In-memory cache
        self.metadata: Dict[str, Dict] = {}  # When created, by what tool, etc.
        self.chroma_client = None
        self.chroma_collection = None

        # Create base directory if it doesn't exist
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Load existing artifacts
        self._load_all()

        # Optional Chroma mirror for local vector-backed retrieval.
        # JSON files remain source-of-truth persistence.
        self._init_chroma()

    def save(self, topic: str, step_name: str, data: Any, metadata: Optional[Dict] = None):
        """
        Save an artifact with a semantic key.

        Args:
            topic: The subject (e.g., "machine_learning", "quantum_physics")
            step_name: The step that produced this (e.g., "components", "analogies")
            data: The actual artifact data (dict, list, string, etc.)
            metadata: Optional info (which tool created it, timestamp, etc.)
        """
        # Normalize the topic to a safe filename
        topic_key = self._normalize_key(topic)

        # Create the full artifact key
        artifact_key = f"{topic_key}:{step_name}"

        # Store in memory
        self.artifacts[artifact_key] = data

        # Build metadata
        artifact_metadata = {
            "created_at": datetime.now().isoformat(),
            "topic": topic,
            "step_name": step_name,
            **(metadata or {})
        }
        self.metadata[artifact_key] = artifact_metadata

        # Persist to disk
        self._save_to_disk(topic_key, step_name, data, artifact_metadata)
        self._sync_to_chroma(artifact_key, data, artifact_metadata)

    def get(self, topic: str, step_name: str) -> Optional[Any]:
        """
        Retrieve an artifact.

        Args:
            topic: The subject
            step_name: The step name

        Returns:
            The artifact data, or None if not found
        """
        topic_key = self._normalize_key(topic)
        artifact_key = f"{topic_key}:{step_name}"
        return self.artifacts.get(artifact_key)

    def get_by_key(self, artifact_key: str) -> Optional[Any]:
        """
        Retrieve an artifact by its full key.

        Args:
            artifact_key: Full key like "machine_learning:components"

        Returns:
            The artifact data, or None if not found
        """
        return self.artifacts.get(artifact_key)

    def query(self, pattern: str) -> Dict[str, Any]:
        """
        Find artifacts matching a pattern.

        Examples:
            query("machine_learning:*") → all artifacts for machine learning
            query("*:components") → all components across topics
            query("*:*") → everything

        Args:
            pattern: Search pattern with * as wildcard

        Returns:
            Dict of matching artifacts {key: data}
        """
        # Convert wildcard pattern to regex safely
        # Example: "*:components" -> "^.*:components$"
        regex_pattern = re.escape(pattern).replace(r"\*", ".*")
        regex = re.compile(f"^{regex_pattern}$")

        matching = {}
        for key, value in self.artifacts.items():
            if regex.match(key):
                matching[key] = value

        return matching

    def list_topics(self) -> List[str]:
        """
        Get all topics that have artifacts.

        Returns:
            List of topic names
        """
        topics = set()
        for key in self.artifacts.keys():
            topic = key.split(":")[0]
            topics.add(topic)
        return sorted(list(topics))

    def list_steps_for_topic(self, topic: str) -> List[str]:
        """
        Get all step names for a specific topic.

        Args:
            topic: The topic to query

        Returns:
            List of step names
        """
        topic_key = self._normalize_key(topic)
        steps = []
        for key in self.artifacts.keys():
            if key.startswith(f"{topic_key}:"):
                step_name = key.split(":", 1)[1]
                steps.append(step_name)
        return sorted(steps)

    def get_metadata(self, topic: str, step_name: str) -> Optional[Dict]:
        """
        Get metadata about an artifact.

        Args:
            topic: The subject
            step_name: The step name

        Returns:
            Metadata dict or None
        """
        topic_key = self._normalize_key(topic)
        artifact_key = f"{topic_key}:{step_name}"
        return self.metadata.get(artifact_key)

    def visualize(self) -> str:
        """
        Create a text visualization of the artifact graph.

        Returns:
            Pretty-printed tree of all artifacts
        """
        output = "📚 Artifact Store\n\n"

        topics = self.list_topics()
        if not topics:
            return output + "  (empty)\n"

        for topic in topics:
            output += f"📖 {topic}\n"
            steps = self.list_steps_for_topic(topic)
            for step in steps:
                artifact_key = f"{topic}:{step}"
                metadata = self.metadata.get(artifact_key, {})
                created = metadata.get("created_at", "unknown")
                output += f"  └─ {step} (created: {created[:19]})\n"
            output += "\n"

        return output

    def export_for_web(self) -> Dict[str, Any]:
        """
        Export artifact store in a format suitable for web UI.

        Returns:
            Dict with topics, artifacts, and metadata
        """
        return {
            "topics": self.list_topics(),
            "artifacts": {
                key: {
                    "data": value,
                    "metadata": self.metadata.get(key, {})
                }
                for key, value in self.artifacts.items()
            }
        }

    def _normalize_key(self, key: str) -> str:
        """
        Convert a topic to a safe, normalized key.

        "Machine Learning" → "machine_learning"
        "Quantum Physics!" → "quantum_physics"
        """
        # Lowercase, replace spaces with underscores, remove special chars
        normalized = key.lower()
        normalized = re.sub(r'[^a-z0-9]+', '_', normalized)
        normalized = normalized.strip('_')
        return normalized

    def _save_to_disk(self, topic_key: str, step_name: str, data: Any, metadata: Dict):
        """
        Persist an artifact to disk.

        Structure:
            artifacts/
              topic_name/
                step_name.json
                step_name.meta.json
        """
        # Create topic directory
        topic_dir = os.path.join(self.base_dir, topic_key)
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)

        # Save data
        data_path = os.path.join(topic_dir, f"{step_name}.json")
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Save metadata
        meta_path = os.path.join(topic_dir, f"{step_name}.meta.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def _load_all(self):
        """
        Load all artifacts from disk into memory.
        """
        if not os.path.exists(self.base_dir):
            return

        # Iterate through topic directories
        for topic_dir_name in os.listdir(self.base_dir):
            topic_path = os.path.join(self.base_dir, topic_dir_name)

            if not os.path.isdir(topic_path):
                continue

            # Load all .json files (except .meta.json)
            for filename in os.listdir(topic_path):
                if filename.endswith(".meta.json"):
                    continue

                if filename.endswith(".json"):
                    step_name = filename[:-5]  # Remove .json

                    # Load data
                    data_path = os.path.join(topic_path, filename)
                    with open(data_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Load metadata if exists
                    meta_path = os.path.join(topic_path, f"{step_name}.meta.json")
                    metadata = {}
                    if os.path.exists(meta_path):
                        with open(meta_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)

                    # Store in memory
                    artifact_key = f"{topic_dir_name}:{step_name}"
                    self.artifacts[artifact_key] = data
                    self.metadata[artifact_key] = metadata

    def _init_chroma(self):
        """Initialize a local Chroma collection if chromadb is available."""
        if chromadb is None:
            return

        try:
            chroma_dir = os.path.join(self.base_dir, "_chroma")
            os.makedirs(chroma_dir, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name="artifacts"
            )
        except Exception:
            # Chroma is optional; keep JSON artifact flow working even if unavailable.
            self.chroma_client = None
            self.chroma_collection = None

    @staticmethod
    def _cheap_embedding(text: str, dim: int = 16) -> List[float]:
        """
        Build a tiny deterministic embedding vector without external model downloads.
        This keeps Chroma local-first and dependency-light for this project.
        """
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = []
        for i in range(dim):
            byte = digest[i % len(digest)]
            values.append(byte / 255.0)
        return values

    def _sync_to_chroma(self, artifact_key: str, data: Any, metadata: Dict[str, Any]):
        """Mirror a saved artifact into Chroma for optional semantic retrieval."""
        if self.chroma_collection is None:
            return

        try:
            document = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
            chroma_meta = {
                "topic": str(metadata.get("topic", "")),
                "step_name": str(metadata.get("step_name", "")),
                "created_at": str(metadata.get("created_at", "")),
            }
            embedding = self._cheap_embedding(document)
            self.chroma_collection.upsert(
                ids=[artifact_key],
                documents=[document],
                metadatas=[chroma_meta],
                embeddings=[embedding],
            )
        except Exception:
            # Never let Chroma mirroring break primary artifact persistence.
            return


def resolve_artifact_references(prompt: str, artifact_store: ArtifactStore) -> Tuple[str, List[str]]:
    """
    Replace {{artifact:topic:step}} references in a prompt with actual artifact data.

    Examples:
        "Compare {{artifact:machine_learning:components}}"
        → "Compare {'name': 'Pattern Recognition', ...}"

    Args:
        prompt: The prompt with potential artifact references
        artifact_store: The artifact store to query

    Returns:
        Tuple of (resolved_prompt, list_of_artifact_keys_used)
    """
    used_artifacts = []

    # Find all {{artifact:topic:step}} patterns
    pattern = r'\{\{artifact:([^:}]+):([^}]+)\}\}'

    def replace_artifact(match):
        topic = match.group(1)
        step_name = match.group(2)

        # Support wildcard lookups like {{artifact:*:step_1}} by expanding
        # to a JSON object of all matching artifacts.
        if "*" in topic or "*" in step_name:
            topic_pattern = topic if "*" in topic else artifact_store._normalize_key(topic)
            artifact_query = f"{topic_pattern}:{step_name}"
            matching = artifact_store.query(artifact_query)
            if not matching:
                return f"{{{{artifact:{topic}:{step_name} [NOT FOUND]}}}}"

            used_artifacts.extend(sorted(matching.keys()))
            return json.dumps(matching)

        artifact = artifact_store.get(topic, step_name)

        if artifact is None:
            # Artifact not found - leave placeholder and warn
            return f"{{{{artifact:{topic}:{step_name} [NOT FOUND]}}}}"

        # Track usage
        topic_key = artifact_store._normalize_key(topic)
        artifact_key = f"{topic_key}:{step_name}"
        used_artifacts.append(artifact_key)

        # Convert artifact to string
        if isinstance(artifact, (dict, list)):
            return json.dumps(artifact)
        else:
            return str(artifact)

    resolved_prompt = re.sub(pattern, replace_artifact, prompt)

    return resolved_prompt, used_artifacts
