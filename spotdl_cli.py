from os import system
import sys


def song():
    log = input("Log Level (INFO/DEBUG) = ")
    if log.lower() not in ("info", "debug"):
        print("Invalid Option Selected.")
        sys.exit()
    
    filetype = input("Output File Type? (m4a,ogg,mp3,opus,flac): ")
    if filetype.lower() not in ('m4a', 'ogg', 'mp3', 'opus', 'flac'):
        print("Invalid File Format Selected.")
        sys.exit()
    
    if_output = input("Manual output directory(y/n)?: ")
    if if_output.lower() == 'y':
        output = input("Enter The Output Directory: ")
        
        if_search = input("Manual Search String (y/n): ")
        if if_search.lower() == 'n':
            system(f"spotdl -s {link} -f {output} --log-level={log.upper()} -o {filetype}")
        elif if_search.lower() == 'y':
            search = input("Enter the search string: ")
            system(f"spotdl -s {link} -f {output} --log-level={log.upper()} -sf{search} -o {filetype}")
        else:
            print("Invalid Option Selected.")
            sys.exit()

    elif if_output.lower() == 'n':
        if_search = input("Manual Search String (y/n): ")
        if if_search.lower() == 'n':
            system(f"spotdl -s {link} --log-level={log.upper()}")
        elif if_search.lower() == 'y':
            search = input("Enter the search string: ")
            system(f"spotdl -s {link} --log-level={log.upper()} -sf {search}")
        else:
            print("Invalid Option Selected..")
            sys.exit()
    else:
        print("Invalid Option Selected..")
        sys.exit()


def playlist():
    log = input("Log Level (INFO/DEBUG) = ")
    
    if_output = input("Manual output directory(y/n)?: ")
    if if_output.lower() == 'y':
        output = input("Enter The Output Directory: ")
        system(f"spotdl -p {link} --log-level={log.upper()} -f {output}")
    elif if_output.lower() == 'n':
        system(f"spotdl -p {link} --log-level={log.upper()}")
    else:
        print("Invalid Option Selected..")
        sys.exit()


def textlist():
    path = str(input("Enter the Path to the list: "))
    log = input("Log Level (INFO/DEBUG): ")
    system(f"spotdl -l {path} --log-level={log.upper()}")


def scan():
    if "spotify.com/track" in link.lower():
        song()
    elif "spotify.com/playlist" in link.lower():
        playlist()
    else:
        song()

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
