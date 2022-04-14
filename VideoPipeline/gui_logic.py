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

from gui_design import VideoPipelineMainInterface


class VideoPipelineGui(VideoPipelineMainInterface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_hooks()

    def _setup_hooks(self):
        """
        Initialises all static button / widget interactions
        """
        self.w_enc_video_slider.valueChanged.connect(self.a_video_slider_sync)
        self.w_enc_video_quality.valueChanged.connect(self.a_video_quality_sync)
        self.w_enc_audio_slider.valueChanged.connect(self.a_audio_slider_sync)
        self.w_enc_audio_quality.valueChanged.connect(self.a_audio_quality_sync)

    def a_video_slider_sync(self):
        """
        Syncs from Slider to Spin Box
        """
        self.w_enc_video_quality.setValue(self.w_enc_video_slider.value()/10)

    def a_video_quality_sync(self):
        """
        Syncs quality back to the slider
        """
        self.w_enc_video_slider.setValue(round(self.w_enc_video_quality.value()*10))

    def a_audio_slider_sync(self):
        """
        Syncs from Slider to Spin Box
        """
        self.w_enc_audio_quality.setValue(self.w_enc_audio_slider.value()/10)

    def a_audio_quality_sync(self):
        """
        Syncs quality back to the slider
        """
        self.w_enc_audio_slider.setValue(round(self.w_enc_audio_quality.value()*10))

