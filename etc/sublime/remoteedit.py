import sublime_plugin, os, sys

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
            remote.rsync(filename, dst)
