import sublime

OVERRIDES = "PlatformOverrides.sublime-settings"
PREFERENCES = "Preferences.sublime-settings"

def apply_overrides():
    overrides = sublime.load_settings(OVERRIDES)
    prefs = sublime.load_settings(PREFERENCES)
    for key, value in (overrides.get(sublime.platform()) or {}).items():
        prefs.set(key, value)
    # NOTE: deliberately NO sublime.save_settings() here.

def plugin_loaded():
    apply_overrides()
    # Optional: re-apply live when you edit the overrides file, no restart needed.
    sublime.load_settings(OVERRIDES).add_on_change("platform_overrides", apply_overrides)