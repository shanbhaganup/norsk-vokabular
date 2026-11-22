# Norskopplæring — Bokmål vocabulary

A Norwegian Bokmål vocabulary project for English-speaking learners.

## Start

1. Open the project root in Codex so `AGENTS.md` provides the project instructions.
2. Read [the project instructions](AGENTS.md) and [grammar conventions](docs/GRAMMAR.md).
3. Choose a word-type template in [templates/](templates/) or search the [working vocabulary index](vocabulary/INDEX.md).

## Project files

| Location | Contents |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Entry, source, duplicate and maintenance rules |
| [templates/](templates/) | Copyable entry templates with a worked example for each word type |
| [vocabulary/INDEX.md](vocabulary/INDEX.md) | Searchable index of working entries by word, type or noun gender, English meaning and topic |
| imports/ | Source lists and import guidance |
| review/ | Uncertain forms and questions for review |
| [docs/GRAMMAR.md](docs/GRAMMAR.md) | Form-label meanings and word-type conventions |
| [STARTER_PROMPTS.md](STARTER_PROMPTS.md) | Example prompts for common tasks |
| scripts/check_vocabulary.py | Structural and duplicate-key checker |

After editing working entries, run `python3 scripts/check_vocabulary.py`. The checker verifies structure and duplicate keys; it does not verify grammatical correctness.
