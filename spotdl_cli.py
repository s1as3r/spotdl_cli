from os import system
import adv.adv_spotdl_cli as adv

try:
    import spotdl
except:
    print('spotdl not found, downloading now.')
    system('pip installl -U spotdl')

def song():
    system(f"spotdl -s {link}")


def album():
    system(f"spotdl -a {link} --write-to=list.txt")
    system(f"spotdl -l list.txt")


def playlist():
    system(f"spotdl -p {link} --write-to=playlist.txt")
    system(f"spotdl -l playlist.txt")

def textlist():
    system(f"spotdl -l {link}")


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
