from os import system
import adv.adv_spotdl_cli as adv


def song():
    system(f"spotdl -s {link}")


def album():
    system(f"spotdl -a {link} --write-to=list.txt")
    system(f"spotdl -l list.txt")


def playlist():
    system(f"spotdl -p {link} --write-to=playlist.txt")
    system(f"spotdl -l playlist.txt")

def textlist():
    path = str(input("Enter the Path to the list: "))
    system(f"spotdl -l {path}")


def scan():
    if "spotify.com/track" in link.lower():
        song()
    elif "spotify.com/playlist" in link.lower():
        playlist()
    elif "spotify.com/album" in link.lower():
        album()
    else:
        song()

type = input("1) Simple Usage.\n"
             "2) Manula (Advanced) Usage.\n"
             "Selcet an Option (1/2): ")
if type == '1':
    selection = input("What do you want to download:\n"
                      "1) A Song or Playlsit.\n"
                      "2) A List of Songs.\n"
                      "Selcet an Option (1/2): ")

    if selection == "1":
        link = input("Enter the song link or enter song name: ")
        scan()
    elif selection == "2":
        textlist()
    else:
        print("Invalid Option Selected.")
elif type == '2':
    adv.main()
else:
    print("Invalid Input")
