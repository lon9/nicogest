import os
import argparse
from urllib import request
from bs4 import BeautifulSoup
import youtube_dl
from moviepy.editor import VideoFileClip, concatenate_videoclips

NICOCO_URL = 'http://nicoco.net/'
VIDEO_URL = 'https://www.nicovideo.jp/watch/'

class Nicogest():
    def __init__(self, output_dir='./', threshold_multiplier=1.2):
        self.output_dir = output_dir
        self.threshold_multiplier = threshold_multiplier

    def _get_seconds(self, time):
        splitted = time.split('.')
        return 60*int(splitted[0])+int(splitted[1])

    def _get_comments(self, video_id):
        html = request.urlopen(NICOCO_URL+video_id)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find('table').find_all('tr')

        comments = []
        for row in rows[1:]:
            tds = row.find_all('td')
            comment_id = tds[0].text
            time = tds[1].text
            user_id = tds[2].text
            content = tds[3].text
            created_at = tds[5].text
            comments.append({
                'comment_id': comment_id,
                'time': time,
                'seconds': self._get_seconds(time),
                'user_id': user_id,
                'content': content,
                'created_at': created_at
            })
        return comments

    def _download_video(self, video_id):
        opts = {
            'outtmpl': '%(id)s.%(ext)s',
            'retries': 10
        }
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([VIDEO_URL+video_id])

    def do(self, video_id):

        # download a video
        self._download_video(video_id)

        # get comments
        comments = self._get_comments(video_id)
        time_table = {}

        # sort comments
        comments = sorted(comments, key=lambda x:x['seconds'])

        # make time table
        for comment in comments:
            if comment['seconds'] in time_table:
                time_table[comment['seconds']].append(comment)
            else:
                time_table[comment['seconds']] = [comment]

        # calculate average
        mu = sum([len(v) for v in time_table.values()]) / len(time_table)
        threshold = mu * self.threshold_multiplier
        print('Average comments: ', mu)
        print('Threshold: ', threshold)

        is_during = False
        start = 0
        end = 0
        stop_count = 0

        video_name = video_id+'.mp4'
        video = VideoFileClip(video_name)
        clips = []
        print('Video duration: ', video.duration)
        for i, (k, v) in enumerate(time_table.items()):
            if len(v) > threshold and not is_during and k < video.duration:
                if k >= 1:
                    start = k - 1
                else:
                    start = k
                is_during = True
            elif len(v) <= threshold and is_during:
                if k < video.duration:
                    if stop_count > 2:
                        end = k
                        print(start,end)
                        clip = video.subclip(start, end)
                        clips.append(clip)
                        start = 0
                        end = 0
                        stop_count = 0
                        is_during = False
                    else:
                        stop_count += 1
                else:
                    end = list(time_table.keys())[i-1]
                    print(start,end)
                    clip = video.subclip(start, end)
                    clips.append(clip)
                    start = 0
                    end = 0
                    stop_count = 0
                    is_during = False

        # concat clips
        final_clip = concatenate_videoclips(clips)
        # save
        final_clip.write_videofile(os.path.join(self.output_dir, video_id+'_digest.mp4'))

        # remove video
        os.remove(video_name)
