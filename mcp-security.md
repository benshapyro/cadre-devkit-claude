# MCP Security Manifest

**Last Updated:** November 30, 2025
**Review Schedule:** Monthly

## Configured MCP Servers

| Server | Purpose | Permissions | Risk Level |
|--------|---------|-------------|------------|
| **Sequential Thinking** | Structured problem-solving and reasoning workflows | Read-only analysis | Low |
| **Exa Search** | Web search and research | External API access | Low |
| **Ref Documentation** | Framework/library documentation lookup | External web read access | Low |
| **Playwright** | Browser automation and testing | File system read + external web access | Medium |

## Permission Details

### Sequential Thinking (`mcp__sequential-thinking`)
- **Tools:** `sequentialthinking`
- **Data Access:** None (pure reasoning)
- **Network Access:** None
- **Risk Assessment:** Low - no external access, stateless reasoning

### Exa Search (`mcp__exa`)
- **Tools:** `exa_search`
- **Data Access:** None
- **Network Access:** External API (exa.ai)
- **Risk Assessment:** Low - read-only web search, no data persistence

### Ref Documentation (`mcp__Ref`)
- **Tools:** `ref_search_documentation`, `ref_read_url`
- **Data Access:** None
- **Network Access:** External documentation sites
- **Risk Assessment:** Low - read-only access to public documentation

### Playwright (`mcp__playwright`)
- **Tools:** Browser navigation, clicks, form filling, screenshots
- **Data Access:** Read files for upload
- **Network Access:** External web access (browser)
- **Risk Assessment:** Medium - can interact with external websites

## Security Policies

### Adding New Servers

Before adding a new MCP server:
1. Document purpose and use case
2. Review permissions and network access
3. Assess risk level (Low/Medium/High)
4. Add to this manifest

### Access Control

- No MCP server has write access to sensitive directories
- No MCP server can execute arbitrary shell commands
- Network access limited to documented purposes

### Monitoring

- Review MCP server usage in Claude Code logs
- Check for unusual network activity
- Validate server behavior matches documentation

## Risk Levels Defined

| Level | Definition | Examples |
|-------|------------|----------|
| **Low** | Read-only, no external network, or public data only | Sequential Thinking, Exa Search |
| **Medium** | External network with controlled scope | Playwright, GitHub API |
| **High** | Write access, credentials, or broad permissions | Database, cloud infrastructure |

## Incident Response

If a security concern is identified:
1. Disable the affected MCP server immediately
2. Review recent usage in Claude Code logs
3. Document the issue
4. Report to appropriate channels

---

*This manifest should be reviewed monthly and updated when MCP servers are added or removed.*
