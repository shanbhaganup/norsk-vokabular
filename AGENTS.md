# Norskopplæring

Maintain accurate Norwegian Bokmål vocabulary for English-speaking learners. Preserve Norwegian spelling in UTF-8 Markdown.

## Entries

- Before adding a word, search `vocabulary/` for duplicates. If a reference snapshot is supplied for the task, check it too. Normalize case, Unicode, infinitive markers and inflected source forms. Keep one entry per lemma, word type and genuinely distinct sense; record source spellings and corrections in Notes.
- Use the matching file in `templates/` and follow `docs/GRAMMAR.md`. Each entry needs top metadata `id`, `lemma`, `word_type`, `sense`, `checked_on`, plus English, Topics, Form status, Notes and Sources.
- For every applicable form, give its value and an original, natural Norwegian example using that form, with an accurate English translation. Use the four-column form table. Illustrate each accepted alternative. Keep inflections distinct from constructions, related words and editorial examples.
- Include the applicable paradigm for each word type: nouns need article/gender and all four number/definiteness forms; verbs need applicable simple forms, participles, compound tenses, imperative and passive; adjectives need agreement and applicable comparison. Other types need their applicable forms and syntax. Do not invent forms or inflections for invariable words.
- Use `—` only for genuinely inapplicable forms and explain why. Use `Unverified` for unknown forms. A missing form is not proof that it is impossible. Explain context-dependent, rare or formal variants.

## Verification and sources

Prefer Bokmålsordboka/Ordbøkene for spelling, gender and paradigms; cite exact entries where possible. Verify English meanings separately: a checked Norwegian headword does not verify its translation. Treat project examples as authored teaching examples, not dictionary quotations. Preserve accepted alternatives. Do not assign a Norwegian CEFR level from an English source level. Keep source imports and any supplied reference snapshot unchanged unless explicitly asked to revise them.

## Imports and maintenance

- A supplied reference snapshot is source material, not a second active index. When promoting an entry from it, create or update the working entry; do not count the promotion as a new word. The 12 seeded format demonstrations are examples, not additional words.
- Mark uncertain translations and paradigms for review rather than guessing.
- Update `vocabulary/INDEX.md` after changes. It is the single searchable index with word, type (noun followed by article/gender), English meaning and topic. Do not create or maintain separate topic index files.
- Read `README.md` and `docs/GRAMMAR.md`; use the matching template, verify lemma and sense, and add forms and bilingual examples. After editing working entries, run `python3 scripts/check_vocabulary.py`. It checks structure and duplicate keys, not grammatical correctness; inspect forms and sentences yourself.

Follow the requested scope and make reversible edits. This file does not change global ChatGPT memory or install a skill.
