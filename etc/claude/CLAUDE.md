# File editing

- Prefer the Edit tool (or Write for new files) over `sed -i` or other in-place shell edits. Use the shell to search or read files if needed, but make changes with Edit so they are exact and reviewable.

# Writing style

- Use plain, literal language. Avoid figurative jargon borrowed from other fields:
  "load-bearing", "doing a lot of work", "heavy lifting", "north star",
  "unlock", "lean into", "surface" (as a verb), "delve".
- Exception: use these words literally when the topic is actually about
  structures or engineering.
- Instead, say what you mean directly: "important", "essential",
  "the main reason", "this depends on X".

# Code comments

Default to no comments. Clear names and structure should explain the
code; every comment is one more thing to maintain.

Comment only when a reader would likely misunderstand or break the code
without it: a non-obvious reason, a workaround, a subtle invariant or
edge case. Keep it to a line or two.

Don't add:
- comments that restate the code or names
- section headers or step-by-step narration inside functions
- doc comments on private or self-explanatory functions
- notes about the change, removed code, or the current task

Don't add comments to code you aren't otherwise changing. Before
finishing, delete any comment in your diff that doesn't meet this bar.
