You are checking whether a Claude Code best practices guide needs updating.
Your ONLY job is to edit `content.yaml` — do NOT touch any other file.

## CRITICAL: Most runs should change NOTHING

This job runs daily. The guide should only change when something genuinely
important happens — a new major feature, a breaking change, or a deprecation.
Making no changes is the EXPECTED outcome for most runs — but when a major
release or new feature drops, update immediately.

Do NOT add content just because you found it. Do NOT tweak existing wording
to add details, examples, or minor clarifications — the current phrasing is
intentional. Do NOT expand existing bullet points or descriptions. Ask yourself:
- "Is this a COMPLETELY NEW feature or command that the guide doesn't mention at all?"
- "Is something in the guide now WRONG because of a breaking change?"
- "If I do nothing, will users be misled or miss something critical?"

If ANY answer is "no", make NO edits and print:
"No significant updates found. Guide is current."

## Quality over quantity

This is a concise tips guide, not a reference manual. The official docs exist
for exhaustive coverage. Only add something if it belongs in a "top tips" guide
that someone reads in 15 minutes. One strong bullet point is better than five
weak ones. If adding something new, consider whether an existing item should be
consolidated or removed to keep the guide tight.

DO NOT make the guide longer overall. If you add a bullet, remove a weaker one.
The guide's current length is the target — not a floor to build on.

## Sources to search (in priority order)

1. https://code.claude.com/docs — official docs, changelog
2. https://anthropic.com/engineering — blog posts about Claude Code
3. @bcherny (Boris Cherny) on X — Claude Code creator
4. @alexalbert__ (Alex Albert) on X — Anthropic
5. @amanrsanger (Aman Sanger) on X — Claude Code team
6. @sdtuck (Sam Tuck) on X — Claude Code team
7. x.com/bcherny/status/2007179832300581177 (setup thread)
8. x.com/bcherny/status/2017742741636321619 (team tips thread)

## What qualifies as an update

YES — add or update for:
- New major features (new mode, new command category)
- Breaking changes or deprecations
- Changed behavior that contradicts current guide content
- A best practice endorsed by Anthropic staff that isn't covered

NO — do not add or change:
- Minor flag additions or options
- Implementation details already covered at the right level
- Content that restates what's already in the guide differently
- Experimental features behind flags (unless widely adopted)
- Anything that makes the guide longer without making it better
- Tweaks, rewording, or expansions to existing content
- Extra details or aliases appended to existing descriptions

## Rules

1. Read `content.yaml` first to understand what's already covered.
2. Search the sources above for genuinely NEW information.
3. If you find something that clears the bar above:
   - Add it to the appropriate existing section in `content.yaml`
   - Use only these element types: body, bullet, code, tip, subsection, heading, quote, prompts
   - For tips_list sections: each tip needs num, title, desc, ref
   - For pitfalls_list sections: each pitfall needs title, problem, fix
   - If adding a new source, append to the `sources` list
   - Keep additions minimal — one bullet or tip, not a whole subsection
4. If you find something outdated or no longer accurate:
   - Remove or update it in `content.yaml`
   - Keeping the guide accurate is more important than preserving old content
5. If nothing clears the bar, make NO changes. This is the right outcome.
6. Print a brief summary: what you searched, what you found, why you did or didn't make changes.
