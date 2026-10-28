#!/bin/sh
# Run iTerm2 hooks only inside iTerm2 on macOS; otherwise no-op
[ "$(uname)" = Darwin ] || exit 0
[ "$TERM_PROGRAM" = "iTerm.app" ] || [ "$LC_TERMINAL" = "iTerm2" ] || exit 0
exec "$@"
