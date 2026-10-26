"""Bounded, additive backups. Archives contain validated, independently usable JSON parts."""

import hashlib
from io import BytesIO
import json
import zipfile
import zlib

from .models import Backup

JSON_LIMIT = 10_000_000
ARCHIVE_LIMIT = 128_000_000
EXPANDED_LIMIT = 256_000_000
PART_LIMIT = 128


def archive_backup(recipes, runs) -> bytes:
    parts = []
    current = [[], []]
    size = 0
    for kind, records in enumerate((recipes, runs)):
        for record in records:
            record_size = len(record.model_dump_json().encode("utf-8")) + 2
            if size + record_size > 8_000_000 or len(current[kind]) == 2000:
                parts.append(Backup(recipes=current[0], runs=current[1]).model_dump_json().encode("utf-8"))
                current, size = [[], []], 0
            current[kind].append(record)
            size += record_size
    if any(current) or not parts:
        parts.append(Backup(recipes=current[0], runs=current[1]).model_dump_json().encode("utf-8"))
    if len(parts) > PART_LIMIT or sum(map(len, parts)) > EXPANDED_LIMIT or any(len(p) > JSON_LIMIT for p in parts):
        raise ValueError("This workspace exceeds the archive limits. Preserve a stopped workspace-folder copy instead.")
    manifest = {"format": "prompt-chaining-studio-archive", "version": 1,
                "parts": [{"name": f"part-{i:04d}.json", "sha256": hashlib.sha256(part).hexdigest()}
                          for i, part in enumerate(parts, 1)]}
    stream = BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest))
        for entry, part in zip(manifest["parts"], parts):
            archive.writestr(entry["name"], part)
    raw = stream.getvalue()
    if len(raw) > ARCHIVE_LIMIT:
        raise ValueError("This workspace exceeds the archive limits. Preserve a stopped workspace-folder copy instead.")
    return raw


def read_backup(raw: bytes) -> tuple[list, list]:
    if not raw.startswith(b"PK"):
        if len(raw) > JSON_LIMIT:
            raise ValueError("Choose a Studio JSON backup smaller than 10 MB, or a Studio ZIP archive.")
        backup = Backup.model_validate_json(raw)
        return backup.recipes, backup.runs
    if len(raw) > ARCHIVE_LIMIT:
        raise ValueError("Choose a Studio archive smaller than 128 MB.")
    try:
        with zipfile.ZipFile(BytesIO(raw)) as archive:
            infos = archive.infolist()
            if (len(infos) > PART_LIMIT + 1 or len({i.filename for i in infos}) != len(infos)
                    or sum(i.file_size for i in infos) > EXPANDED_LIMIT
                    or any(i.file_size > JSON_LIMIT or i.flag_bits & 1 for i in infos)):
                raise ValueError()
            with archive.open("manifest.json") as source:
                manifest_raw = source.read(20_001)
            if len(manifest_raw) > 20_000:
                raise ValueError()
            manifest = json.loads(manifest_raw)
            if (set(manifest) != {"format", "version", "parts"}
                    or manifest["format"] != "prompt-chaining-studio-archive" or manifest["version"] != 1
                    or not isinstance(manifest["parts"], list) or not 1 <= len(manifest["parts"]) <= PART_LIMIT):
                raise ValueError()
            recipes, runs = [], []
            names = {"manifest.json"}
            for index, entry in enumerate(manifest["parts"], 1):
                name = f"part-{index:04d}.json"
                if not isinstance(entry, dict) or set(entry) != {"name", "sha256"} or entry["name"] != name:
                    raise ValueError()
                names.add(name)
                with archive.open(name) as source:
                    part = source.read(JSON_LIMIT + 1)
                if len(part) > JSON_LIMIT or hashlib.sha256(part).hexdigest() != entry["sha256"]:
                    raise ValueError()
                backup = Backup.model_validate_json(part)
                recipes.extend(backup.recipes)
                runs.extend(backup.runs)
            if names != {i.filename for i in infos}:
                raise ValueError()
        return recipes, runs
    except (ValueError, KeyError, TypeError, RuntimeError, OSError, EOFError, zlib.error, zipfile.BadZipFile, NotImplementedError):
        raise ValueError("Invalid Studio archive. No records were imported.") from None
