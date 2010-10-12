#!/usr/bin/python

# Copyright (c) 2005 by Christian Schulze - xCr4cx@googlemail.com,
# Florian Lerch - floppycode@yahoo.de 
#
# Generated: Fr 8. Okt 15:10:26 CEST 2010
#
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
#

import sys
import urllib
import os
import re

HELP = """
ytripper - Options
	\033[1mSyntax\033[m
	ytripper [OPTIONS ...] links/id's/playlist's

	\033[1mOptions\033[m
	--keep-files, -k
		Keep all temorary files in /tmp
		WARNING: If you download a whole playlist,
		there might be no free space left on your root partition!
		This CAN cause trouble, so be sure you have free space left.

	--mpeg-3-conversion, -m
		Convert the downloaded files to mp3. NOTE: the .flv files will
		be deleted! If you want to keep them, make sure you add the
		"-k" flag.

	--help, -?
		Shows this and exits
 

	\033[1mParameters\033[m
	-p, --playlist  [PLAYLISTS]
		The given playlists will be downloaded.
    	
	\033[1mExamples\033[m
	Download playlist and convert all videos to MP3.
		ytripper -m -p $PLAYLIST

	Download video, convert it to MP3 and keep the temp files in /tmp.
		ytripper -k -m $YOUTUBE-URL
"""

class YT_ripper:
	def __init__(self):
		sys.argv = sys.argv[1:]
		self.playlists = []
		self.videos = []
		self.regexps = regexps()
		self.modes = {
		"mp3-conversion": False,
		"keep-files-tmp": False,
		"check-playlist": False,
		"help_mode": False
		}
		
		self.links = []
		
		self.__parse_args()

		if self.modes["help_mode"]:
			print HELP
			sys.exit(2)

		self.__check_links()
		
		self.header = {
		"Connection": "keep-alive",
		"Referer": "http://www.google.com",
		"Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"}
		
		self.__init_tmp()
			
		if self.modes["check-playlist"]:
			# there IS now the possibility to checkout more than one pl
			for playlist in self.playlists:
				self.checkout_playlist(playlist)
		
		# the actual main process
		print "Videos:" + str(self.videos)
		for vid in self.videos:
			new_vid = video(vid, self.modes["keep-files-tmp"], self.modes["mp3-conversion"])

			# if the video class couldn't get the token or video_id, the
			# status from new_vid is 0, means that we cannot proceed
			if new_vid.status:
				new_vid.get_flv()
				
				if self.modes["mp3-conversion"]:
					new_vid.flv_to_mp3()
		
	def __parse_args(self):
		args = sys.argv
		
		for arg in args:
			if arg == "-m" or arg == "--mpeg-3-conversion":
				self.modes["mp3-conversion"] = True
			elif arg == "-p" or arg == "--playlist":
				self.modes["check-playlist"] = True
			elif arg == "-k" or arg == "--keep-files":
				# do not delete anything created in /tmp
				self.modes["keep-files-tmp"] = True
			elif arg == "-?" or arg == "--help":
				self.modes["help_mode"] = True

			else:
				# assume we got a youtube url or video id
				self.links.append(arg)
				
		return True
			
			
	def __check_links(self):
		for link in self.links:
			if self.modes["check-playlist"]:
				# assume the given links are playlists
				ids = self.checkout_playlist(link)
				for vid_id in ids:
					self.videos.append(vid_id)
			else:
				# assume the given links are all youtube links or video ids
				ident = self.__extract_ident(link)
				self.videos.append(ident)
				
		return True

		
	def __extract_ident(self, url):
		if url.count("watch?") > 0:
			# url is a path, or at least contains "watch?"
			if url.startswith("http") and url.count("youtube") > 0:
				url = url.split("/")[3]
				if url.count("&") > 0:
					url = url.split("&")[0]
				ident = url.replace("watch?v=", "")
				return ident
			else:
				print "[-]Seems to be no YouToube link!"
				return False
		else:
			# url seems to be no youtube link
			print "[-] Assuming the given parameter is a youtube video ID"
			return url			
	def __init_tmp(self):
		# create dir in /tmp and chdir
		try:
			os.mkdir("/tmp/YT_dl/")
		except:
			pass
		os.chdir("/tmp/YT_dl")
		
		return True

	def checkout_playlist(self, playlist_url):
		playlist_ids = []

		source = urllib.urlopen(playlist_url).read()
		ids_string = self.regexps.VIDEO_LIST.findall(source)[0]
		ids_string = ids_string.replace('"','')
		ids_string = ids_string.replace(' ','')
		for i in ids_string.split(','):
			playlist_ids.append(i)
		return playlist_ids

