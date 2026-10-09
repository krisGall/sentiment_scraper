from datetime import datetime

def show_header():
    """
    Creates the header in terminal for the program.
    """
    print(
    """
    \n
    +==========================================+
    |              Bluesky Scraper             |
    +==========================================+
    \n
    """
)

def get_current_time():
    """
    Returns the current time as a string

    Returns:
        string showing datetime currently.
    """
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))