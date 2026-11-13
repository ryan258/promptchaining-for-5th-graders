# artifact_store.py - Persistent knowledge accumulation for prompt chains
# Every chain step can save artifacts that future chains can reuse

import json
import os
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import re
import hashlib
import logging
import tempfile
from threading import RLock
import unicodedata

logger = logging.getLogger(__name__)
MAX_ARTIFACT_BYTES = 10_000_000

try:
    import chromadb
except ImportError:
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
        self._write_lock = RLock()
        self.load_warnings: List[str] = []

        # Create base directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)

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

        # Build metadata
        artifact_metadata = {
            "created_at": datetime.now().isoformat(),
            "topic": topic,
            "step_name": step_name,
            **(metadata or {})
        }
        # Publish the primary file before changing the cache. A serialization or
        # disk failure must not advertise an answer that was never saved.
        with self._write_lock:
            self._save_to_disk(topic_key, step_name, data, artifact_metadata)
            self.artifacts[artifact_key] = data
            self.metadata[artifact_key] = artifact_metadata
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
        return self.get_by_key(artifact_key)

    def get_by_key(self, artifact_key: str) -> Optional[Any]:
        """
        Retrieve an artifact by its full key.

        Args:
            artifact_key: Full key like "machine_learning:components"

        Returns:
            The artifact data, or None if not found
        """
        with self._write_lock:
            if artifact_key not in self.artifacts:
                return None
            topic, _, step = artifact_key.partition(":")
            topic_path = os.path.join(self.base_dir, topic)
            path = os.path.join(topic_path, f"{step}.json")
            if os.path.islink(topic_path) or os.path.islink(path) or not os.path.isfile(path):
                self.artifacts.pop(artifact_key, None)
                self.metadata.pop(artifact_key, None)
                return None
            return self.artifacts[artifact_key]

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
        with self._write_lock:
            for key in tuple(self.artifacts):
                if regex.match(key):
                    value = self.get_by_key(key)
                    if key in self.artifacts:
                        matching[key] = value

        return matching

    def list_topics(self) -> List[str]:
        """
        Get all topics that have artifacts.

        Returns:
            List of topic names
        """
        topics = set()
        for key in self.query("*:*"):
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
        for key in self.query(f"{topic_key}:*"):
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
        self.get_by_key(artifact_key)
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
                for key, value in self.query("*:*").items()
            }
        }

    def _normalize_key(self, key: str) -> str:
        """
        Convert a topic to a safe, normalized key.

        "Machine Learning" → "machine_learning"
        "Quantum Physics!" → "quantum_physics"
        """
        # Lowercase, replace spaces with underscores, remove special chars
        key = unicodedata.normalize("NFC", key).lower()
        normalized = re.sub(r'[^a-z0-9]+', '_', key).strip('_')
        if not normalized or len(normalized) > 255:
            digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
            normalized = f"{normalized[:160] or 'topic'}_{digest}"
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
        if not isinstance(step_name, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,120}", step_name):
            raise ValueError("Use a short artifact step name containing letters, numbers, underscores or hyphens.")
        # Serialize both values before touching an existing saved file.
        data_text = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)
        metadata = {**metadata, "content_sha256": hashlib.sha256(data_text.encode("utf-8")).hexdigest()}
        meta_text = json.dumps(metadata, indent=2, ensure_ascii=False, allow_nan=False)
        if max(len(data_text.encode("utf-8")), len(meta_text.encode("utf-8"))) > MAX_ARTIFACT_BYTES:
            raise ValueError("Artifact data or metadata exceeds the supported size.")
        topic_dir = os.path.join(self.base_dir, topic_key)
        if os.path.islink(topic_dir):
            raise ValueError("An artifact topic cannot be a symbolic link.")
        os.makedirs(topic_dir, exist_ok=True)

        # Save data
        data_path = os.path.join(topic_dir, f"{step_name}.json")
        _atomic_replace(data_path, data_text)

        # Save metadata
        meta_path = os.path.join(topic_dir, f"{step_name}.meta.json")
        try:
            _atomic_replace(meta_path, meta_text)
        except OSError:
            # The answer is already durable. A stale sidecar is ignored on load
            # using its digest; it must not turn a saved answer into a failed run.
            logger.warning("Artifact saved; metadata sidecar could not be updated")

    def _load_all(self):
        """
        Load all artifacts from disk into memory.
        """
        if not os.path.exists(self.base_dir):
            return

        # Iterate through topic directories
        for topic_dir_name in os.listdir(self.base_dir):
            topic_path = os.path.join(self.base_dir, topic_dir_name)

            if not os.path.isdir(topic_path) or topic_dir_name.startswith((".", "_")) or os.path.islink(topic_path):
                continue

            # Load all .json files (except .meta.json)
            try:
                filenames = os.listdir(topic_path)
            except OSError:
                self.load_warnings.append(topic_dir_name)
                continue
            for filename in filenames:
                if filename.endswith(".meta.json") or filename.startswith("."):
                    continue

                if filename.endswith(".json"):
                    step_name = filename[:-5]  # Remove .json

                    # Load data
                    data_path = os.path.join(topic_path, filename)
                    try:
                        raw = _read_artifact_text(data_path)
                        data = json.loads(raw)
                    except (OSError, ValueError, RecursionError):
                        self.load_warnings.append(f"{topic_dir_name}/{filename}")
                        logger.warning("Skipped an unreadable artifact; original file preserved")
                        continue

                    # Load metadata if exists
                    meta_path = os.path.join(topic_path, f"{step_name}.meta.json")
                    metadata = {}
                    if os.path.exists(meta_path):
                        try:
                            metadata = json.loads(_read_artifact_text(meta_path))
                            if (not isinstance(metadata, dict)
                                    or (metadata.get("content_sha256") and metadata["content_sha256"] != hashlib.sha256(raw.encode("utf-8")).hexdigest())
                                    or (not metadata.get("content_sha256") and os.stat(meta_path).st_mtime_ns < os.stat(data_path).st_mtime_ns)):
                                metadata = {}
                        except (OSError, ValueError, RecursionError):
                            metadata = {}

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
            if os.path.islink(chroma_dir):
                return
            os.makedirs(chroma_dir, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(
                path=chroma_dir,
                settings=chromadb.config.Settings(anonymized_telemetry=False),
            )
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name="artifacts", embedding_function=None,
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


def _read_artifact_text(path: str) -> str:
    if os.path.islink(path) or not os.path.isfile(path):
        raise ValueError("Expected a regular artifact file.")
    with open(path, "rb") as stream:
        data = stream.read(MAX_ARTIFACT_BYTES + 1)
    if len(data) > MAX_ARTIFACT_BYTES:
        raise ValueError("Artifact file exceeds the supported size.")
    return data.decode("utf-8")


def remove_artifact_mirror(base_dir: str, topic: str, step: str) -> bool:
    """Remove an artifact from an existing Chroma mirror after its JSON is removed."""
    chroma_dir = os.path.join(base_dir, "_chroma")
    if not os.path.exists(chroma_dir):
        return True
    if chromadb is None or os.path.islink(chroma_dir):
        return False
    try:
        client = chromadb.PersistentClient(path=chroma_dir,
                                          settings=chromadb.config.Settings(anonymized_telemetry=False))
        client.get_or_create_collection(name="artifacts", embedding_function=None).delete(ids=[f"{topic}:{step}"])
    except Exception:
        logger.warning("Artifact JSON removed; Chroma mirror could not be updated")
        return False
    return True


def _atomic_replace(path: str, text: str) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".artifact-", dir=os.path.dirname(path))
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


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
