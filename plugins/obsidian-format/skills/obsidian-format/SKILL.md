---
name: obsidian-format
description: >-
  Reformat a file's raw content into clean, Obsidian-compatible Markdown without
  changing the wording. Use when the user wants to "format this for Obsidian",
  "make this Obsidian compatible", "clean up this markdown", "reformat this note",
  "fix the formatting of this .md file", or asks to tidy a markdown/text file so it
  renders correctly in Obsidian. Preserves content; fixes structure (headings,
  lists, code blocks, tables, spacing), adds frontmatter if missing, and applies
  Obsidian features (callouts, wikilinks, tags) only where clearly appropriate.
---

# Obsidian Format

Reformat a given file's raw content into well-structured, Obsidian-compatible
Markdown. **Preserve the content** — fix formatting and structure, do not rewrite,
summarize, reorder, or paraphrase the author's words.

## Scope

- **Input:** markdown or near-markdown files (`.md`, `.txt`, notes). Not for HTML
  exports, PDFs, or binary formats.
- **Output:** the same file, rewritten in place.

## Interactivity mode

Default to **interactive** unless the invoking prompt explicitly says otherwise.

- **Interactive (default):** After producing the reformatted version, show the user
  a concise summary of the structural changes (and a diff if helpful), then confirm
  with `AskUserQuestion` BEFORE overwriting the file. If the user declines, do not
  write.
- **Non-interactive / headless:** If the prompt contains the keyword
  `non-interactive` (or `headless`), skip all prompts and overwrite the file
  directly. Do not call `AskUserQuestion`.

## Workflow

1. **Read** the target file's full raw content.
2. **Consult Obsidian syntax** by invoking the `obsidian-markdown` skill (its
   reference files cover callouts, embeds, and properties). Do not duplicate that
   syntax knowledge here — rely on it.
3. **Reformat** the content applying the rules below.
4. **Mode gate:**
   - Interactive: present a change summary and confirm via `AskUserQuestion`.
   - Non-interactive: proceed.
5. **Write** the reformatted content back to the same path (only after confirmation
   in interactive mode).
6. **Report** what changed in a short bulleted summary.

## Formatting rules (structure — always safe)

- Ensure exactly one top-level `# H1`; demote/normalize the heading hierarchy so
  levels don't skip (no H1 -> H3 jumps).
- Put a blank line before and after headings, lists, tables, and fenced code blocks.
- Normalize list markers (consistent `-` for bullets; `1.` ordered) and indentation.
- Wrap code in fenced blocks with a language hint where the language is obvious;
  convert stray indented code to fenced blocks.
- Normalize tables (aligned pipes, header separator row).
- Trim trailing whitespace; collapse 3+ blank lines to one; ensure a single
  trailing newline; normalize line endings.
- Fix obviously broken markdown syntax (unclosed code fences, malformed links).

## Obsidian features (apply only when clearly appropriate)

- **Frontmatter:** If the file has no YAML frontmatter, add a minimal block with
  `title` (from the H1 or filename), `date`, and empty `tags: []`. If frontmatter
  already exists, leave it intact (only fix YAML syntax errors).
- **Callouts:** Convert clear "Note:", "Warning:", "Tip:", "Important:" style blocks
  into Obsidian callouts (`> [!note]`, `> [!warning]`, etc.). Only when the intent is
  unambiguous.
- **Wikilinks:** Convert internal references that clearly point to other vault notes
  into `[[wikilinks]]`. Leave external URLs as standard `[text](url)` links. When in
  doubt, leave the link as-is.
- **Tags:** Only add/move tags into frontmatter if the source already contains them.
  Do not invent new tags.

## Hard constraints

- Never change, summarize, translate, reorder, or paraphrase the actual prose/content.
- Never delete content. The only removals allowed are redundant whitespace/blank lines.
- If unsure whether a transformation changes meaning, prefer the conservative choice
  and leave it as-is.
