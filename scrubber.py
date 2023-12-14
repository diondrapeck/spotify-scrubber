import os
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import argparse


# Set up auth
os.environ["SPOTIPY_CLIENT_ID"] = "client id"
os.environ["SPOTIPY_CLIENT_SECRET"] = "client secret"
os.environ["SPOTIPY_REDIRECT_URI"] = "redirect url"


def get_clean_version(client, track):
    # Get track info
    track_name = track.get("track").get("name")
    track_artist = track.get("track").get("artists")[0].get("name")

    # Search for clean version
    query_results = client.search(q=f"{track_name} {track_artist}", type="track").get("tracks").get("items")
    for track in query_results:
        if track.get("artists")[0].get("name") == track_artist and track.get("name") == track_name and not track.get("explicit"):
            return track.get("id")
    print(f"No clean version found for {track_name} by {track_artist}. Will be omitted from playlist.")
    return None


def scrub_playlist(playlist_name):
    # Set up auth
    sp = Spotify(oauth_manager=SpotifyOAuth(scope="playlist-modify-public"))
    user_id = sp.current_user().get("id")

    # Get explicit playlist
    explicit_playlist = None
    playlists = sp.current_user_playlists().get("items")
    for playlist in playlists:
        if playlist.get("name") == playlist_name:
            explicit_playlist = playlist.get("id")
            is_public = playlist.get("public")
            explicit_playlist = sp.playlist_items(playlist_id=explicit_playlist).get("items")
    if explicit_playlist is None:
        print("Playlist not found")
        return 1
    
    # Initialize new playlist
    scrubbed_name = playlist_name + " (Clean)"
    scrubbed_playlist = sp.user_playlist_create(user=user_id, name=scrubbed_name, public=is_public).get("id")

    # Build new playlist
    scrubbed_tracks = []
    for track in explicit_playlist:
        if track.get("track").get("explicit"):
            scrubbed_track = get_clean_version(sp, track)
        else:
            scrubbed_track = track.get("track").get("id")

        if scrubbed_track:
            scrubbed_tracks.append(scrubbed_track)

    sp.user_playlist_add_tracks(user=user_id, playlist_id=scrubbed_playlist, tracks=scrubbed_tracks)

    print(f"Playlist {scrubbed_name} successfully created.")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-n", "--name", help="Spotify playlist name")
    args = argParser.parse_args()

    scrub_playlist(playlist_name=args.name)
