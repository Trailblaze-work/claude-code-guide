# Claude Code Tips & Best Practices

A concise, dark-themed PDF guide to getting the most out of [Claude Code](https://claude.ai/code). Updated daily by a GitHub Action that searches official sources for new features and best practices.

**[Download the PDF](Claude_Code_Tips_and_Best_Practices.pdf)**

## What's in the guide

- The 10 tips that matter most
- Plan Mode workflow
- Verification and feedback loops
- The CLAUDE.md system
- Context management
- Prompting techniques
- Parallel sessions, worktrees, and subagents
- Skills, hooks, and MCP
- Test-driven development with Claude
- Common pitfalls

## How it works

Content and rendering are separated so updates can be automated safely:

| File | Role |
|------|------|
| `content.yaml` | All guide content as structured YAML — the only file the daily job edits |
| `generate_guide.py` | PDF renderer. Reads YAML, produces the PDF. Never touched by automation |
| `validate_content.py` | Schema validation. Blocks malformed YAML before PDF generation |

A daily GitHub Action ([`.github/workflows/update-guide.yml`](.github/workflows/update-guide.yml)):
1. Runs Claude Code CLI with web search to check official sources for updates
2. Claude edits `content.yaml` only (restricted to `Read`, `Edit`, `WebSearch`, `WebFetch`)
3. `validate_content.py` catches any structural errors
4. If content changed, regenerates the PDF and commits

Most runs change nothing — the [prompt](.github/prompts/update-guide-prompt.md) sets a high bar so the guide stays concise.

## Local development

```bash
pip install -r requirements.txt
python validate_content.py   # check YAML structure
python generate_guide.py     # produce PDF
```

## Sources

- [Official docs](https://code.claude.com/docs)
- [Anthropic engineering blog](https://anthropic.com/engineering)
- Boris Cherny ([@bcherny](https://x.com/bcherny)) — Claude Code creator
- [Claude Code best practices](https://anthropic.com/engineering/claude-code-best-practices)

---

Built by [Trailblaze](https://trailblaze.work)
