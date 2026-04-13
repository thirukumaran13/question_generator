#!/usr/bin/env python3
"""Validate all question JSON files for the question_generator project."""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("ERROR: 'jsonschema' package is not installed. Run: pip install jsonschema")
    sys.exit(1)

QUESTIONS_DIR = Path(__file__).parent / "questions"
MANIFEST_FILE = QUESTIONS_DIR / "manifest.json"
MANIFEST_SCHEMA_FILE = QUESTIONS_DIR / "manifest-schema.json"
QUESTION_SCHEMA_FILE = QUESTIONS_DIR / "question-schema.json"

SKIP_FILES = {"manifest.json", "manifest-schema.json", "question-schema.json"}


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def count_questions(data: list) -> int:
    total = 0
    for item in data:
        if "context" in item and "questions" in item:
            total += len(item["questions"])
        else:
            total += 1
    return total


def schema_errors(data: object, schema: dict) -> list[str]:
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        location = " -> ".join(str(p) for p in error.absolute_path) or "root"
        errors.append(f"  [{location}] {error.message}")
    return errors


def main() -> int:
    manifest_schema = load_json(MANIFEST_SCHEMA_FILE)
    question_schema = load_json(QUESTION_SCHEMA_FILE)

    failed = 0
    passed = 0

    # --- Validate manifest ---
    print(f"Validating {MANIFEST_FILE.name} ...")
    try:
        manifest = load_json(MANIFEST_FILE)
    except json.JSONDecodeError as e:
        print(f"  FAIL: manifest.json is not valid JSON: {e}")
        return 1

    errors = schema_errors(manifest, manifest_schema)
    if errors:
        print(f"  FAIL: manifest.json")
        for e in errors:
            print(e)
        failed += 1
    else:
        print(f"  PASS: manifest.json")
        passed += 1

    # --- Validate each question file referenced in manifest ---
    referenced: set[Path] = set()
    for entry in manifest.get("entries", []):
        folder = entry.get("folder", "")
        for filename in entry.get("files", []):
            filepath = QUESTIONS_DIR / folder / filename
            referenced.add(filepath.resolve())

            print(f"Validating {folder}/{filename} ...")
            if not filepath.exists():
                print(f"  FAIL: file not found: {filepath}")
                failed += 1
                continue
            try:
                data = load_json(filepath)
            except json.JSONDecodeError as e:
                print(f"  FAIL: not valid JSON: {e}")
                failed += 1
                continue

            errors = schema_errors(data, question_schema)
            if errors:
                print(f"  FAIL: {folder}/{filename}")
                for e in errors:
                    print(e)
                failed += 1
            else:
                print(f"  PASS: {folder}/{filename} ({count_questions(data)} questions)")
                passed += 1

    # --- Warn about JSON files on disk not referenced in manifest ---
    for json_file in QUESTIONS_DIR.rglob("*.json"):
        if json_file.name in SKIP_FILES:
            continue
        if json_file.resolve() not in referenced:
            print(
                f"  WARNING: '{json_file.relative_to(QUESTIONS_DIR)}' exists on disk "
                "but is not listed in manifest.json"
            )

    print()
    print(f"Results: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
