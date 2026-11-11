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

- Write concise, direct comments. Explain why the code does something or
  note behavior that isn't clear from reading it.
- Don't state the obvious: no comments that restate the code, the
  function name, or the variable name (e.g. `// increment i` above `i++`).
- Leave out unrelated information, such as the history of a change,
  references to the current task or conversation, or notes about code
  that was removed.
