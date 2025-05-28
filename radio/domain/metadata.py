import ast
import json
import re
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Tuple

import requests
from django.conf import settings

from radio.models import Radio


@dataclass
class Track:
    title: str
    album_title: str
    cover: str
    artist_name: str


@dataclass
class RadioMedata:
    id: int
    user_id: int
    title: str
    album_title: str
    cover: str
    artist_name: str
    radio_flux: str
    song_history: List[Dict[str, str]] = field(default_factory=lambda: [])

    def __get_image_track(title: str) -> Tuple[str, str]:
        req = (
            requests.get(url=settings.COVER_ENDPOINT, params={"term": title})
            .json()
            .get("results")
        )
        return req[0].get("artworkUrl100"), req[0].get("collectionName")

    @classmethod
    @staticmethod
    def from_cls_to_dict(cls) -> Dict:
        return json.dumps(asdict(cls))

    @staticmethod
    def is_uri_available(url: str | None) -> bool:
        try:
            req = requests.get(url)
            req.raise_for_status()
            return True
        except requests.exceptions.RequestException as ex:
            return False

    @classmethod
    def make_requests(cls, radio: Radio) -> "RadioMedata" | Dict[str, str]:
        song_list_history = []
        server_type = radio.server_type
        api_currrent_song, api_history_song = (
            radio.url_api_radio_current_song,
            radio.url_api_radio_history,
        )
        if not RadioMedata.is_uri_available(
            api_currrent_song
        ) or not RadioMedata.is_uri_available(api_history_song):
            return {
                "detail": f"{api_currrent_song} or {api_history_song} is not available, check your api before"
            }
        else:
            match server_type:
                case "shoutcast":
                    current_title = requests.get(radio.url_api_radio_current_song).text
                    cover, album = RadioMedata.__get_image_track(current_title)
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title=current_title.split("-")[1].strip(),
                        album_title=album,
                        cover=cover,
                        artist_name=current_title.split("-")[0].strip(),
                    )
                case "icecast":
                    current_title = (
                        requests.get(radio.url_api_radio_current_song)
                        .json()
                        .get("icestats")
                    )
                    song = current_title.get("source", None)
                    if song is not None:
                        song = current_title.get("source").get("title").split("-")
                        cover, album = RadioMedata.__get_image_track(song[1])
                        return RadioMedata(
                            id=radio.pk,
                            user_id=radio.user.id,
                            radio_flux=radio.url_flux_radio,
                            title=song[1],
                            album_title=album,
                            cover=cover,
                            artist_name=song[0],
                        )
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title="",
                        album_title="",
                        cover=str(radio.radio_image_icon.url),
                        artist_name="",
                    )
                case "everestpanel":
                    current_song = requests.get(radio.url_api_radio_current_song).json()
                    history = (
                        requests.get(radio.url_api_radio_history)
                        .json()
                        .get("past_tracks", [])[0:5]
                    )
                    for track in history:
                        match = re.match(r"\d+,(.+)", track)
                        if match:
                            value = match.group(1).split("-")
                            track = Track(
                                title=value[0],
                                album_title="",
                                cover=RadioMedata.__get_image_track(value[0])[0],
                                artist_name=value[1],
                            )
                            song_list_history.append(
                                ast.literal_eval(RadioMedata.from_cls_to_dict(track))
                            )
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title=current_song.get("current_track").get("name"),
                        album_title=current_song.get("current_track").get("album"),
                        cover=current_song.get("current_track").get("image"),
                        artist_name=current_song.get("current_track").get("artist"),
                        song_history=song_list_history,
                    )
                case "rcast":
                    current_song = requests.get(radio.url_api_radio_current_song).json()
                    history, covers = current_song.get(
                        "trackhistory", []
                    ), current_song.get("covers")
                    song_data = current_song.get("nowplaying").split("-")
                    for track, cover in zip(history, covers):
                        song = track.split("-")
                        track = Track(
                            title=song[0].strip(),
                            album_title="",
                            cover=cover,
                            artist_name=song[1].strip(),
                        )
                        song_list_history.append(track)
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title=song_data[1].strip(),
                        album_title="",
                        cover=current_song.get("coverart"),
                        artist_name=song_data[0].strip(),
                        song_history=song_list_history,
                    )
                case "centovacast":
                    history = (
                        requests.get(radio.url_api_radio_history)
                        .json()
                        .get("items", [])
                    )
                    for track in history:
                        data = track["title"].split("-")
                        song = Track(
                            title=data[1],
                            album_title="",
                            cover=track.get("enclosure").get("url"),
                            artist_name=data[0],
                        )
                        song_list_history.append(song)
                    current_song = (
                        requests.get(radio.url_api_radio_current_song)
                        .json()
                        .get("data")[0]
                        .get("track")
                    )
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title=current_song.get("title"),
                        album_title=current_song.get("album"),
                        cover=current_song.get("imageurl"),
                        artist_name=current_song.get("artist"),
                        song_history=song_list_history,
                    )
                case "azuracast":
                    current_song = requests.get(radio.url_api_radio_current_song).json()
                    history = current_song.get("song_history", [])
                    for track in history:
                        song = Track(
                            title=track.get("song").get("title"),
                            album_title=track.get("song").get("album"),
                            cover=track.get("song").get("art"),
                            artist_name=track.get("song").get("artist"),
                        )
                        song_list_history.append(song)
                    song_data = current_song.get("now_playing").get("song")
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title=song_data.get("text"),
                        album_title=song_data.get("album"),
                        cover=song_data.get("art"),
                        artist_name=song_data.get("artist"),
                        song_history=song_list_history,
                    )
                case "radioking":
                    return RadioMedata(
                        id=radio.pk,
                        user_id=radio.user.id,
                        radio_flux=radio.url_flux_radio,
                        title="",
                        album_title="",
                        cover=str(radio.radio_image_icon.url),
                        artist_name="",
                    )
