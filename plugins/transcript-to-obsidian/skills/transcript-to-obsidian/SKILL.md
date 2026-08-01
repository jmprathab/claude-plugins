---
name: transcript-to-obsidian
description: >-
  Use when the user pastes a transcript, points at a file containing a raw or timestamped
  transcript, or asks to "turn this transcript into notes", "make Obsidian notes from this
  video", "summarize this YouTube video / webinar / lecture / podcast / interview / meeting
  into a note", "structure this transcript", or drops a wall of timestamped spoken text. Turns
  spoken-word source material into a concise, vault-native Obsidian note that matches the target
  vault's conventions, overwriting the transcript in place after confirming.
---

# Transcript → Obsidian Note

Turn a raw transcript (YouTube, lecture, podcast, talk) into a concise, high-quality note that
drops straight into an Obsidian vault. The transcript is the *source material*, not the output —
extract the core concepts, key takeaways, and actionable steps, then restructure them into a note
that reads like it was written, not transcribed.

**Brevity is the goal, not coverage.** A transcript of an hour of talking should compress to a note
that's read in a couple of minutes. Distil — don't transcribe-with-headings. If a sentence doesn't
add a concept, a number, or a decision, cut it. Favour bullets and tables over paragraphs, and lean
on the recall techniques below (mnemonics, a tight Executive Summary) so the few things that matter
actually stick. A shorter note the user re-reads beats a thorough one they never reopen.

Companion skills do the heavy lifting on syntax and vault mechanics — lean on them instead of
restating:

- **obsidian-markdown** — the syntax reference for callouts, wikilinks, embeds, math, and tags.
- **obsidian-cli** — read, search, list tags, and write notes from the command line.
- **vault-lint** — verify the finished note against the vault's conventions.

## Input

- **Primary case:** a file holding a raw or timestamped transcript. Read it, then overwrite it in
  place with the finished note.
- **Fallback case:** a transcript pasted directly in chat. Ask where it should be saved (suggest a
  title derived from the topic) before writing.

A transcript is messy spoken language. Before structuring, strip the noise: timestamps, speaker
labels, filler ("uh", "um", "you know"), repetition, ad-reads, music markers, and "like and
subscribe" chatter. Keep only the substantive content. A reader of the final note should never be
able to tell it came from a transcript.

**Stay faithful to the source.** Capture only what the transcript actually says — distil and
reorganize, but never invent facts, fill gaps with outside knowledge, or "improve" the argument.
Preserve exact technical terms, names, and numbers. If the transcript is too garbled,
auto-generated with clear errors, or in a language you can't reliably handle, say so and ask for a
clean version rather than guessing. If the named file already holds a finished note (not a raw
transcript), don't blindly overwrite — ask whether to redo, refine, or leave it.

## Match the vault's conventions

Different vaults have different house rules, and a note that ignores them won't organize or render
correctly. Before writing, read **3–5 representative existing notes** (the most topically related
ones) plus any project instructions such as a `CLAUDE.md`. If conventions look inconsistent across
notes, follow the most recent / most common pattern, or ask. A brand-new vault with nothing to
learn from? Fall back to the Output Structure below. Pay attention to:

- **Tagging** — how tags are written and placed: a leading `Tags:` line of `[[wikilinks]]`, YAML
  frontmatter (`tags:`), or inline `#hashtags`. Match the format the vault already uses. Reuse the
  vault's *existing* tags — discover them via obsidian-cli or by browsing the tags folder. Tag by
  **topic**, not by source medium (don't add a "video" tag). If the vault uses a closed tag set and
  none fit, describe the note and the closest tags and **ask** — don't invent one. (If the vault has
  no tag system at all, a topical tag derived from the content is fine.)
- **Title** — many vaults treat the filename as the title and start the body at `##` (no `# H1`,
  no YAML frontmatter). Follow whatever the existing notes do.
- **Headings, lists, callouts** — mirror the depth and style already in use.

If a `vault-lint` skill is available, treat its rules as the source of truth and run it at the end.
If it isn't, verify manually against the 3–5 sample notes (tag format, heading depth, callout style)
before finishing.

## Workflow

1. **Locate the source.** Get the transcript file path from the user or context (the vault is
   wherever that file lives). If it was pasted with no file, ask where to save it.
2. **Learn the conventions** (above) — find the sample notes with obsidian-cli search, or by
   globbing the vault for `.md` files near the source and reading the most relevant ones.
3. **Cross-link related notes.** Reference notes that **already exist** inline as `[[Note Name]]`
   (or `[[Note Name|display text]]`) where they directly support a point — search first to confirm
   the target exists; don't link speculatively or for the sake of connectivity.
