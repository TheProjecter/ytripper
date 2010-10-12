#!/usr/bin/python

# Copyright (c) 2005 by Christian Schulze - xCr4cx@googlemail.com
#
# Generated: Fr 8. Okt 15:10:26 CEST 2010
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA

import re
import sys

class playlist_crawler:
	"""
		base class for the playlist-check.

		subclasses: __regex, __playlist
	"""
	def __init__(self):
		self.url = None
		self.__parse-args()

		if self.url:
			self.playlist = __playlist(self.url)
		else:
			print "[-] No playlist"
			sys.exit(0)

	def __parse_args(self):
		for arg in sys.argv:
			if arg.count("youtube.com/") > 0:
				self.url = arg
			else:
				print "[-] No valid playlist url given"
				sys.exit(0)

class __regex:
	def __init__(self):
		self.extract_playlist_videos = re.compile("'FULL_SEQUENTIAL_VIDEO_LIST': \[([^\]]+)")

class __playlist:
	"""
		subclass of playlist_crawler

		subclasses: video
	"""
	def __init__(self, url):
		self.ids = [] 
