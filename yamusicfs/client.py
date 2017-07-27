from math import ceil
import hashlib
import time
import logging

import requests


class YandexMusic(requests.Session):
    log = logging.getLogger("yamusicfs.client")

    def __init__(self):
        super().__init__()
        self.base_url = "https://music.yandex.ru"
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            # "Cookie": ...,  # TODO?
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "X-Retpath-Y": "https://music.yandex.ru/",
        })

    def request(self, *a, **kw):
        r = super().request(*a, **kw)
        self.log.debug("%d %s", r.status_code, r.url)
        return r

    def search(self, text, type="tracks", page=0):
        return self.get(self.base_url + "/handlers/music-search.jsx", params={
            "text": text,
            "type": type,
            "page": str(page),
        })

    def get_track(self, track):
        return self.get(self.base_url + "/handlers/track.jsx", params={
            "track": str(track),
        })

    def get_artist(self, artist_id):
        return self.get(self.base_url + "/handlers/artist.jsx", params={
            "artist": artist_id,
        })

    def get_artist_tracks(self, artist_id):
        return self.get(self.base_url + "/handlers/artist.jsx", params={
            "artist": str(artist_id),
            "what": "tracks",
        })

    def get_album(self, album_id):
        return self.get(self.base_url + "/handlers/album.jsx", params={
            "album": str(album_id),
        })

    def get_playlist(self, owner, playlist_id):
        return self.get(self.base_url + "/handlers/playlist.jsx", params={
            "owner": str(owner),
            "kinds": playlist_id,
        })

    def get_download_link(self, track):
        if type(track) is int:
            track = self.get_track(track).json()
        elif hasattr(track, "json"):
            track = track.json()

        url = "{}/api/v2.1/handlers/track/{}/track/download/m".format(
            self.base_url,
            track["track"]["id"]
        )
        r1 = self.get(url, params={"hq": 1})
        src = r1.json()["src"]

        r2 = self.get(src + "&format=json")
        storage_info = r2.json()

        salt = "XGRlBW9FXlekgbPrRHuSiA" + storage_info["path"][1:] + storage_info["s"]
        h = hashlib.md5()
        h.update(salt.encode())

        src_url = "https://{host}/get-mp3/{h}/{ts}{path}?track-id={id}".format(
            host=storage_info["host"],
            h=h.hexdigest(),
            ts=storage_info["ts"],
            path=storage_info["path"],
            id=track["track"]["id"]
        )

        return src_url
