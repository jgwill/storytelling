# MCP Module Release Guide

This document outlines the release and deployment procedures for the Storytelling MCP (Model Context Protocol) Server module.

## Release Strategy

The MCP module follows semantic versioning aligned with the main `storytelling` package but maintains its own release cycle for stability. MCP updates are released when:

1. **New tools or resources** are added
2. **Tool signatures** change or improve
3. **Critical bugs** are fixed
4. **Integration enhancements** improve AI agent capabilities

## Pre-Release Checklist

### Code Quality

```bash
# Run tests
make test-mcp

# Check linting
make lint

# Type checking
mypy mcp/

# Format check
black --check mcp/
```

### Documentation

- [ ] Update `mcp/README.md` with new tools/resources
- [ ] Add examples for new functionality
- [ ] Update troubleshooting section if needed
- [ ] Verify all tool descriptions are clear and complete

### Integration Testing

```bash
# Test tool availability
python -m mcp.server --test-tools

# Test with Claude Desktop (if setup)
# Verify tools appear in assistant context
```

## Release Workflow

### 1. Version Bump

MCP module version format: `mcp-{major}.{minor}.{patch}`

Update in relevant files:
- `pyproject.toml` - Add version note in changelog or extra field
- `mcp/README.md` - Update any version-specific instructions

### 2. Create Release Branch

```bash
git checkout -b release/mcp-x.y.z
```

### 3. Update Changelog

Add to `CHANGELOG.md` under MCP section:

```markdown
## MCP [version]

### Added
- New tool: tool_name - brief description

### Changed
- Modified tool_name signature
- Updated resource documentation

### Fixed
- Fixed bug in tool_x

### Breaking Changes
- List any breaking changes with migration path
```

### 4. Tag Release

```bash
git tag -a mcp-x.y.z -m "Release MCP version x.y.z"
git push origin release/mcp-x.y.z --tags
```

### 5. Create Pull Request

Create PR with:
- Title: `Release: MCP vx.y.z`
- Description: Link to CHANGELOG entries
- Testing: Attach test results
- Reviewers: Request code review

### 6. Merge & Deploy

After approval:

```bash
git checkout main
git merge --no-ff release/mcp-x.y.z
git push origin main
```

## Deployment

### Docker (if applicable)

```bash
# Build MCP server image
docker build -f mcp/Dockerfile -t storytelling-mcp:x.y.z .

# Tag and push
docker tag storytelling-mcp:x.y.z registry.example.com/storytelling-mcp:x.y.z
docker push registry.example.com/storytelling-mcp:x.y.z
```

### PyPI Package

The MCP module is distributed as part of the main `storytelling` package under the `mcp` optional dependency.

No separate PyPI release needed—updates go out with main package releases.

### Direct Installation

Users install latest MCP tools via:

```bash
pip install storytelling[mcp]
# or for all features
pip install storytelling[all]
```

## Integration Points for LLM Platforms

### Claude Desktop

After release, users configure via:

```json
{
  "mcpServers": {
    "storytelling": {
      "command": "python",
      "args": ["-m", "storytelling.mcp"]
    }
  }
}
```

**No deployment action required** - users control when they update.

### GitHub Copilot

GitHub Copilot pulls from system `storytelling` installation. Deployment via:

```bash
# User runs (automatic in many setups)
pip install --upgrade storytelling
```

### OpenAI ChatGPT / Custom Integrations

For third-party integrations, provide:
- MCP server URL (if self-hosted)
- Tool specifications (auto-generated from `server.py`)
- Authentication requirements
- Model URI examples

## Versioning Policy

### Semantic Versioning

- **MAJOR**: Breaking changes to tool signatures or resource URIs
- **MINOR**: New tools, new resources, non-breaking enhancements
- **PATCH**: Bug fixes, documentation improvements, internal refactoring

### Compatibility Matrix

| Storytelling Version | MCP Version | Status        |
|----------------------|-------------|---------------|
| 0.2.x                | mcp-1.0.x   | Current       |
| 0.2.6+               | mcp-1.1.x   | Latest        |
| 0.3.x (planned)      | mcp-2.0.x   | Future        |

## Tool Stability Guarantees

### Stable (Supported)

These tools maintain backward compatibility:
- `generate_story` - Core generation workflow
- `list_sessions` - Session enumeration
- `resume_session` - Session continuation
- `validate_model_uri` - Model URI validation

### Experimental (May change)

New tools marked experimental in documentation may change:
- Signature updates
- Behavior refinements
- Deprecation in next MAJOR version

### Deprecated (Will be removed)

Deprecated tools continue working but are not recommended:
- **Removal target**: Set 2-3 releases in advance
- **Alternative**: Always provide replacement before deprecation

## Rollback Procedure

If a release has critical issues:

```bash
# Identify problematic version
git tag -l | grep mcp-

# Revert in main
git revert <commit-hash>

# Create patch hotfix
git checkout -b hotfix/mcp-x.y.z-critical

# Make minimal fix and retag
git tag -a mcp-x.y.z-hotfix -m "Hotfix for critical issue"
```

Communicate to users:
- Post notice on project channels
- Document workaround if available
- Provide timeline for fixed version

## Monitoring Post-Release

### Success Metrics

- Tool availability confirmed by integrating platforms
- No spike in error reports
- User feedback positive
- Documentation clear and complete

### Ongoing Support

- Monitor issue tracker for MCP-related bugs
- Respond to integration questions
- Gather feature requests for next version
- Maintain this guide with lessons learned

## Next Release Checklist Template

```markdown
## MCP Release [X.Y.Z] Preparation

**Target Date**: [DATE]

### Code Changes
- [ ] All PRs merged to development branch
- [ ] Tests passing (make test-mcp)
- [ ] Linting clean (make lint)

### Documentation
- [ ] README.md updated with changes
- [ ] Examples added/updated
- [ ] Troubleshooting expanded if needed

### Testing
- [ ] Integration testing complete
- [ ] Claude Desktop testing (if applicable)
- [ ] Regression testing on previous scenarios

### Release
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Release branch created
- [ ] Tag created and pushed
- [ ] PR created and merged
```

## Contact & Support

For questions about MCP releases:
- Check this guide first
- Review `mcp/README.md` for user-facing docs
- File issues on GitHub for bugs
- Discuss feature requests in project discussions

## Related Documentation

- [`mcp/README.md`](./README.md) - User guide
- [`../README.md`](../README.md) - Main project
- [`../CHANGELOG.md`](../CHANGELOG.md) - Project changelog
- [`../pyproject.toml`](../pyproject.toml) - Package config
