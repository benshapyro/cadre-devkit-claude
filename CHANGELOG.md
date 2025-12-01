# Changelog

All notable changes to cadre-devkit-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
