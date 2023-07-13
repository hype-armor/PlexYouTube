from pytube import YouTube, Channel
from datetime import datetime, timedelta
import curses, time


import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

import unicodedata
import re

# Initialize curses
stdscr = curses.initscr()
# Get the size of the window
height, width = stdscr.getmaxyx()

locations = {
    "app_title": (1, 1),
    "current_action": (3, 3),
    "channel": (2, 2),
    "video": (4, 4),
    "history": (height-1, 1)
}
history = []

# Move cursor to position (1, 1)
def move_cursor(item):
    stdscr.move(locations[item][0], locations[item][1])

def clear_text(item):
    stdscr.move(locations[item][0], locations[item][1])
    stdscr.clrtoeol()

# Write "test" at that position
def update_text(string, item):
    
    #stdscr.refresh()
    max_length = 5
    string.ljust(max_length)
    
    max_chars = width - locations[item][1] - 1
    string = string[:max_chars]
    
    if len(history) == height - 7:
        history.pop(0)
    history.append(string)

    stdscr.refresh()
    time.sleep(0.04) # don't ask me why this is needed, but it is.
    stdscr.move(locations['history'][0] - len(history), 0)
    stdscr.clrtobot()
    move_cursor("history")
    for i in range(0, len(history)):
        ypos = (locations['history'][0] - i) -1
        stdscr.move(ypos, locations['history'][1])
        stdscr.addstr(history[i])

    clear_text(item)
    move_cursor(item)
    stdscr.addstr(string)
    
    # Refresh the screen to see the changes
    stdscr.refresh()

def parse_to_filename(s):
    # Pattern to match all invalid filename characters
    pattern = r'[<>:"/\\|?*]'

    # Use re.sub() to replace the pattern with an empty string
    return re.sub(pattern, '', s)
   

update_text("YouTube Downloader!", "app_title")
time.sleep(1)
update_text("Starting Up", "history")
 
today = datetime.now()
thirty_days_ago = today - timedelta(days=9000)

with open('Wantallvids.txt', "r") as f:
    for line in f:
        c = Channel(line)
        update_text(c.channel_name, "channel")
        update_text('Searching', "current_action")
        for video in c.videos:
            try:
                title = parse_to_filename(video.title)
                
                if os.path.exists(c.channel_name + '\\' + title + '.mp4'):
                    update_text('SKIPPING: ' + title, "video")
                    continue

                # if we won't have the video, see if it's too old.
                if (video.publish_date < thirty_days_ago):
                    update_text('SKIPPING TOO OLD: ' + title, "video")
                    break

                update_text('Downloading: ' + video.title, "current_action")
                video.streams.get_highest_resolution().download(c.channel_name, title + '.mp4', timeout=60)
                time.sleep(1)
                update_text('Searching', "current_action")
                if 'str' in line:
                    break
            except Exception as e:
                update_text('Error Downloading: ' + video.title, "current_action")
                if hasattr(e, 'error_string'):
                    update_text(e.error_string, "current_action")
