import sublime_plugin, os


class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save(self, view):
        home = os.path.expanduser("~")
        remote = home + '/remote/'

        filename = view.file_name()
        if filename.startswith(remote):
            host = filename[len(remote):].split('/')[0]
            remote_host = remote + host
            dest = filename[len(remote_host):]
            target = "/usr/bin/scp '{0}' {1}:'{2}'".format(filename, host, dest)
            print(target)
            os.system(target + " &")
