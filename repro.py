import sublime
import sublime_plugin

from enum import Enum
import traceback #debug

import subprocess
import sys

from pathlib import Path
import os

### LOGGING ###

LOG_INPUT_PANEL = "input-panel"
# LOG_INPUT_PANEL = None

LOG_TO_FILE = True

def plugin_loaded():
	if LOG_TO_FILE:
		with open('plugin_trace.txt','w') as file:
		    pass	# NOTE - Clears file

def trace(tag, text):
	if tag:
		if LOG_TO_FILE:
			# SLOW - opening file every time we log, lol
			with open('plugin_trace.txt', 'a') as file:
				file.write(f"[{tag}] {text}\n")
		else:
			print(line)

### INPUT PANEL ###

class InputPanelMgr():
	window_dict = {}
	ELEMENT_NAME = "input:input"

	def __init__(self, window):
		self.window = window
		self.view = None

	@staticmethod
	def get(window):
		result = InputPanelMgr.window_dict.get(window.id())

		if result is None:
			result = InputPanelMgr(window)
			InputPanelMgr.window_dict[window.id()] = result

		return result

	def on_deactivated(self):
		trace(LOG_INPUT_PANEL, "on_deactivated(..)")
		if self.is_showing():
			trace(LOG_INPUT_PANEL, "\tcalling close(..)")
			self.close()

	def is_showing(self):
		return self.view and self.view.window()

	def open(self):
		trace(LOG_INPUT_PANEL, "open(..)")
		if self.is_showing():
			trace(LOG_INPUT_PANEL, "\tcalling focus_view(..)")
			self.window.focus_view(self.view)
		else:
			trace(LOG_INPUT_PANEL, "\tcalling show_input_panel(..)")
			self.view = self.window.show_input_panel("i-panel", "", self.on_done, None, self.on_cancel)
			trace(LOG_INPUT_PANEL, "\tself.view = " + str(self.view))

	def close(self):
		trace(LOG_INPUT_PANEL, "close(..)")
		if self.is_showing():
			trace(LOG_INPUT_PANEL, '\tcalling run_command("hide_panel")')
			self.view.window().run_command("hide_panel")

	def on_done(self, text):
		trace(LOG_INPUT_PANEL, "on_done(..)")

	def on_cancel(self):
		trace(LOG_INPUT_PANEL, "on_cancel(..)")

class OpenInputPanel(sublime_plugin.TextCommand):
	def run(self, edit):
		input_panel = InputPanelMgr.get(self.view.window())
		input_panel.open()

class MyEventListener(sublime_plugin.EventListener):
	def on_deactivated(self, view):
		if view.element() == InputPanelMgr.ELEMENT_NAME:
			input_panel = InputPanelMgr.get(view.window())
			input_panel.on_deactivated()
