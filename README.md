# bassem-elsodany-skills

**One marketplace, two Claude Code plugins: Rust skills for AI coding agents, and a study tutor that turns course material into lessons, audited quizzes and an interactive player. Add the catalog once, then pick what to install.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This repository is only a **catalog**: it holds a `marketplace.json` that tells Claude Code where each plugin lives. The plugins themselves stay in their own repositories, with their own issues, releases and versions. Nothing here is copied or forked.

*Topics: claude-code, claude-code-plugin, claude-code-marketplace, agent-skills, rust, education.*

## Quick start (about one minute)

**1. Add the catalog once** (in Claude Code):

```
/plugin marketplace add bassem-elsodany/bassem-elsodany-skills
```

**2. Install what you want.** Run `/plugin` to browse the catalog and pick, or install by name:

```
/plugin install rs-skills@bassem-elsodany-skills
/plugin install study-guide-tutor-skill@bassem-elsodany-skills
```

**3. Reload and check:** `/reload-plugins` (or start a new session), then `/plugin` → *Installed*.

## What is in the catalog

| Plugin | Install | What it does | Repository |
|---|---|---|---|
| **rs-skills** | `/plugin install rs-skills@bassem-elsodany-skills` | Rust skills for AI coding agents: an entry router, SDK-first and ports-and-adapters gates, threat-model security review, fuzzing, release checks, cleanup and git discipline (62 skills, 400+ rules) | [bassem-elsodany/rs-skills](https://github.com/bassem-elsodany/rs-skills) |
| **study-guide-tutor-skill** | `/plugin install study-guide-tutor-skill@bassem-elsodany-skills` | Turns slides, notes and PDFs into a source-checked tutoring course: learner intake, fact ledger, lessons with tricky-part hints, audited quizzes, spaced flashcards, a timed exam and an interactive study player | [bassem-elsodany/study-guide-tutor-skill](https://github.com/bassem-elsodany/study-guide-tutor-skill) |

Each plugin's README has its own requirements, configuration and limits. Read it before installing.

## Keeping up to date

```
/plugin marketplace update bassem-elsodany-skills
```

pulls the latest catalog. A plugin's own version changes when its repository publishes a new release; see its releases page.

## Questions

**Why a catalog and not one repository with everything?** Each plugin keeps its own version, issues, stars and release notes, and can be installed on its own straight from its repository (`/plugin marketplace add bassem-elsodany/rs-skills`). The catalog adds one place to add both.

**I already installed `rs-skills` from its own repository. Do I have a problem?** No, but avoid installing the same plugin from two marketplaces: you would get its commands twice. Keep whichever install you prefer and uninstall the other (`/plugin uninstall rs-skills@rs-skills`).

**Can I see what a plugin does before installing it?** Yes: every plugin in this catalog is open source in the repository linked above, and `/plugin` lists each plugin's skills, agents and hooks before and after installing.

## Maintaining the catalog

To add a plugin, add an object to `plugins` in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) with a `name` equal to the plugin's own manifest name, a `description`, and a `source` of the form `{"source": "github", "repo": "owner/repo"}`. Then:

```bash
python3 -I scripts/validate-catalog.py --self-test
python3 -I scripts/validate-catalog.py . --online     # also reads each plugin's own plugin.json and checks the name matches
claude plugin validate . --strict                      # the official validator (needs the Claude Code CLI)
```

CI runs the same checks on every push and once a week, so a renamed or removed plugin repository shows up as a failing build. Update `CHANGELOG.md` and `VERSION` (and the `version` in `marketplace.json`) for a user-visible change.

## Safety and privacy

- The catalog contains no plugin code and makes no network calls. `scripts/validate-catalog.py` only reads files here (and, with `--online`, each plugin's public `plugin.json`).
- Plugins can run commands and read files on your machine once installed: read a plugin's README and components first. Report problems with the catalog privately: see [SECURITY.md](SECURITY.md).

## Status and limits

- **Version 1.0.0**, single maintainer. Two plugins today.
- Verified: the catalog validates (`claude plugin validate --strict`), CI is green, and both plugins install from it in a clean Claude Code configuration. Not verified: other agents (a catalog entry is Claude Code only; each plugin's README says how to use its skills elsewhere).

## Licence

MIT: see [LICENSE](LICENSE). Each plugin carries its own licence in its repository.