class regexps:
	def __init__(self):
		self.VIDEO_ID = re.compile(r'video_id=([^&]+)')
		self.T = re.compile(r'&t=([^&]+)')
		self.VIDEO_LIST = re.compile("'FULL_SEQUENTIAL_VIDEO_LIST': \[([^\]]+)")
		self.SPECIAL_SIGNS = re.compile("[^a-zA-Z0-9\s_]")

class amazon_tags:
	def __init__(self):
		pass

class video:
	def __init__(self, ident, cleanup=False, rmflv=False):
		self.status = 1
		self.cleanup = cleanup
		self.rmflv = rmflv #whether removing the .flv or not
		self.regexps = regexps()

		self.id = ident
		self.link = self.__gen_link(self.id)
		self.source = self.__get_source(self.link)
		self.title = self.__get_title()
		
		self.source_file = self.__write_source_to_tmp()
		
		self.token = self.__get_token()
		if not self.token:
			print "[-] Seems that this video is unavailable: " + str(self.title)
			
			self.status = 0
			
		self.video_id = self.__get_video_id()
		self.temp_dl_link = self.__gen_temp_dl_link()
			
	def __gen_link(self, video_id):
		return "http://www.youtube.com/watch?v=" + str(video_id)
	
	def __get_source(self, url):
		html_file_source = urllib.urlopen(url).read()
		
		return html_file_source
	
	def __write_source_to_tmp(self):
		html = open(str(self.id) + ".html", "w")
		html.write(self.source)
		html.close()

		return True
		
	def __get_title(self):
		source_file = self.source
		new_source = source_file.split("<title>")[1]
		new_source = new_source.split("</title>")[0]
	
		new_source = new_source.split("\n")
		
		i = 0 # iterator
		for line in new_source:
			i += 1
		
		title = ""
		for line in range(0, i):
			line_source = new_source[line]
			if line_source != "":
				title += str(line_source.replace("    ", ""))
			
		if title.startswith("YouTube-"): title = title[7:]
	
		while title.startswith(" ") or title.startswith("-"):
			title = title[1:]
		
		while title.endswith(" "): title = title[:-1]
	
		#Remove special signs
		title = self.regexps.SPECIAL_SIGNS.sub('',title)

		return title
	
	def __get_token(self):
		token_regexp = self.regexps.T
		try:
			return token_regexp.findall(self.source)[0]
		except:
			return None
	
	def __get_video_id(self):
		video_id_regexp = self.regexps.VIDEO_ID
		try:
			return video_id_regexp.findall(self.source)[0]
		except:
			return None
		
	def __gen_temp_dl_link(self):
		temp_dl_link = "http://www.youtube.com/get_video?&video_id=" + str(self.video_id) + "&t="  + str(self.token) + "&asv=3"
		return temp_dl_link
	
	def get_flv(self):
		print "[+] Downloading " + str(self.id) + ".flv"
		flv_link = urllib.urlopen(self.temp_dl_link)
		
		self.flv_path = str(self.id) + ".flv"
		
		flv_file = open(self.flv_path, "wb")
		flv_file.write(flv_link.read())
		
		print "[+] Seems that we got the flv!"
		
		return True
	
	def flv_to_mp3(self):
		print "[+] Converting .flv to .mp3"
		try:
			os.popen('ffmpeg -i "/tmp/YT_dl/' + str(self.flv_path) + '" "/tmp/YT_dl/' + str(self.title) + '.mp3" 2>/dev/null')
			print "[+] Writing mp3-file to /tmp - maybe succeeded"
		except:
			print "[-] There was an error!"
			
	def __del__(self):
		if self.cleanup:
			try:
				if self.id: os.remove(self.id + ".html") # remove the html source
			except:
				print "[-] Cannot remove source file!"
			try: 
				if self.flv_path and self.rmflv: os.remove(self.flv_path) # remove the .flv
			except:
				pass
	
instance = YT_ripper()
