import sublime_plugin, os

# Remove the .- files when saving
# In MacOS 13.2, the com.apple.provenance extended attribute is always set
class RemoveMacAttr(sublime_plugin.EventListener):
    def on_post_save(self, view):
        (path,name) = os.path.split(view.file_name())
        attrname = "._" + name
        attrpath = os.path.join(path, attrname)
        if os.path.exists(attrpath):
            os.remove(attrpath)
