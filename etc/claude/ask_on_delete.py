#!/usr/bin/env python3
"""PreToolUse hook: prompt before Bash commands that delete files, edit them in
place (sed -i), or run git commit / git push. Exempt simple rm-family deletions
confined to /tmp or tmp/. Stay silent on everything else so the auto-mode
classifier still decides."""
import json
import re
import shlex
import sys

SIMPLE_DELETE_CMDS = {"rm", "rmdir", "unlink", "shred", "srm", "wipe", "truncate", "trash"}
OPERATORS = {"&&", "||", "|", "|&", "&", ";"}
SED_ARG_TAKING = {"-e", "-f", "-l"}
GIT_ARG_TAKING = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
GIT_ASK_SUBCMDS = {"commit", "push"}

COMPLEX_DELETE_RE = re.compile(
    r"(?:^|[;&|]|\s)git\s+(?:rm|clean)(?:\s|$)|gio\s+trash|find\s+.*-delete|-exec\s+rm"
)
ANY_DELETE_RE = re.compile(
    r"(?:^|[;&|]|\s)(?:\S*/)?(?:rm|rmdir|unlink|shred|srm|wipe|truncate|trash)(?:\s|$)"
    r"|" + COMPLEX_DELETE_RE.pattern
)


def _is_tmp(path):
    p = path.strip().strip('"').strip("'")
    return p in ("/tmp", "tmp") or p.startswith(("/tmp/", "tmp/", "./tmp/"))


def _all_rm_targets_in_tmp(tokens):
    i, saw_delete = 0, False
    while i < len(tokens):
        if tokens[i].rsplit("/", 1)[-1] in SIMPLE_DELETE_CMDS:
            saw_delete = True
            targets, j = [], i + 1
            while j < len(tokens) and tokens[j] not in OPERATORS:
                if not tokens[j].startswith("-"):
                    targets.append(tokens[j])
                j += 1
            if not targets or not all(_is_tmp(t) for t in targets):
                return False
            i = j
        else:
            i += 1
    return saw_delete


def _has_sed_inplace(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i].rsplit("/", 1)[-1] == "sed":
            j = i + 1
            while j < len(tokens) and tokens[j] not in OPERATORS:
                opt = tokens[j]
                if opt == "--":
                    break
                if opt.startswith("--"):
                    if opt == "--in-place" or opt.startswith("--in-place="):
                        return True
                elif opt.startswith("-") and len(opt) > 1:
                    cluster = opt[1:]
                    pre_i = cluster.split("i", 1)[0]
                    if "i" in cluster and "e" not in pre_i and "f" not in pre_i:
                        return True
                    if opt in SED_ARG_TAKING:
                        j += 1
                j += 1
            i = j
        else:
            i += 1
    return False


def _has_git_ask(tokens):
    """True if any git invocation's subcommand is commit or push."""
    i, n = 0, len(tokens)
    while i < n:
        if tokens[i].rsplit("/", 1)[-1] == "git":
            j = i + 1
            while j < n and tokens[j] not in OPERATORS:
                t = tokens[j]
                if t.startswith("-"):
                    j += 2 if t in GIT_ARG_TAKING else 1
                    continue
                if t in GIT_ASK_SUBCMDS:   # first non-option token = subcommand
                    return True
                break
            i = j + 1
        else:
            i += 1
    return False


def main():
    try:
        command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError, ValueError):
        command = ""
    if not command:
        sys.exit(0)

    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        tokens = []

    sed_inplace = _has_sed_inplace(tokens)
    git_ask = _has_git_ask(tokens)
    has_delete = bool(ANY_DELETE_RE.search(command))

    if not sed_inplace and not git_ask and not has_delete:
        sys.exit(0)  # nothing of interest -> defer to the classifier

    tmp_exempt = (
        has_delete and not sed_inplace and not git_ask
        and not COMPLEX_DELETE_RE.search(command)
        and bool(tokens) and _all_rm_targets_in_tmp(tokens)
    )

    if tmp_exempt:
        decision, reason = "allow", "Deletion confined to /tmp or tmp/ — auto-approved."
    else:
        decision = "ask"
        parts = []
        if git_ask:
            parts.append("runs git commit/push")
        if sed_inplace:
            parts.append("edits files in place (sed -i)")
        if has_delete:
            parts.append("can delete files")
        reason = "Confirm before running: this command " + " and ".join(parts) + "."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
