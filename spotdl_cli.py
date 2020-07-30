import sys
from threading import Thread

from spotdl import Spotdl, util
from spotdl.helpers.spotify import SpotifyHelpers

from adv import adv_spotdl_cli as adv

helper_instance = SpotifyHelpers()
spotdl_instance = Spotdl()


def logs():
    print(util.install_logger(level='INFO'))

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
    elif ".txt" in link.lower():
        textlist()
    elif "spotify.com/album" in link.lower():
        album()
    else:
        song()

def main():
    global link
    type = input("1) Simple Usage.\n"
                "2) Manual (Advanced) Usage.\n"
                "Selcet an Option (1/2): ")
    if type == '1':
        link = input("Enter A Song/playlist/album link or Enter the path to a list:\n")
        scan()
    elif type == '2':
        adv.main()
    else:
        print("Invalid Input")

if __name__ == '__main__':
    main()
