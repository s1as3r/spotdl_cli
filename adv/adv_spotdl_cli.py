import sys
from threading import Thread

from spotdl_cli import u_client_id, u_client_secret

from spotdl.authorize.services import AuthorizeSpotify
from spotdl import Spotdl, util
from spotdl.helpers.spotify import SpotifyHelpers

helper_instance = SpotifyHelpers(spotify=AuthorizeSpotify(client_id=u_client_id,
                                                          client_secret=u_client_secret))


def logs():
    print(util.install_logger(level=log_level.upper()))


log = Thread(target=logs)


def song():
    log.start()

    def download():
        spotdl_instance.download_track(link)
    downloader = Thread(target=download)
    downloader.start()


def album():
    log.start()
    alb = helper_instance.fetch_album(link)
    helper_instance.write_album_tracks(alb, './album_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('album_tracks.txt')
    downloader = Thread(target=download)
    downloader.start()


def playlist():
    log.start()
    playlist = helper_instance.fetch_playlist(link)
    helper_instance.write_playlist_tracks(playlist, '.\playlist_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('playlist_tracks.txt')
    downloader = Thread(target=download)
    downloader.start()


def textlist():
    log.start()

    def download():
        spotdl_instance.download_tracks_from_file(link)
    downloader = Thread(target=download)
    downloader.start()


def scan():
    if "spotify.com/track" in link.lower():
        song()
    elif "spotify.com/playlist" in link.lower():
        playlist()
    elif "spotify.com/album" in link.lower():
        album()
    else:
        song()


def main():
    global link
    global spotdl_instance
    global log_level

    log_level = input('Log Level (INFO/DEBUG/ERROR/WARNING) = ')
    if log_level.lower() not in ['info', 'error', 'debug', 'warning']:
        log_level = 'INFO'

    output_ext = input('Output Format (m4a,flac,mp3,opus,ogg) = ')
    if output_ext.lower() not in ['m4a', 'flac', 'mp3', 'opus', 'ogg']:
        output_ext = 'mp3'

    if input('Manual Search String? (y/n): ').lower() == 'y':
        search_format = input('Enter Manual Search String: ')
    else:
        search_format = '{artist} - {track-name} lyrics'

    if input('Manual Output Directory? (y/n): ').lower() == 'y':
        output_file = input("Enter Path to the Directory: ")
    else:
        output_file = '{artist} - {track-name}.{output_ext}'

    spotdl_instance = Spotdl(args={'output_ext': output_ext,
                                   'search_format': search_format,
                                   'output_file': output_file})

    link = input("Enter the song/playlist/album link or path to a textlist: ")

    scan()


if __name__ == '__main__':
    main()
