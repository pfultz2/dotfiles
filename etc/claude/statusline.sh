#!/usr/bin/env bash
# Claude Code status line: model, effort, context window, weekly and Fable weekly usage, PR number.
# Reads the status line JSON from stdin.

input=$(cat)

mapfile -t fields < <(jq -r '
    def pct: if . == null then "" else (. + 0.5 | floor | tostring) end;
    .model.display_name // "",
    .effort.level // "",
    (.context_window.used_percentage | pct),
    (.rate_limits.seven_day.used_percentage | pct),
    (.rate_limits.seven_day != null),
    (.pr.number // "" | tostring),
    .pr.kind // ""
' <<<"$input")
model=${fields[0]}
effort=${fields[1]}
ctx=${fields[2]}
week=${fields[3]}
subscription=${fields[4]}
pr=${fields[5]}
pr_kind=${fields[6]}

# Claude Code does not pass the Fable weekly usage to the status line, so it is
# read from the claude.ai usage endpoint that /usage uses. The endpoint is
# undocumented. Fetches run in the background at most every $refresh seconds.
# Only sessions that report a weekly window are on a claude.ai subscription; a
# gateway or API key session can still have a claude.ai token in $creds, which
# would show another account's usage.
creds=${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.credentials.json
cache_dir=${XDG_CACHE_HOME:-$HOME/.cache}/claude-statusline
fable_cache=$cache_dir/fable.json
fable_stamp=$cache_dir/fable.stamp
refresh=300
now=$(date +%s)

# fetch_fable: cache the Fable weekly row as {"percent": N, "resets_at": epoch}.
# Only the access token is used; refreshing it is left to Claude Code.
fetch_fable() (
    set -o pipefail
    jq -e --argjson now "$(( now * 1000 ))" '.claudeAiOauth.expiresAt > $now' "$creds" >/dev/null || exit
    tmp=$(mktemp "$fable_cache.XXXXXX") || exit
    if jq -r '"Authorization: Bearer " + .claudeAiOauth.accessToken' "$creds" \
        | curl -sf --max-time 10 -H @- -H 'anthropic-beta: oauth-2025-04-20' \
            https://api.anthropic.com/api/oauth/usage \
        | jq '[.limits[]? | select(.kind == "weekly_scoped" and .scope.model.display_name == "Fable")][0] // {}
              | {percent, resets_at: (.resets_at | try (sub("\\.[0-9]+"; "") | sub("\\+00:00$"; "Z") | fromdateiso8601) catch null)}' \
            > "$tmp"; then
        mv "$tmp" "$fable_cache"
    else
        rm -f "$tmp"
    fi
)

fable=
if [ "$subscription" = true ] && [ -r "$creds" ] && command -v curl >/dev/null; then
    mkdir -p "$cache_dir"
    last=0
    [ -r "$fable_stamp" ] && read -r last < "$fable_stamp"
    [[ $last =~ ^[0-9]+$ ]] || last=0
    if (( now - last >= refresh )); then
        echo "$now" > "$fable_stamp"
        fetch_fable </dev/null >/dev/null 2>&1 &
    fi
    # Hide a cached value once its week has reset.
    fable=$(jq -r --argjson now "$now" '
        select(.percent != null and (.resets_at == null or .resets_at > $now))
        | .percent + 0.5 | floor
    ' "$fable_cache" 2>/dev/null)
fi

sep=$'\033[90m │ \033[0m'

# bar <label> <percent>: a 10-cell bar, green below 50%, yellow below 80%, red from 80%.
bar() {
    local label=$1 pct=$2 width=10 filled color i
    local cells=$pct
    (( cells > 100 )) && cells=100
    filled=$(( (cells * width + 50) / 100 ))
    if (( pct >= 80 )); then
        color=31
    elif (( pct >= 50 )); then
        color=33
    else
        color=32
    fi
    printf '%s \033[%sm' "$label" "$color"
    for (( i = 0; i < filled; i++ )); do printf '█'; done
    printf '\033[90m'
    for (( i = filled; i < width; i++ )); do printf '░'; done
    printf '\033[0m %d%%' "$pct"
}

out=$'\033[1m'"$model"$'\033[0m'
[ -n "$effort" ] && out+=" ($effort)"
[ -n "$ctx" ] && out+="$sep$(bar ctx "$ctx")"
[ -n "$week" ] && out+="$sep$(bar week "$week")"
[ -n "$fable" ] && out+="$sep$(bar fable "$fable")"
if [ -n "$pr" ]; then
    if [ "$pr_kind" = mr ]; then out+="$sep!$pr"; else out+="$sep#$pr"; fi
fi
printf '%s' "$out"
