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
from encoder_presets import EncoderPresetDialogue
from toolset import extract_probe, format_timedelta
from PySide6 import QtCore, QtGui
from pathlib import Path, PurePath
from datetime import timedelta
import os
import ffmpeg


class VideoPipelineGui(VideoPipelineMainInterface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_hooks()
        # instance variables
        self.v_dropped_elements = []
        self.sub_proc = {}

    def _setup_hooks(self):
        """
        Initialises all static button / widget interactions
        """
        self.w_enc_video_slider.valueChanged.connect(self.a_video_slider_sync)
        self.w_enc_video_quality.valueChanged.connect(self.a_video_quality_sync)
        self.w_enc_audio_slider.valueChanged.connect(self.a_audio_slider_sync)
        self.w_enc_audio_quality.valueChanged.connect(self.a_audio_quality_sync)
        self.w_enc_preset_new.clicked.connect(self.test)

    def test(self):
        bla = EncoderPresetDialogue(encoder_preset={}, parent=self)
        if bla.exec():
            print(bla.get_data())
            blo = EncoderPresetDialogue(encoder_preset=bla.get_data(), parent=self)
            blo.exec()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.v_dropped_elements.append(url.toLocalFile())
        self.a_trigger_order_work()

    def a_trigger_order_work(self):
        if not self.v_dropped_elements:
            return
        a_file = self.v_dropped_elements.pop()
        if not Path(a_file).is_file():
            return
        data = extract_probe(ffmpeg.probe(a_file))
        print(a_file)
        self.w_proj_title.setText("")
        for i in range(3):
            point = data['time_length'].total_seconds() * ((i + 1) / 4)
            time_point = format_timedelta(timedelta(seconds=point))
            self.w_proj_title.setText(f"{self.w_proj_title.text()} - {time_point}")
            path = Path(os.getcwd()) / f"thumb_{i}.png"
            self.sub_proc[i] = QtCore.QProcess(self)
            # ! Beware! As soon as you connect your signal to a lambda slot with a reference to self,
            # ! your widget will not be garbage-collected!
            # ? the question is..what do i do? --- Apparently manually disconnecting
            # ? Its PyQt5 but anyway https://www.pythonguis.com/tutorials/transmitting-extra-data-qt-signals/
            self.sub_proc[i].finished.connect(
                lambda exitCode, exitStatus, val=i: self.a_async_set_pixmap(exitCode, exitStatus, val)
            )
            # fast seeking in ffmpeg, otherwise this takes literal ages
            self.sub_proc[i].start("ffmpeg", ["-y", "-ss", time_point, "-i", a_file, "-ss", "00:00:15", "-s",
                                              "1280x720",  "-vcodec", "png", "-vframes", "1", "-an", str(path)])

    def a_async_set_pixmap(self, x_code, x_status, i):
        """
        Crudely sets the preview image of an video, QProcess.finished emits two additional parameters, namely
        exitCode and exitStatus, we need those to append additional parameters
        :param i:
        :return:
        """
        wdgt = {
            0: self.w_video_preview1,
            1: self.w_video_preview2,
            2: self.w_video_preview3
        }
        print(f"this trigger: {i}")
        if i in self.sub_proc:
            path = Path(os.getcwd()) / f"thumb_{i}.png"
            print(path)
            img = QtGui.QPixmap(str(path))
            img.scaledToHeight(200)
            wdgt[i].setPixmap(img)
            wdgt[i].setScaledContents(True)
            self.sub_proc[i].terminate()
            # creating closure for the not garbage collected lambdas?
            self.sub_proc[i].finished.disconnect()
            del self.sub_proc[i]

    def a_stderr_process(self, i):
        if i in self.sub_proc:
            data = self.sub_proc[i].readAllStandardError()
            stderr = bytes(data).decode("utf8")
            print(stderr)

    def a_stdout_process(self, i):
        if i in self.sub_proc:
            data = self.sub_proc[i].readAllStandardOutput()
            stdout = bytes(data).decode("utf8")
            print(stdout)

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