4. **Draft the note** using the Output Structure below.
5. **Confirm, then overwrite in place.** Show the user the finished note and the target path, ask
   for a single go-ahead to replace the transcript, then write it — one confirmation for the whole
   note, not a prompt per edit. Because this destroys the original transcript, do not skip the
   confirmation; if the user declines, save to a new file or revise instead. If the filename is a
   poor title (e.g. `transcript.md` or a raw video ID), suggest a better one and offer to rename.
6. **Verify and finish.** Run the vault-lint skill if available (else re-check against the sample
   notes), fix what you can, and surface anything you can't. Done = file written, conventions pass,
   and you've told the user the final note path.

## Output Structure

Emit this shape, adapting tag placement and title style to the vault. The `## Executive Summary`
right after the tags is the high-value part — the 3–5 takeaways someone gets from re-reading the
note in 20 seconds — so write it last, once the body has clarified what actually matters.

```markdown
Tags: [[topic-tag]] [[second-tag-if-applicable]]

## Executive Summary

- Core takeaway one.
- Core takeaway two.
- (3–5 bullets total — the essence of the content.)

## <Section reflecting the source's structure>

Concise, information-dense prose and bullets. Cross-link with [[Note Name]].

### <Subsection>

- Use numbered lists only when sequence matters (steps, ordered processes).
- Use tables for comparisons.

## References

- [Source title](https://source-url)
```

If no URL is available, cite the source descriptively (e.g. `- Transcript — <speaker/topic>, <event>`)
or ask the user for it; never fabricate a link. If the content is very long after compression
(roughly 3000+ words) or spans several unrelated topics, propose splitting it into a short hub note
that links out to one note per topic — confirm with the user before creating multiple files.

## Visualizations (Mermaid, Excalidraw) & LaTeX

A diagram earns its place **only when it conveys something prose and tables cannot** — a
structure, flow, or set of relationships the reader would otherwise have to reconstruct in their
head. Most notes need zero diagrams. Do not add one to look thorough; a well-organized list or
comparison table is usually clearer and cheaper. Before drawing, ask: "Does this picture let the
reader understand a relationship faster than a paragraph would?" If not, skip it.

When a visual *is* warranted, pick the right tool and use its MCP rather than hand-writing the
source — the MCPs validate and render, so the output is guaranteed to display correctly:

- **Mermaid** (Mermaid MCP) — the default for *structured, code-describable* diagrams: flowcharts,
  pipelines, decision trees, sequence and state diagrams, simple architecture. Validate/render the
  diagram with the Mermaid MCP before embedding the fence so it can't render-fail in Obsidian. See
  obsidian-markdown for exact fence syntax.
- **Excalidraw** (Excalidraw MCP) — for *free-form, spatial, or hand-drawn-feel* visuals that
  Mermaid can't express well: conceptual maps, annotated sketches, layered architecture with custom
  layout, anything where position and grouping carry meaning. Generate it via the Excalidraw MCP and
  embed the resulting drawing; never hand-edit the embedded JSON.

Rule of thumb: if you can describe it as nodes-and-edges, use Mermaid; if it needs spatial freedom
or a sketch feel, use Excalidraw; if a table or list says it just as clearly, use neither. If the
needed MCP isn't available, fall back to a plain ` ```mermaid ` fence (only if you're confident the
syntax is valid) or to a table/bulleted breakdown — never embed an unvalidated, possibly-broken
diagram.

- **LaTeX math** — whenever the source presents a formula, transcribe it as **Obsidian-compatible
  LaTeX** (rendered by MathJax) rather than paraphrasing in words. Use `$...$` for inline math and
  `$$...$$` (on their own lines) for block equations. Stick to MathJax-supported commands; see
  obsidian-markdown for the exact syntax and the handful of Obsidian-specific gotchas (e.g. avoid a
  space after the opening `$`, escape literal `$`).

## Mnemonics

When the source presents a list worth remembering (steps, components, principles), add a mnemonic
as a callout to aid recall — acronyms work best:

```markdown
> [!note] Mnemonic Device (SPLAR)
>
> - **S**elf-Attention (Multi-head)
> - **P**ositional Encoding
> - **L**ayer Normalization
> - **A**dd (Residual Connections)
> - **R**esidual Feed-Forward Networks
```

Add a mnemonic only when it genuinely helps recall: a list of roughly 3–6 items whose initials form
a pronounceable or memorable acronym. If the letters don't cooperate, skip it — a forced acronym is
worse than none.
