#!/usr/bin/env python3
"""Generate the searchable site catalog from vocabulary/INDEX.md."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "vocabulary" / "INDEX.md"
OUTPUT = ROOT / "site" / "data" / "vocabulary.json"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]*)?\)")


def table_cells(line: str) -> list[str]:
    """Split a Markdown table row, respecting escaped pipes."""
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def field(text: str, name: str) -> str:
    match = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.*?)\s*$", text, re.M)
    return match.group(1).strip() if match else ""


def field_block(text: str, name: str) -> str:
    match = re.search(
        rf"(?ms)^\*\*{re.escape(name)}:\*\*\s*(.*?)(?=^\*\*[A-Za-z /]+:\*\*|^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def metadata(text: str) -> dict[str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        raise ValueError("missing YAML metadata block")
    return dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", match.group(1), re.M))


def parse_forms(text: str) -> list[dict[str, str]]:
    forms: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| Form / feature"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            if forms:
                break
            continue
        cells = table_cells(line)
        if len(cells) != 4 or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        forms.append({"label": cells[0], "value": cells[1], "example": cells[2], "translation": cells[3]})
    return forms


def parse_sources(text: str) -> list[dict[str, str]]:
    block = field_block(text, "Sources")
    sources: list[dict[str, str]] = []
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", line)
        if link:
            sources.append({"label": link.group(1), "url": link.group(2)})
        else:
            sources.append({"label": line, "url": ""})
    return sources


def parse_entry(relative_path: str, index_english: str, index_type: str, topics: list[str]) -> dict[str, object]:
    # Index links use POSIX separators even when the generator runs on Windows.
    vocabulary_root = ROOT / "vocabulary"
    path = (vocabulary_root / Path(*PurePosixPath(relative_path).parts)).resolve()
    if vocabulary_root.resolve() not in path.parents or not path.is_file():
        raise ValueError(f"index link does not resolve to a vocabulary file: {relative_path}")
    text = path.read_text(encoding="utf-8")
    meta = metadata(text)
    lemma = meta.get("lemma", "").strip()
    word_type = meta.get("word_type", "").strip()
    sense = meta.get("sense", "").strip()
    checked_on = meta.get("checked_on", "").strip()
    entry_id = meta.get("id", "").strip()
    english = field(text, "English")
    if not all((entry_id, lemma, word_type, sense, checked_on, english, index_english, index_type)):
        raise ValueError("entry or index row is missing required metadata or English meaning")

    return {
        "id": entry_id,
        "path": relative_path,
        "lemma": lemma,
        "word_type": word_type,
        "index_type": index_type,
        "sense": sense,
        "checked_on": checked_on,
        "english": english,
        "index_english": index_english,
        "topics": topics,
        "form_status": field(text, "Form status"),
        "notes": field_block(text, "Notes"),
        "sources": parse_sources(text),
        "forms": parse_forms(text),
    }


def main() -> int:
    issues: list[str] = []
    entries: list[dict[str, object]] = []
    indexed: dict[str, dict[str, object]] = {}
    for line_number, line in enumerate(INDEX.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = table_cells(line)
        if len(cells) != 4:
            continue
        link = LINK_RE.search(cells[0])
        if not link:
            continue
        relative = link.group(1).split("#", 1)[0]
        index_type = cells[1].strip()
        index_english = cells[2].strip()
        index_topics = [topic.strip() for topic in cells[3].split(";") if topic.strip()]
        current = indexed.get(relative)
        if current is None:
            indexed[relative] = {
                "english": index_english,
                "type": index_type,
                "topics": index_topics,
            }
        else:
            if current["english"] != index_english or current["type"] != index_type:
                issues.append(f"vocabulary/INDEX.md:{line_number}: conflicting index data for {relative}")
            current_topics = current["topics"]
            assert isinstance(current_topics, list)
            for topic in index_topics:
                if topic not in current_topics:
                    current_topics.append(topic)

    for relative, index_row in indexed.items():
        try:
            entries.append(parse_entry(
                relative,
                str(index_row["english"]),
                str(index_row["type"]),
                list(index_row["topics"]),
            ))
        except (OSError, ValueError) as error:
            issues.append(f"{relative}: {error}")

    seen_ids: set[str] = set()
    for entry in entries:
        entry_id = str(entry["id"])
        if entry_id in seen_ids:
            issues.append(f"duplicate entry id: {entry_id}")
        seen_ids.add(entry_id)

    if issues:
        print("Vocabulary site data generation failed:", file=sys.stderr)
        print("\n".join(f"- {issue}" for issue in issues), file=sys.stderr)
        return 1
    if not entries:
        print("No vocabulary entries were found in vocabulary/INDEX.md", file=sys.stderr)
        return 1

    entries.sort(key=lambda entry: str(entry["lemma"]).casefold())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Generated site data for {len(entries)} indexed words at {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
