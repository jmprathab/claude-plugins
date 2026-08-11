# jmprathab-claude-plugins

A personal [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

## Installation

Add this marketplace to Claude Code, then install the plugins you want:

```
/plugin marketplace add https://github.com/jmprathab/claude-plugins.git
```

Then browse and install:

```
/plugin
```

## Plugins

| Plugin | Description |
| --- | --- |
| **bruno** | Run API tests using Bruno CLI with environment management, test assertions, and report generation. |
| **jq** | Extract and transform specific fields from JSON files and API responses using jq. |
| **obsidian-flashcard** | Generate spaced-repetition flashcards in Obsidian Spaced Repetition plugin format from notes. |
| **obsidian-format** | Reformat raw content into clean, Obsidian-compatible Markdown without changing the wording. |
| **obsidian-note-from-transcript** | Turn a raw or timestamped transcript into a concise, vault-native Obsidian note. |
| **obsidian-vault-lint** | Health check for an Obsidian vault—broken links, malformed callouts, orphan notes, and house-rule conventions. |

## Updating

After pushing changes to the repo, refresh the marketplace in Claude Code:

```
/plugin marketplace update jmprathab-claude-plugins
```
