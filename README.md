# spotify-scrubber


Algorithm to create a new, clean version of a Spotify playlist by replacing all explicit songs with their clean versions, if available.

To create a new clean version of an existing Spotify playlist, update the environment variables in scrubber.py with your own [Spotify Developer](https://developer.spotify.com/dashboard) credentials 
```python
os.environ["SPOTIPY_CLIENT_ID"] = "client id"
os.environ["SPOTIPY_CLIENT_SECRET"] = "client secret"
os.environ["SPOTIPY_REDIRECT_URI"] = "redirect url"
```

then run

```dotnetcli
python scrubber.py -n <playlist-name>
```