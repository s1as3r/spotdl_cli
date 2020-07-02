from os import system


def song():
    link = input("Enter the song link or enter song name: ")
    log = input("Log Level (INFO/DEBUG) = ")
    if_output = input("Manual output directory(y/n)?: ")
    if if_output.lower() == 'y':
        output = input("Enter The Output Directory: ")
        if_search = input("Manual Search String (y/n): ")
        if if_search.lower() == 'n':
            system(f"spotdl -s {link} -f {output} --log-level={log.upper()}")
        elif if_search.lower() == 'y':
            search = input("Enter the search string: ")
            system(f"spotdl -s {link} -f {output} --log-level={log.upper()} -sf{search}")
        else:
            print("Invalid Option Selected.")

    elif if_output.lower() == 'n':
        if_search = input("Manual Search String (y/n): ")
        if if_search.lower() == 'n':
            system(f"spotdl -s {link} --log-level={log.upper()}")
        elif if_search.lower() == 'y':
            search = input("Enter the search string: ")
            system(f"spotdl -s {link} --log-level={log.upper()} -sf {search}")
        else:
            print("Invalid Option Selected..")
    else:
        print("Invalid Option Selected..")


def playlist():
    link = input("Enter the playlist link: ")
    log = input("Log Level (INFO/DEBUG) = ")
    if_output = input("Manual output directory(y/n)?: ")
    if if_output.lower() == 'y':
        output = input("Enter The Output Directory: ")
        system(f"spotdl -p {link} --log-level={log.upper()} -f {output}")
    elif if_output.lower() == 'n':
        system(f"spotdl -p {link} --log-level={log.upper()}")
    else:
        print("Invalid Option Selected..")


def textlist():
    path = str(input("Enter the Path to the list: "))
    log = input("Log Level (INFO/DEBUG): ")
    system(f"spotdl -l {path} --log-level={log.upper()}")


def main():
    selection = input("What do you want to download:\n "
                      "1) Only One Song.\n"
                      "2) A Playlist.\n"
                      "3) A list of songs.\n"
                      "Selcet an Option (1/2/3): ")
    if selection == "1":
        song()
    elif selection == "2":
        playlist()
    elif selection == "3":
        textlist()
    else:
        print("Invalid Option Selected.")


main()
