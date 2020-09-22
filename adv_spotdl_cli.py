import os
import sys
from threading import Thread

from spotdl import Spotdl, util
from spotdl.authorize.services import AuthorizeSpotify
from spotdl.helpers.spotify import SpotifyHelpers

with open("spotify_keys.txt", "r+") as keys:
    contents = keys.readlines()
    contents = [key.strip() for key in contents]  # Removal of newlines
    u_client_id = contents[0]
    u_client_secret = contents[1]

helper_instance = SpotifyHelpers(spotify=AuthorizeSpotify(
    client_id=u_client_id, client_secret=u_client_secret))


def logs(log_level):
    print(util.install_logger(level=log_level.upper()))


def song(link, log):
    log.start()

    def download():
        spotdl_instance.download_track(link)

    downloader = Thread(target=download)
    downloader.start()


def album(link, log):
    log.start()
    alb = helper_instance.fetch_album(link)
    helper_instance.write_album_tracks(alb, './album_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('album_tracks.txt')

    downloader = Thread(target=download)
    downloader.start()


def playlist(link, log):
    log.start()
    playlist = helper_instance.fetch_playlist(link)
    helper_instance.write_playlist_tracks(playlist, '.\playlist_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('playlist_tracks.txt')

    downloader = Thread(target=download)
    downloader.start()


def textlist(directory, log):
    log.start()

    def download():
        spotdl_instance.download_tracks_from_file(directory)

    downloader = Thread(target=download)
    downloader.start()


def scan(link, log):
    if "spotify.com/track" in link.lower():
        song(link, log)
    elif "spotify.com/playlist" in link.lower():
        playlist(link, log)
    elif "spotify.com/album" in link.lower():
        album(link, log)
    elif ".txt" in link.lower():
        textlist(link, log)
    else:
        song(link, log)


def select(output_ext, log_level):
    os.system('cls')

    print(
        f"""
    =================================================================
   |                                                                 |
   |   1) Log Level = {log_level:19}2) Output Format = {output_ext:9}|
   |   3) Set Manual Search String       4) Set Output Derictory     |
   |   5) Start                          6) Exit                     |
   |                                                                 |
    =================================================================
    """
    )
    return input("Enter option You want to change/set: ")


def main():
    global spotdl_instance

    search_format = '{artist} - {track-name} lyrics'
    log_level = 'INFO'
    output_ext = 'mp3'
    output_file = os.getcwd()
    again = 'Y'
    while again == 'Y':
        selection = select(output_ext, log_level)
        if selection == '1':
            os.system('cls')
            log_level = input('Log Level (INFO/DEBUG/ERROR/WARNING) = ')
            if log_level.lower() not in ['info', 'error', 'debug', 'warning']:
                log_level = 'INFO'

        elif selection == '2':
            os.system('cls')
            output_ext = input('Output Format (m4a,flac,mp3,opus,ogg) = ')
            if output_ext.lower() not in ['m4a', 'flac', 'mp3', 'opus', 'ogg']:
                output_ext = 'mp3'

        elif selection == '3':
            os.system('cls')
            print(f'Current Search String: {search_format}')
            search_format_inp = input('Enter Manual Search String: ')
            if search_format_inp.lower() == 'default':
                search_format = '{artist} - {track-name} lyrics'
            elif not search_format_inp:
                continue
            else:
                search_format = search_format_inp

        elif selection == '4':
            os.system('cls')
            print(f'Current Output Directory: {output_file}')
            output_file_inp = input("Enter Path to the Directory: ")
            if output_file_inp.lower() == 'default':
                output_file = os.getcwd()
            elif not output_file_inp:
                continue
            else:
                output_file = output_file_inp

        elif selection == '5':
            again = 'N'

        elif selection == '6':
            sys.exit()

        else:
            continue

    spotdl_instance = Spotdl(args={'output_ext': output_ext,
                                   'search_format': search_format,
                                   'output_file': output_file})

    os.system('cls')
    log = Thread(target=logs, kwargs={'log_level':log_level})
    scan(input("Enter the song/playlist/album link or path to a textlist: "), log)


if __name__ == '__main__':
    main()
