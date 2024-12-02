import sublime, sublime_plugin, os, sys

__dotfiles__ = os.path.normpath(os.path.join(os.path.realpath(__file__), '..', '..', '..'))
sys.path.append(os.path.join(__dotfiles__, 'py'))
import remote


class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename = view.file_name()
        host = remote.get_remote_host(filename)
        print(filename, host)
        if remote.needs_sync(host):
            remote_path = remote.get_remote_path(host, filename)
            dst = '{}:{}'.format(host, remote_path)
            sublime.set_timeout_async(lambda: remote.rsync(filename, dst, show=True), 0)

class RemotePullCommand(sublime_plugin.WindowCommand):
    def run(self):
        dirname = self.window.folders()[0]
        sublime.set_timeout_async(lambda: remote.pull([dirname]), 0)

class RemotePushCommand(sublime_plugin.WindowCommand):
    def run(self):
        dirname = self.window.folders()[0]
        sublime.set_timeout_async(lambda: remote.push([dirname]), 0)
