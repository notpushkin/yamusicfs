from defuse.fs import DefuseFS
from defuse.nodes import Directory

from .nodes import YMFileProxy
from .client import YandexMusic

ym = YandexMusic()

root = Directory({
    "playlists": Directory({}),
    "searches": Directory({}),
    "tracks": Directory({
        "dope_shit.mp3": YMFileProxy(ym, ym.get_track(30934223).json())
    }),
})

fs = DefuseFS("yamusicfs-fuse", root)
