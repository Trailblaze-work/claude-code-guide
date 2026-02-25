You are updating a Claude Code best practices guide. Your ONLY job is to
edit `content.yaml` if you find relevant new information. Do NOT touch any
other file.

## Sources to search (in priority order)

1. https://code.claude.com/docs — official docs, changelog
2. https://anthropic.com/engineering — blog posts about Claude Code
3. @bcherny (Boris Cherny) on X — Claude Code creator
4. @alexalbert__ (Alex Albert) on X — Anthropic
5. @amanrsanger (Aman Sanger) on X — Claude Code team
6. @sdtuck (Sam Tuck) on X — Claude Code team
7. x.com/bcherny/status/2007179832300581177 (setup thread)
8. x.com/bcherny/status/2017742741636321619 (team tips thread)

## What to look for

- New CLI flags, commands, or modes
- New or changed CLAUDE.md / hooks / skills / MCP behavior
- Breaking changes or deprecations
- Significant new best practices from Anthropic staff

## Rules

1. Read `content.yaml` first to understand what's already covered.
2. Search the sources above for NEW information.
3. If you find something new:
   - Add it to the appropriate existing section in `content.yaml`
   - Use only these element types: body, bullet, code, tip, subsection, heading, quote, prompts
   - For tips_list sections: each tip needs num, title, desc, ref
   - For pitfalls_list sections: each pitfall needs title, problem, fix
   - If adding a new source, append to the `sources` list
4. If you find something that is outdated or no longer accurate:
   - Remove or update it in `content.yaml`
   - Keeping the guide accurate is more important than preserving old content
5. If nothing new is found, make NO changes.
6. Print a summary of findings.
