#!/usr/bin/env python
# -*- coding: utf-8 -*-
from moviepy.editor import *
import arabic_reshaper
from bidi.algorithm import get_display
from moviepy.video.tools.credits import credits1
import json
import sys
import pyarabic


def readJson(position):
    with open("real_estate.json", "r") as file:
        data = json.load(file)
        info_list = data["Real Estate"][position]
        return info_list


def make_movie(movie_version):
    screensize = (720, 460)
    current_dictionary = readJson(movie_version)

    all_videos = []
    counter = 0
    for key in current_dictionary:

        if counter == 0:

            clip = TextClip(key + " -> " + "{0}".format(current_dictionary[key]),
                            color="white",
                            fontsize=15,
                            stroke_width=5,
                            size=screensize).set_duration(3)
            clip.write_videofile("{0}clip.mp4".format(counter), fps=25)
            all_videos.append(VideoFileClip("{0}clip.mp4".format(counter)))
            counter = counter + 1

        else:
            txtClip = key + " -> " + current_dictionary[key]
            clip = TextClip(txtClip, color="white", fontsize=15, stroke_width=2, size=screensize).set_duration(3)
            clip.write_videofile("{0}clip.mp4".format(counter), fps=25)
            all_videos.append(VideoFileClip("{0}clip.mp4".format(counter)))
            counter = counter + 1

    final_clip = concatenate_videoclips(all_videos)
    final_clip.write_videofile("my_concatenation.mp4", fps=25)


make_movie(2)
