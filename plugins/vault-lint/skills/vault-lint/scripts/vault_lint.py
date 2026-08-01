#!/usr/bin/env python3
"""Generic linter for an Obsidian vault.

Scans every Markdown note in a vault and reports issues that hurt rendering,
break plugins, or drift from a vault's house style. It is intentionally vault-
agnostic: the universal Obsidian/Markdown checks run by default, and the opinionated
"house convention" checks (tag-line-first, no-H1) are opt-in flags so each vault can
enforce only the rules it actually adopts. A vault documents which flags to pass in
its own CLAUDE.md / AGENTS.md.

Read-only: never modifies files.

Usage:
    python vault_lint.py VAULT_ROOT [options]

Options:
    --notes-dir DIR       Folder (relative to root) whose .md files are linted as
                          prose notes. Repeatable. Link/embed targets are always
                          resolved against the WHOLE vault regardless of this, so
                          attachments and diagrams stay valid targets without being
                          linted themselves. Default: the whole vault.
    --tags-dir DIR        Folder of one-file-per-tag notes (e.g. "Tags"). If present,
                          tag links on the tag line are validated against it.
    --require-tag-line    Flag notes whose first non-empty line isn't the tag line.
    --tag-line-prefix STR Prefix that identifies the tag line. Default: "Tags:".
    --forbid-h1           Flag any "# H1" in a note body (vaults where the filename
                          is the title and bodies start at "##").

Output: a JSON object {summary, findings} on stdout.
"""

import argparse
import json
import os
import re
import sys

# Windows consoles default stdout to the active codepage (e.g. cp1252), not UTF-8.
# Finding messages can embed non-ASCII characters from note content (em dashes,
# smart quotes, etc.), so force UTF-8 to avoid UnicodeEncodeError / mangled output.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Folders that hold config or version-control data, never notes.
IGNORED_DIRS = {".obsidian", ".git", ".trash", ".smart-env", "node_modules"}

# [[target]], [[target|alias]], [[target#heading]], [[target#^anchor]], ![[embed]]
LINK_RE = re.compile(r"(!?)\[\[([^\]]+?)\]\]")


def link_target(raw):
    """Extract the resolvable note/attachment name from a wikilink's inner text.

    Strips the alias (after `|`) and any heading/block reference (after `#`). Inside
    a Markdown table cell the alias pipe is escaped as `\\|` to avoid splitting the
    cell — treat that as a normal alias separator, not part of the target name.
    """
    raw = raw.replace("\\|", "|")
    return raw.split("|")[0].split("#")[0].strip()
# Spaced-repetition / flashcard plugin markers — these regions are fragile and are
# never style-checked, only validated for broken embeds.
CARD_MARKER_RE = re.compile(r"#card/|#flashcards|<!--SR:")


def split_frontmatter(text):
    """Return (frontmatter_str_or_None, body)."""
    if text.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
        if m:
            return m.group(1), text[m.end():]
    return None, text


def walk_markdown(root, notes_dirs):
    """Yield (stem, abspath) for lintable .md files.

    If notes_dirs is given, only .md files under those subfolders are linted; this
    keeps machine-generated Markdown (e.g. Excalidraw drawings) out of prose checks.
    Excalidraw files are always excluded — they are JSON wrapped in Markdown.
    """
    roots = [os.path.join(root, d) for d in notes_dirs] if notes_dirs else [root]
    for base in roots:
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
            for f in filenames:
                if f.endswith(".md") and not f.endswith(".excalidraw.md"):
                    yield f[:-3], os.path.join(dirpath, f)


def build_target_index(root):
    """Set of lowercased names that a [[link]] or ![[embed]] may resolve to.

    Obsidian resolves links vault-wide regardless of folder, by filename or stem.
    """
    names = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for f in filenames:
            names.add(f.lower())                       # full filename, e.g. img.png
            names.add(os.path.splitext(f)[0].lower())  # stem, e.g. img
            if f.endswith(".excalidraw.md"):           # Excalidraw double extension
                names.add(f[: -len(".excalidraw.md")].lower())
    return names


def known_tags(root, tags_dir):
    d = os.path.join(root, tags_dir)
    tags = set()
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                tags.add(f[:-3].lower())
    return tags


def flashcard_line_indices(lines):
    """Indices of lines inside a flashcard/SR region — skipped by style checks.

    Flashcard decks are conventionally the terminal section of a note, and group
    their cards under sub-headings (often `###`, sometimes `## Section N`). Closing
    the region at the next heading would wrongly re-enable checks mid-deck and flag
    the `[[links]]` and `::` clozes inside cards. So once a `## Flashcards` heading
    or any `#card/` marker is seen, the region runs to end-of-file. `<!--SR:-->`
    scheduling lines are always treated as card lines too (they can trail a card
    that sits above the heading).
    """
    skip = set()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+Flashcards\s*$", ln.strip()) or CARD_MARKER_RE.search(ln):
            start = i
            break
    if start is not None:
        skip.update(range(start, len(lines)))
    for i, ln in enumerate(lines):
        if "<!--SR:" in ln:
            skip.add(i)
    return skip


