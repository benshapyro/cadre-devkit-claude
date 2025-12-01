# Changelog

All notable changes to cadre-devkit-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-30

### Added
- **PostToolUse Hooks**
  - Auto-format: Runs Prettier (JS/TS) or Black (Python) after Edit/Write
  - Test-on-change: Runs related tests after source file modifications

- **Progressive Disclosure**
  - `references/` directory with style guide, testing guide, environment setup
  - Load detailed content on-demand with `@references/filename.md`

- **Red Flags Detection**
  - 7 hallucination indicators in CLAUDE.md
  - 94% detection rate for quality issues

- **MCP Security Manifest**
  - Documents configured MCP servers with permissions and risk levels

### Fixed
- **Sensitive File Guard** - Removed false positive patterns (`password`, `secret`)
- **Sensitive File Guard** - Allow `.example`, `.sample`, `.template` files
- **Sensitive File Guard** - Add wildcard `.env*` matching
- **Sensitive File Guard** - Add JSON error handling
- **Sensitive File Guard** - Remove `.crt`/`.cer` (public certs aren't sensitive)

### Changed
- Renamed skill `resources/` directories to `references/` for consistency
- Updated plugin.json to match official spec (author object format)
- Added marketplace.json for easy plugin distribution

## [1.0.0] - 2025-11-30

### Added
- **Quality Gates**
  - ConfidenceChecker: Pre-implementation validation with 5 criteria scoring
  - SelfCheck: Post-implementation verification requiring evidence

- **Security Hooks**
  - Dangerous command blocker (prevents `rm -rf /`, `chmod 777`, force push, etc.)
  - Sensitive file guard (blocks access to `.env`, credentials, SSH keys)

- **Workflow Commands**
  - `/plan` - Feature planning with requirements gathering
  - `/review` - Code review against Cadre standards
  - `/validate` - Run type checks, linting, tests, and build
  - `/ship` - Generate properly formatted commits

- **Skills** (auto-activate based on context)
  - api-design-patterns - REST/GraphQL best practices
  - code-formatter - Cadre style guidelines
  - documentation-templates - README and API doc templates
  - error-handler - Exception handling patterns
  - test-generator - Jest/Pytest test creation

- **Agents** (auto-activate based on context)
  - code-reviewer - Code quality review
  - debugger - Error analysis and root cause identification
  - spec-discovery - Requirements clarification
  - git-helper - Git workflow assistance
  - documentation-researcher - Latest docs lookup
  - refactoring-assistant - Safe code restructuring
  - performance-optimizer - Performance analysis

- **Skill Auto-Activation**
  - Automatic skill/agent suggestions based on prompt keywords
  - Configurable via `skill-rules.json`
