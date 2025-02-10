"""
Utility Class that feature a context manager for temporary directory
"""

import os
import pathlib
import shutil
import stat
import tempfile


class TempDir:
    """
    Utility Class that feature a context manager for temporary directory
    """

    def __init__(self, remove_on_exit: bool = True) -> None:
        """
        @param remove_on_exit: If the directory will be remove when getting out
            of the context manager
        """
        self._path = None
        self._remove = remove_on_exit

        self.current_dir = pathlib.Path.cwd()

    def __enter__(self):
        self._path = pathlib.Path(tempfile.mkdtemp())
        if not self._path.exists():
            raise FileExistsError()
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if pathlib.Path.cwd() != self.current_dir:
            os.chdir(self.current_dir)

        if self._remove and self._path.exists():
            shutil.rmtree(self._path, onerror=self._remove_readonly)

        if self._remove and self._path.exists():
            raise FileExistsError(f'The tempory file: "{self._path}" was not properly remove')

        if not pathlib.Path.cwd().exists():
            raise FileExistsError()

    def _remove_readonly(self, func, path, _):
        pathlib.Path.chmod(path, stat.S_IWRITE)
        func(path)

    @property
    def path(self):
        return self._path

    def join(self, *path: str):
        """
        Join to the temporary directory path.
        @param path: The paths to join

        @return : The joint directory path
        """
        return pathlib.Path(self._path, *path)
