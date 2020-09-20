import sys
from threading import Thread
import os
from os import system

from spotdl.authorize.services import AuthorizeSpotify
from spotdl import Spotdl, util
from spotdl.helpers.spotify import SpotifyHelpers

with open("spotify_keys.txt", "r+") as keys:
    contents = keys.readlines()
    contents = [key.strip() for key in contents]  # Removal of newlines
    u_client_id = contents[0]
    u_client_secret = contents[1]

helper_instance = SpotifyHelpers(spotify=AuthorizeSpotify(
    client_id=u_client_id, client_secret=u_client_secret))
log_level, output_ext = 'INFO', 'mp3'  # Set Default Log Level and Output Format


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


def select():
    global log_level
    global output_ext

    system('cls')
    # FIXME: Make this a litte less messy?
    print(
        """
    ==============================================================
   |                                                               |
   |   1) Log Level = {:17}2) Output Format = {:9}|
   |   3) Set Manual Search String     4) Set Output Derictory     |
   |                        5) Start                               |
   |                                                               |
    ==============================================================
    """.format(log_level, output_ext)
    )
    return input("Enter option You want to change/set: ")


def main():
    global link
    global spotdl_instance
    global log_level
    global output_ext

    search_format = '{artist} - {track-name} lyrics'
    output_file = os.getcwd()
    again = 'Y'
    while again == 'Y':
        selection = select()
        if selection == '1':
            system('cls')
            log_level = input('Log Level (INFO/DEBUG/ERROR/WARNING) = ')
            if log_level.lower() not in ['info', 'error', 'debug', 'warning']:
                log_level = 'INFO'

        elif selection == '2':
            system('cls')
            output_ext = input('Output Format (m4a,flac,mp3,opus,ogg) = ')
            if output_ext.lower() not in ['m4a', 'flac', 'mp3', 'opus', 'ogg']:
                output_ext = 'mp3'

        elif selection == '3':
            system('cls')
            print(f'Current Search String: {search_format}')
            search_format = input('Enter Manual Search String: ')

        elif selection == '4':
            system('cls')
            print(f'Current Output Directory: {output_file}')
            output_file = input("Enter Path to the Directory: ")

        elif selection == '5':
            again = 'N'

    spotdl_instance = Spotdl(args={'output_ext': output_ext,
                                   'search_format': search_format,
                                   'output_file': output_file})

    system('cls')
    link = input("Enter the song/playlist/album link or path to a textlist: ")
    scan()


if __name__ == '__main__':
    main()
