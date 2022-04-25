#!/usr/bin/env python
# coding: utf-8

# Copyright 2022 by BurnoutDV, <development@burnoutdv.com>
#
# This file is part of [CHANGE]VideoPipeline.
#
# [CHANGE]VideoPipeline is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# [CHANGE]VideoPipeline is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0-only <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
As a final layer of fallback this file provides all the default and hopefully sane settings if nothing else can be
found elsewhere
"""

VERSION: str = "0.01"

# vp = videopipeline
vp_vid_stream = 0  # video stream that is used per default, almost no file has more than 1
vp_vid_crf = 23.0  # quality rate factor
vp_vid_g = 250  # key frames interval
vp_vid_bf = 16  # bframes
vp_vid_scaling_w = -1  # scaling via Lanczos4 to size, height will always be automatic
vp_aud_stream0 = 1  # audio stream inside the file that is considered #1
vp_aud_stream1 = 2  # audio stream inside the file that is considered #2
vp_aud_stream0_boost = 0  # volume adjustment of stream 0 in dB
vp_aud_stream1_boost = 0  # volume adjustment of stream 1 in dB
vp_aud_quality = 7.0  # quality target for ogg-vorbis encoding

vk_translate_to_preset = {
        'vid_src': vp_vid_stream,
        'vid_quality': vp_vid_crf,
        'aud_src1': vp_aud_stream0,
        'aud_src2': vp_aud_stream1,
        'aud_quality': vp_aud_quality,
        'aud_adj1': vp_aud_stream0_boost,
        'aud_adj2': vp_aud_stream1_boost,
        'aud_archive': False
    }

project_file_video_makeup = {'stream': 'v_stream', 'crf': 'v_crf', 'g': 'v_g', 'bf': 'v_bf', 'scaling_w': 'scaling_w'}
project_file_audio_makeup = {'stream0': 'a_0', 'stream1': 'a_1', 'stream0_boost': 'a_0db', 'stream1_boost': 'a_1db',
                             'quality': 'a_q'}

rescale_presets = ["1280x720", "1920x1080", "2560x1440", "3840x2160", "640x480", "800x600", "1024x768", "1280x1024"]
reframe_presets = ["15", "20", "25", "30", "45", "60"]