# Norskopplæring — Codex project template

A Norwegian Bokmål vocabulary project with 12 templates and 12 worked entries. Every applicable form or feature row has a Norwegian example and an English translation. The earlier 4,472-entry vocabulary package is included as a reference snapshot.

## Start

1. Extract the ZIP. Keep the project folders together so Markdown links work.
2. Open the extracted Norskopplaering_Codex_Project folder as your working folder in Codex. Use the root of the project so AGENTS.md is the project instruction file. See the [official instruction-file guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
3. Read [AGENTS.md](AGENTS.md) and [grammar conventions](docs/GRAMMAR.md).
4. Browse [all templates and examples](TEMPLATES.md), or open [the working vocabulary index](vocabulary/INDEX.md).
5. Use a prompt from [STARTER_PROMPTS.md](STARTER_PROMPTS.md) to add, promote, review or practise entries.
6. After editing working entries, run `python3 scripts/check_vocabulary.py` from the project root. Python 3 is the only dependency for the checker. Reading and editing Markdown requires no Python packages.

## Files and folders

| Location | Contents |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Project instructions: format, examples, sources, duplicates and verification |
| [TEMPLATES.md](TEMPLATES.md) | All 12 worked examples in one document |
| templates/ | One copyable template and worked example per word type |
| [vocabulary/INDEX.md](vocabulary/INDEX.md) | Links to 12 working example entries |
| topics/ | Topic indexes for those working examples |
| [reference/README.md](reference/README.md) | Existing 4,472-entry vocabulary, unchanged |
| [imports/README.md](imports/README.md) | Instructions for future source lists |
| [review/README.md](review/README.md) | Questions and uncertain forms needing review |
| [docs/GRAMMAR.md](docs/GRAMMAR.md) | Grammar, status and example-writing conventions |
| [docs/MIGRATION.md](docs/MIGRATION.md) | Promoting reference entries without counting duplicates |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Project change history |
| [docs/SOURCES.md](docs/SOURCES.md) | Sources and authorship |
| [STARTER_PROMPTS.md](STARTER_PROMPTS.md) | Ready-to-use Codex prompts |
| scripts/check_vocabulary.py | Checks working-entry structure, examples and duplicate metadata keys |

## Word types

Substantiv, verb, adjektiv, adverb, pronomen, determinativer, preposisjoner, konjunksjoner, subjunksjoner, interjeksjoner, uttrykk, and tallord each have a separate template. The adverb example fort is explicitly an adverbial use of an adjective; the numeral example labels related ordinal andre separately from cardinal to.

## Using a template

Copy the code block from a template into a new file in the relevant vocabulary subfolder. Replace the placeholders, then add this metadata at the top:

```yaml
---
id: verb-forstaa
lemma: forstå
word_type: verb
sense: main
checked_on: YYYY-MM-DD
---
```

Allowed word_type values: noun, verb, adjective, adverb, pronoun, determiner, preposition, conjunction, subjunction, interjection, expression, numeral. Keep id unique. If there are genuinely different senses, use a specific sense value and a distinct id. Copy the metadata pattern from a worked entry if preferred.

Each table has four columns: Form / feature, Value, Norwegian example, English translation. An example must use the listed form. Illustrate every accepted alternative listed in the same cell, or split it into separate rows. Use — for an inapplicable form with a reason; use Unverified when a form is unknown. Usage constructions and related words are labelled explicitly.

The 12 worked entries demonstrate the enriched layout. The 4,472-entry reference retains its existing layout and verification notes; its entries can be promoted individually when requested. Working examples and reference copies are not additive counts of unique words. AGENTS.md carries project guidance; it does not update global ChatGPT memory or automatically convert an existing ChatGPT project.
