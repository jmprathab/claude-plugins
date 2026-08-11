---
name: obsidian-vault-lint
description: >-
  Health check for an Obsidian vault. Use when the user wants to "lint the vault",
  "check my notes for issues", "find broken links", "find dead wikilinks", "run a
  vault health check", "audit my notes", or check that notes follow the vault's
  conventions. Scans Markdown notes for broken [[wikilinks]] and ![[embeds]],
  unclosed code fences, heading-level skips, malformed callouts, unknown tags,
  orphan notes, and (when the vault opts in) house rules like a required tag line or
  a ban on H1 headings. Reports findings grouped by severity and only fixes when
  asked. Read-only by default.
---

# Vault Lint

A repeatable health check for an Obsidian vault. It finds notes that have rendering
problems, broken links, or that drift from the vault's house style, so the vault
stays consistent as it grows.

This skill is **read-only by default**: it reports problems and proposes fixes, but
does not modify files unless the user explicitly asks it to fix something. That
matters because some "problems" (a `[[link]]` to a note not yet written, a
deliberately flat note) are intentional — the human decides.

## How conventions work

Obsidian vaults share universal mechanics (wikilinks, embeds, code fences, headings)
but differ in house style — one vault starts every note with a tag line and forbids
H1s, another uses YAML frontmatter and H1 titles. So the linter splits its checks:

- **Universal checks** always run: broken links/embeds, unclosed fences, heading
  skips, trailing whitespace, orphan detection.
- **House-convention checks** are **opt-in flags**, because enforcing them on a vault
  that doesn't follow that convention would produce pure noise.

A vault records which flags to pass in its own `CLAUDE.md` / `AGENTS.md` (look there
first — the project file is the source of truth for *this* vault's conventions and
the exact command to run). If no such guidance exists, run the universal checks only,
then show the user the convention flags below and ask which apply.

## When to use

- "Lint the vault", "run a vault health check", "audit my notes".
- "Find broken links" / "any dead wikilinks?"
- After a bulk edit, import, or mass rename, to catch fallout.
- On a regular cadence (e.g. monthly) to keep notes tidy.

## How to run

1. **Find the vault's conventions.** Read the vault's `CLAUDE.md`/`AGENTS.md` for the
   note format and the documented lint command (which folder holds notes, whether a
   tag line is required, whether H1 is banned). Use that command if present.

2. **Run the linter:**

   ```bash
   python "<skill-dir>/scripts/vault_lint.py" "<vault-root>" [flags]
   ```

   Common flags (combine per the vault's conventions):

   | Flag | Effect |
   |------|--------|
   | `--notes-dir DIR` | Only lint `.md` files under `DIR` (repeatable). Links still resolve against the whole vault, so attachments/diagrams stay valid targets without being linted. Excalidraw `.excalidraw.md` files are always excluded. |
   | `--tags-dir DIR` | Folder of one-file-per-tag notes (default `Tags`); tag links on the tag line are validated against it. |
   | `--require-tag-line` | Flag notes whose first non-empty line isn't the tag line. |
   | `--tag-line-prefix STR` | Prefix that marks the tag line (default `Tags:`). |
   | `--forbid-h1` | Flag any `# H1` in a note body (vaults where the filename is the title). |

   The script prints JSON: `{ "summary": {...}, "findings": [ {file, line, category, severity, message}, ... ] }`.

3. **Summarize for the user**, grouped by severity, most actionable first. Lead with
   errors (broken links, stray H1s, unclosed fences). Reference notes as
   `path/to/note.md:line` so they're clickable.

4. **Only if asked to fix**, address findings note-by-note. For prose/structure
   fixes, use the `obsidian-format` skill on the specific file. For broken links,
   confirm the intended target before changing or removing a link — never silently
   delete one, since it may point to a note yet to be written.

## What it checks

**Errors (break rendering or plugins):**

- `broken-wikilink` — a `[[target]]` or `![[embed]]` whose target doesn't exist anywhere in the vault.
- `unclosed-fence` — an odd number of ` ``` ` code fences.
- `missing-tag-line` *(with `--require-tag-line`)* — first non-empty line isn't the tag line.
- `unknown-tag` *(when a tags folder exists)* — a tag on the tag line has no file in the tags folder.
- `stray-h1` *(with `--forbid-h1`)* — a `# H1` heading where the filename should be the title.

**Warnings (style / consistency):**

- `heading-skip` — heading level jumps (e.g. `##` straight to `####`).
- `tag-line-not-first` — content precedes the tag line.
- `unlabeled-fence` — a fenced code block with no language hint.
- `trailing-whitespace`, `multiple-blank-lines` — formatting noise.

**Info:**

- `orphan` — a note with no inbound links from any other note. A candidate to link from a hub/MOC.

## Machine syntax is protected

Plugin-parsed syntax is fragile and is **never flagged for reformatting** — the
linter only flags it when it appears *broken* (e.g. an embed whose target is
missing). The linter automatically skips:

- Flashcard / spaced-repetition regions (`#card/`, `#flashcards`, `<!--SR:…-->`, and a `## Flashcards` section).
- YAML frontmatter and Kanban boards (`kanban-plugin:` frontmatter) — these notes are exempt from tag-line/H1 rules.
- Excalidraw files (`.excalidraw.md`) are never linted as prose.

When fixing, extend that same care to LaTeX (`$…$`, `$$…$$`), block anchors
(`^id`), and block/heading reference links (`[[Note#^id]]`, `[[Note#Heading]]`).

## Hard constraints

- Default to read-only. Don't edit notes unless explicitly told to fix.
- Never delete or rewrite machine syntax (flashcards, Kanban, Excalidraw, LaTeX, block anchors).
- Never create a new tag to resolve an `unknown-tag` finding — surface it and let the user decide.
- Confirm before changing or removing any wikilink.
