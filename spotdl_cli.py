from os import system
import sys
from threading import Thread

try:
    import spotdl
except:
    if input("spotdl not found, Download Now? (y/n): ").lower() == 'y':
        system('pip install -U spotdl')
    else:
        sys.exit()

from spotdl.authorize.services import AuthorizeSpotify
from spotdl import Spotdl, util
from spotdl.helpers.spotify import SpotifyHelpers


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# -- As per Spotfiy API documentation --
# Make sure that you safeguard your application Client Secret at all times.
# Be aware, for example, that if you commit your code to a public repository like GitHub
# you will need to remove the Client Secret from your code before doing so.
u_client_id = ''
u_client_secret = ''


try:
    # Attempt to locate spotify secret keys from a local spotify_keys.txt file
    with open("spotify_keys.txt", "r+") as keys:
        contents = keys.readlines()
        if contents:
            contents = [key.strip() for key in contents]  # Removal of newlines
            try:
                u_client_id = contents[0]
                u_client_secret = contents[1]
                print(BColors.OKGREEN +
                      "Success: Found local spotify keys!" + BColors.ENDC)
            except IndexError:
                raise FileNotFoundError
        else:
            raise FileNotFoundError

except FileNotFoundError:
    # If keys are not found, allow the user to obtain the keys from spotify
    print(BColors.WARNING + "Warning: You are missing the client_id/secret which is required for the album/playlist features" + BColors.ENDC)
    print(BColors.WARNING +
          "You can obtain these keys by creating a quick app with Spotify" + BColors.ENDC)
    print("https://developer.spotify.com/dashboard/applications\n")

    # User is able to proceed without keys, which will limit some features
    if(input("Enter keys manually? (y/n): ").lower()[0] == "y"):

        # Note: Create a first call to the /autorize endpoint to validate if an API token was retrieved?
        u_client_id = input("Enter your client id:")
        u_client_secret = input("Enter your client secret:")

        # Keys will be saved for the future in a local text file
        with open("spotify_keys.txt", "w") as keys:
            keys.writelines([u_client_id + "\n", u_client_secret])
        print(BColors.OKGREEN +
              "Success: Your keys were saved for future use!" + BColors.ENDC)

    else:
        print(BColors.WARNING +
              "Warning: Cannot proceed without the keys! Exiting Now..." + BColors.ENDC)
        sys.exit()
except:
    raise

helper_instance = SpotifyHelpers(spotify=AuthorizeSpotify(
    client_id=u_client_id, client_secret=u_client_secret))
spotdl_instance = Spotdl()


def logs():
    print(util.install_logger(level='INFO'))


log = Thread(target=logs)


def song(link):
    log.start()

    def download():
        spotdl_instance.download_track(link)

    downloader = Thread(target=download)
    downloader.start()


def album(link):
    log.start()
    alb = helper_instance.fetch_album(link)
    helper_instance.write_album_tracks(alb, './album_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('album_tracks.txt')

    downloader = Thread(target=download)
    downloader.start()


def playlist(link):
    log.start()
    playlist = helper_instance.fetch_playlist(link)
    helper_instance.write_playlist_tracks(playlist, '.\playlist_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('playlist_tracks.txt')

    downloader = Thread(target=download)
    downloader.start()


def textlist(directory):
    log.start()

    def download():
        spotdl_instance.download_tracks_from_file(directory)

    downloader = Thread(target=download)
    downloader.start()


def scan(link):
    if "spotify.com/track" in link.lower():
        song(link)
    elif "spotify.com/playlist" in link.lower():
        playlist(link)
    elif ".txt" in link.lower():
        textlist(link)
    elif "spotify.com/album" in link.lower():
        album(link)
    else:
        song(link)


def main():
    system('cls')

    print(
        """
     ======================================================
    |                                                      |
    |   1) Simple Usage.     2) Manual (Advanced) Usage.   |
    |                                                      |
     ======================================================
    """
    )

    type = input("Selcet an Option (1/2): ")

    if type == '1':
        system('cls')
        scan(input(
            "Enter A Song/playlist/album link or Enter the path to a list:\n"))
    elif type == '2':
        system('cls')
        __import__('adv_spotdl_cli').main()
    else:
        print("Invalid Input")
        sys.exit()


if __name__ == '__main__':
    main()
