from pytube import YouTube, Channel
from datetime import datetime, timedelta

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

today = datetime.now()
thirty_days_ago = today - timedelta(days=10)

with open('Channels_to_DL.txt', "r") as f:
    for line in f:
        print(line)
        c = Channel(line)
        
        for video in c.videos:
            try:
                if (video.publish_date >= thirty_days_ago):
                    print ('Downloading:', video.title)
                    title = slugify(video.title)
                    #video.streams.get_highest_resolution().download(c.channel_name + ' [UC' + c.channel_id + ']', title + ' [' + video.video_id + '].mp4')
                    # import ffmpeg
                    # video_stream = ffmpeg.input('The Hospitals IT Staff hates me.mp4')
                    # audio_stream = ffmpeg.input('The Hospitals IT Staff hates me.webm')
                    # ffmpeg.output(audio_stream, video_stream, 'out.mp4').run()
                else:
                    break
                if 'str' in line:
                    break
            except:
                print ('Error downloading:', video.title)

def check_if_exists(video):
    video.title = slugify(video.title)


    #print (video.publish_date >= thirty_days_ago)
    #video.streams.first().download()