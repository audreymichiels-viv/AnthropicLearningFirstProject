# Project Notes — Anthropic Learning

A learning sandbox for the Anthropic API and Claude Code skills.

## What this project contains

| File | Purpose |
|---|---|
| `main.py` | Python CLI that translates and corrects French ↔ English in photo-caption style. |
| `requirements.txt` | One dependency: `anthropic`. |
| `.claude/skills/photo-captions/SKILL.md` | Claude Code skill — single source of truth for the caption style and name corrections. |

## How to run the translator

```bash
source venv/bin/activate
python main.py "your sentence here"
```

Requires `ANTHROPIC_API_KEY` in the environment.

## Key concepts learned

### System prompt
The standing instructions Claude follows on every request. Defines tone, format, and rules. In `main.py`, the system prompt is built at runtime from two pieces:
- `OUTPUT_FORMAT_INSTRUCTIONS` (hardcoded — defines the output structure)
- The body of `SKILL.md` (read from disk — defines the style rules)

### Adaptive thinking
`thinking={"type": "adaptive"}` — lets Claude decide how much to think before answering. Useful when judgement matters (like grammar correction).

### Prompt caching
`cache_control: {"type": "ephemeral"}` — caches the system prompt for ~5 minutes so repeated runs cost less. Cache hits cost ~0.1× the normal token price.

### Skills
A skill is a folder containing a `SKILL.md` file. The structure:

```
.claude/skills/<skill-name>/
  └── SKILL.md
```

`SKILL.md` has two parts:
- **Frontmatter** (between `---` lines): `name` and `description`. The description is what Claude reads to decide whether the skill is relevant.
- **Body**: the actual instructions Claude follows when the skill activates.

## Skills in different contexts — the mental model

| Where | How it uses skills |
|---|---|
| Claude Code (the CLI) | Auto-scans `.claude/skills/` on startup. Loads skills lazily based on description matching. Tunes style — does **not** auto-trigger actions. |
| `main.py` (plain API calls) | No skill mechanism on the API side. Python reads `SKILL.md` from disk and inlines its body in the system prompt. Always loaded. |
| Managed Agents (Anthropic-hosted) | Upload skills via the Skills API, reference by ID. Not used in this project. |

**The crucial insight:** `main.py` doesn't "call" the skill — it just reads the file. Same SKILL.md file, two different consumers, two completely different mechanisms.

## My specific choices for this project

- **Caption style**: friendly, fun, short, not over-the-top. No strings of exclamation marks. Casual French abbreviations welcome (`aprem'`, `resto`, `anniv`, `p'tit`).
- **Auto-corrections**: `Pape` → `Papé`, `Mame` → `Mamé` (keyboard lacks accent aigu).
- **One source of truth**: rules live in `SKILL.md` only. Editing it updates both the Claude Code skill and the translator.

## Common pitfalls & gotchas

- **New skills aren't loaded mid-session.** Created a skill in this Claude Code session? Restart Claude Code to pick it up.
- **Skills tune behavior, they don't replace conversation.** Sending Claude Code an isolated phrase like "afternoon with Papé" won't auto-translate — you need to ask explicitly.
- **The translator runs as a separate process.** It uses the API directly and has its own system prompt. The Claude Code skill mechanism doesn't apply to it — that's why we read `SKILL.md` from disk in `main.py`.

## How to extend

- **Change the style or add another name correction**: edit `SKILL.md`, save. Both consumers update.
- **Change the output format of the translator**: edit `OUTPUT_FORMAT_INSTRUCTIONS` in `main.py`.
- **Add a new skill for a different use case**: create another folder under `.claude/skills/` with its own `SKILL.md`.

---

## Learning journal

*Each session appends a dated entry here. Older entries on top, newest at the bottom.*

*********** 25/05/2026 — Session 1 ***********

- **Built the translator** (`main.py`): a Python CLI that calls the Anthropic API to translate and correct French ↔ English in photo-caption style.
- **New concepts:**
  - *System prompt* — the standing instructions Claude follows on every request.
  - *Adaptive thinking* — `thinking={"type": "adaptive"}` lets Claude decide how much to reason.
  - *Prompt caching* — `cache_control` caches the system prompt for ~5 min at ~0.1× cost.
- **Created a Claude Code skill** (`.claude/skills/photo-captions/SKILL.md`) with the caption style and the Pape→Papé / Mame→Mamé fix.
- **The big distinction:** Claude Code auto-discovers skills from `.claude/skills/`. The plain Anthropic API does not. To use a skill from `main.py`, we read `SKILL.md` from disk and inline its body in the system prompt.
- **Refactored for one source of truth:** `main.py` now reads `SKILL.md` at runtime. Edit the skill — both the translator and Claude Code update.
- **Set up this learning journal** — future sessions append new dated entries below.
