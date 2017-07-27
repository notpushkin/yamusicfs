import requests
from requests import Request, Session
from defuse.nodes import FileProxy


class YMFileProxy(FileProxy):
    def __init__(self, ym, track):
        self.track = track
        self.size = int(192 * 1.28 * track["track"]["durationMs"])
        # XXX: ???
        self.ym = ym
        self.fp = None

    def open(self, fh=None):
        r = self.ym.get(self.ym.get_download_link(self.track), stream=True)
        self.fp = r.raw
        return 0

    def read(self, size, offset, fh=None):
        if self.fp is None:
            self.open()

        return super().read(size, offset, fh=None)
