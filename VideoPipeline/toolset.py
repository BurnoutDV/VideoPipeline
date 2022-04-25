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
import logging
import re
from datetime import timedelta

logger = logging.getLogger(__name__)


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


def create_full_encoding_preset(partial_preset: dict):
    """
    Enriches any given preset with a all necessary parameters, supplementing with defaults if necessary
    :param partial_preset:
    :return:
    """
    full_preset = {
        'vid_codec': "libx264",
        'vid_src': 0,
        'vid_quality': 0.0,
        'vid_rescale': "",
        'vid_sample': "",
        'aud_codec': "libvorbis",
        'aud_src1': 0,
        'aud_src2': 0,
        'aud_quality': 0.0,
        'aud_adj1': 0,
        'aud_adj2': 0,
        'aud_archive': 0
    }
    ranges = {
        'vid_quality': {
            'min': 0.0,
            'max': 51.0
        },
        'aud_quality': {
            'min': 0.0,
            'max': 10.0
        }
    }
    for key, value in full_preset.items():
        if key in partial_preset and not value and not isinstance(partial_preset[key], (dict, list)):
            try:
                if isinstance(value, int):
                    full_preset[key] = int(partial_preset[key])
                elif isinstance(value, float):
                    full_preset[key] = float(partial_preset[key])
                else:
                    full_preset[key] = partial_preset[key]
                if key in ranges:  # makes sure values are in a sane range, currently only for vorbis & x264 crf
                    if full_preset[key] < ranges[key]['min'] or full_preset[key] > ranges[key]['max']:
                        full_preset[key] = vk_translate_to_preset[key]
            except ValueError:
                full_preset[key] = vk_translate_to_preset[key]
        else:
            full_preset[key] = vk_translate_to_preset[key]
    return full_preset


def extract_probe(ffmpeg_probe: dict) -> dict:
    for stream in ffmpeg_probe['streams']:
        if stream['codec_type'] == "video":
            raw_fps = int(stream['r_frame_rate'].split("/")[0])
            # tags can actually have a language assigned to them..hrrr
            dur_tag = None
            for key in stream['tags']:
                if key[0:8] == "DURATION":
                    dur_tag = key
                    break
            else:
                return {}
            raw_delta = str_to_timedelta(stream['tags'][dur_tag])
            raw_frames = round(raw_delta.seconds*raw_fps + (raw_delta.microseconds/100)*raw_fps)
            return {
                "time_length": raw_delta,
                "file_size": int(ffmpeg_probe['format']['size'])*1024,  # ffmpeg gives us kbyte
                "fps": int(raw_fps),
                "est_frames": raw_frames
            }
    return {}


def sizeof_fmt(num: int, suffix="B") -> str:
    """
    Human readeable size, stolen from another repo

    https://stackoverflow.com/a/1094933

    https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size
    :param int num: size in bytes
    :param str suffix: suffix after size identifier, like GiB
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.2f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.2f} Yi{suffix}"


def str_to_timedelta(delta_str: str) -> timedelta:
    """
    Converts a string of the format "HH:MM:SS:MS" to a timedelta object

    Checks the correct structure by regex which might be somewhat expensive
    """
    if not re.match(r"^[0-9]{2}:[0-9]{2}:[0-9]{2}[.][0-9]{2}.*$", delta_str):
        if re.match(r"^[0-9]:[0-9]{2}:[0-9]{2}[.][0-9]{2}.*$", delta_str):
            logger.warning(f"timedelta correct '{delta_str}'")
            delta_str = "0" + delta_str
        else:
            logger.error(f"timedelta error '{delta_str}'")
            return timedelta(seconds=0)  # empty timedelta, not sure about that one, timedelta(0) is not falsey
    return timedelta(hours=int(delta_str[0:2]),
                     minutes=int(delta_str[3:5]),
                     seconds=int(delta_str[6:8]),
                     microseconds=int(delta_str[9:11]))


def format_timedelta(gamma: timedelta) -> str:
    return f"{str(gamma.seconds//3600):0>2}:{str(int(gamma.seconds//60%60)):0>2}:{str(gamma.seconds%60):0>2}"


def regex_ffmpeg_encoding(stderr: str) -> dict:
    pattern = r"^(frame=\s*)([0-9]+)\s+(fps=)\s*([0-9]+)\s+(q=)\s*([0-9]*[.]?[0-9]+)\s+(size=)\s*([0-9]+)..\s+(time=)\s*([0-9][0-9]:[0-9][0-9]:[0-9][0-9][.][0-9][0-9])\s+(bitrate=)\s*([0-9]*[.]?[0-9]+)(kbits\/s)\s+(speed=)\s*([0-9]*[.]?[0-9]+)x\s*"
    result = re.search(pattern, stderr)
    if not result:
        return {}
    data = {}
    ints = ['frames', 'fps', 'file_size']
    floats = ['q', 'enc_rate', 'speed']
    data['frames'] = result.group(2)
    data['fps'] = result.group(4)
    data['q'] = result.group(6)
    data['file_size'] = result.group(8)
    data['elapsed'] = result.group(10)  # time of the material that is already encoded, not encoding time
    data['enc_rate'] = result.group(12)
    data['enc_unit'] = result.group(13)
    data['speed'] = result.group(15)
    for key in ints:
        try:
            data[key] = int(data[key])
        except TypeError:
            logger.warning(f"Cannot convert {key} to INT")
    for key in floats:
        try:
            data[key] = float(data[key])
        except TypeError:
            logger.warning(f"Cannot convert {key} to FLOAT")
    try:
        data['elapsed'] = str_to_timedelta(data['elapsed'])
    except TypeError:
        logger.warning("Cannot convert time elapsed into timedelta object")
    return data

