import sublime, os
from LSP.plugin import AbstractPlugin


class ClangdPlugin(AbstractPlugin):

    @classmethod
    def name(cls) -> str:
        return "clangd-plugin"

    @classmethod
    def basedir(cls) -> str:
        # Do everything relative to this directory
        return os.path.join(cls.storage_path(), cls.name())