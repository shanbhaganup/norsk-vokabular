# Norskopplæring

This project maintains Norwegian Bokmål vocabulary for an English-speaking learner.

## Entry format

Use the matching file in templates/. TEMPLATES.md collects the worked examples. Keep one canonical entry per normalized lemma, word type and genuinely distinct sense under vocabulary/. Use UTF-8 Markdown with Norwegian spelling preserved. Keep metadata fields id, lemma, word_type, sense and checked_on at the top of each entry.

For every applicable grammatical form, include its value, at least one original Norwegian example sentence using that form, and an accurate English translation. If a cell lists alternatives, illustrate each alternative or put each in a separate row. Follow the four-column table format. Do not treat a grammatical feature, construction, or related word as an inflected form.

Include English, Topics, Form status, Notes and Sources. Use standard Bokmål labels. Nouns need article/gender and all four number/definiteness combinations. Verbs need applicable simple forms, participles, compound tenses, imperative and passive constructions; note context-dependent or unavailable constructions. Adjectives need gender/number/definiteness agreement and applicable comparison. Other word types use their own applicable forms and syntax; do not invent inflections for invariable words.

Use — only for a genuinely inapplicable form, and explain why. Use Unverified for unknown forms. A missing form is not automatically impossible. Keep dictionary forms, productive constructions and editorial examples distinguishable. Do not invent plural forms, comparatives, passives or imperatives. Examples must be natural and must match the labelled form and meaning.

## Correctness and sources

Prefer Bokmålsordboka/Ordbøkene for spelling, genders and paradigms. Cite exact entries where possible. Dictionary verification of a Norwegian headword does not verify an imported English translation. Review the sense separately. Treat examples in this project as authored teaching examples, not dictionary quotations. Preserve accepted alternatives. Explain rare or formal variants. Do not assign a Norwegian CEFR level from an English source level.

## Duplicates and imports

Search vocabulary/ and reference/vocabulary-4472/ before adding a word. Normalize case, Unicode, infinitive markers and inflected source forms. Merge genuine duplicates by lemma, word type and sense. Distinct word types or genuinely different senses may have separate entries. Put source spellings and corrections in Notes.

The reference snapshot is source material, not a second active vocabulary index. When upgrading a reference entry, create or update its working entry under vocabulary/ and record the promotion in docs/MIGRATION.md. Do not count that promotion as a new word. The 12 seeded working entries are format demonstrations and may overlap the reference snapshot; do not add their count to the snapshot count.

Keep source imports unchanged. Mark uncertain translations and paradigms for review instead of guessing. Record additions, merges and corrections in docs/CHANGELOG.md. Update vocabulary/INDEX.md and relevant topic indexes after changes. Keep the reference snapshot unchanged unless the user explicitly asks to revise it.

## Workflow

Read README.md and docs/GRAMMAR.md. Copy the appropriate template, verify the lemma and sense, add forms and bilingual examples, then update indexes. Run `python3 scripts/check_vocabulary.py` after editing working entries. The checker verifies structure and duplicate keys; it does not establish grammatical correctness. Inspect sentences and forms yourself.

Make reversible edits and follow the user's requested scope. Never claim that this file changes global ChatGPT memory or installs a skill.
