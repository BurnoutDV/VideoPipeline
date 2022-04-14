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

import ffmpeg
from hard_definitions import *


def use_project_on_file(file: str, project: dict):
    para = {'v_stream': vp_vid_stream,
            'v_crf': vp_vid_crf,
            'v_g': vp_vid_g,
            'v_bf': vp_vid_bf,
            'scaling': vp_vid_scaling_w,
            'a_0': vp_aud_stream0,
            'a_1': vp_aud_stream1,
            'a_0db': vp_aud_stream0_boost,
            'a_1db': vp_aud_stream1_boost,
            'a_q': vp_aud_quality}
    if 'video' in project:
        for key, value in project_file_video_makeup:
            if key in project['video']:
                para[value] = project['video'][key]
    if 'audio' in project:
        for key, value in project_file_audio_makeup:
            if key in project['audio']:
                para[value] = project['video'][key]
    stream = ffmpeg.input(file)
    cli = f"ffmpeg -i {file}" \
          f" -filter_complex '[0:a:{para['a_0']}][0:a:{para['a_1']}]amix=2:longest:weights=1 2[aout]'" \
          f" -map 0:v:0 -c:v:0 libx264 -crf {para['v_crf']} -preset medium -g {para['v_g']} -bf {para['v_bf']}'" \
          f" -map '[aout]' -c:a libvorbis -q:a {para['a_q']}" \
          f" -map 0:a:1" \
          f" -map 0:a:2" \
          f" 'output.mkv'"
    ffmpeg.run()