def lint_note(stem, path, rel, targets, tagset, cfg):
    findings = []
    text = open(path, encoding="utf-8").read()
    fm, _ = split_frontmatter(text)
    lines = text.split("\n")

    def add(line, category, severity, message):
        findings.append({"file": rel, "line": line, "category": category,
                         "severity": severity, "message": message})

    is_kanban = fm is not None and "kanban-plugin" in fm
    is_fm_stub = fm is not None  # frontmatter-driven note (e.g. media DB entries)
    plugin_owned = is_kanban or is_fm_stub

    # --- house-convention checks (opt-in) ---
    if not plugin_owned:
        first_idx = next((i for i, l in enumerate(lines) if l.strip()), None)
        if first_idx is None:
            add(1, "empty-note", "info", "Note is empty.")
        else:
            first = lines[first_idx]
            is_tag_line = first.startswith(cfg.tag_prefix)
            if cfg.require_tag_line and not is_tag_line:
                add(first_idx + 1, "missing-tag-line", "error",
                    f"First non-empty line is not a '{cfg.tag_prefix}' line.")
            elif cfg.require_tag_line and first_idx != 0:
                add(first_idx + 1, "tag-line-not-first", "warning",
                    f"Blank line(s) precede the '{cfg.tag_prefix}' line.")
            if is_tag_line and tagset:
                for _, target in LINK_RE.findall(first):
                    t = link_target(target).lower()
                    if t and t not in tagset:
                        add(first_idx + 1, "unknown-tag", "error",
                            f"Tag [[{target}]] has no file in the tags folder.")

    # --- per-line checks ---
    fence_count, prev_level = 0, 0
    card_lines = flashcard_line_indices(lines)
    for i, ln in enumerate(lines):
        lineno = i + 1
        in_card = i in card_lines

        if cfg.forbid_h1 and not plugin_owned and not in_card and re.match(r"^#\s+\S", ln):
            add(lineno, "stray-h1", "error",
                "Stray '# H1' — in this vault the filename is the title and bodies start at '##'.")

        hm = re.match(r"^(#{1,6})\s+\S", ln)
        if hm and not in_card:
            level = len(hm.group(1))
            if prev_level and level > prev_level + 1:
                add(lineno, "heading-skip", "warning",
                    f"Heading jumps from H{prev_level} to H{level} (skips a level).")
            prev_level = level

        if ln.strip().startswith("```"):
            fence_count += 1
            if fence_count % 2 == 1 and not ln.strip()[3:].strip():
                add(lineno, "unlabeled-fence", "warning", "Fenced code block has no language hint.")

        if ln != ln.rstrip():
            add(lineno, "trailing-whitespace", "warning", "Trailing whitespace.")

        # link/embed resolution — skip flashcard regions, code, and the tag line
        if not in_card and fence_count % 2 == 0 and not ln.startswith(cfg.tag_prefix):
            for bang, raw in LINK_RE.findall(ln):
                target = link_target(raw)
                if target == "":   # in-note ref like [[#Heading]] — not validated
                    continue
                if target.lower() not in targets:
                    kind = "embed" if bang else "wikilink"
                    add(lineno, "broken-wikilink", "error",
                        f"Broken {kind}: [[{raw}]] — target '{target}' not found in vault.")

    if fence_count % 2 == 1:
        add(len(lines), "unclosed-fence", "error", "Odd number of ``` fences (unclosed code block).")
    for m in re.finditer(r"\n{4,}", text):
        add(text[: m.start()].count("\n") + 1, "multiple-blank-lines", "warning",
            "3+ consecutive blank lines.")

    return findings


def main():
    ap = argparse.ArgumentParser(description="Lint an Obsidian vault.")
    ap.add_argument("root", nargs="?", default=".", help="Vault root (default: cwd)")
    ap.add_argument("--tags-dir", default="Tags")
    ap.add_argument("--require-tag-line", action="store_true")
    ap.add_argument("--tag-line-prefix", dest="tag_prefix", default="Tags:")
    ap.add_argument("--forbid-h1", action="store_true")
    ap.add_argument("--notes-dir", dest="notes_dirs", action="append", default=[])
    cfg = ap.parse_args()
    root = cfg.root

    targets = build_target_index(root)
    tagset = known_tags(root, cfg.tags_dir)
    notes = [(stem, path, os.path.relpath(path, root).replace("\\", "/"))
             for stem, path in walk_markdown(root, cfg.notes_dirs)]

    # inbound-link counts for orphan detection
    inbound = {stem.lower(): 0 for stem, _, _ in notes}
    for stem, path, _ in notes:
        for _, raw in LINK_RE.findall(open(path, encoding="utf-8").read()):
            t = link_target(raw).lower()
            if t in inbound and t != stem.lower():
                inbound[t] += 1

    findings = []
    for stem, path, rel in notes:
        findings.extend(lint_note(stem, path, rel, targets, tagset, cfg))

    for stem, path, rel in notes:
        if inbound.get(stem.lower(), 0) == 0:
            text = open(path, encoding="utf-8").read()
            fm, _ = split_frontmatter(text)
            if fm is None and not CARD_MARKER_RE.search(text):
                findings.append({"file": rel, "line": 1, "category": "orphan",
                                 "severity": "info",
                                 "message": "No inbound links from other notes — consider linking it from a hub/MOC."})

    by_sev, by_cat = {"error": 0, "warning": 0, "info": 0}, {}
    for f in findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
        by_cat[f["category"]] = by_cat.get(f["category"], 0) + 1

    rank = {"error": 0, "warning": 1, "info": 2}
    print(json.dumps({
        "summary": {"notes_scanned": len(notes), "findings": len(findings),
                    "by_severity": by_sev, "by_category": by_cat},
        "findings": sorted(findings, key=lambda f: (rank[f["severity"]], f["file"], f["line"])),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
