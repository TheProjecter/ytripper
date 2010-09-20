#!/usr/bin/python

import sys
import urllib
import os
import re

#TODO:
#	YT_ripper integration
#	YT_ripper.modes - parse sys.argv
#	playlist scanning
#	clean up /tmp
#	detecting artist/title
#	writing id3

class YT_ripper:
	def __init__(self):
		self.modes = {"mp3-conversion": False, "keep-files-tmp": False, "check-playlist": False}
		self.links = []
		
		self.__parse_args()
		self.__check_links()
		
		self.params = {"playlist": None, "videos": []}
		
		self.header = {"Connection": "keep-alive", "Referer": "http://www.google.com", "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"} #usw.
		self.init_tmp()
		
		for arg in sys.argv:
			self.vid_list.append(arg)
			
		for vid in self.vid_list:
			pass
		
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
				
			else:
				# assume we got a youtube url or video id
				self.links.append(arg)
			
			
	def __check_links(self):
		for link in self.links:
			if self.modes[check-playlist]:
				# assume the given links are playlists
				#TODO
				mach_deine_playlist_check_funktion()
				# schreib die id's dann in: self.params["videos"].append(id)
			else:
				# assume the given links are all youtube links or video ids
				ident = self.__extract_ident()
				self.params["videos"].append(ident)
				
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
			print "[ ] The given URL seems to be no YouTube link, or it is a video id."
			return False
			
	def init_tmp(self):
		# create dir in /tmp and chdir
		try:
			os.mkdir("/tmp/YT_dl/")
		except:
			pass
		os.chdir("/tmp/YT_dl")
		
		return True
		
	def get_video_link(self):
		pass
		# curl link
		# self.video_link = ladida
		
	def get_video(self):
		pass
		# curl self.video_link

class regexps:
	def __init__(self):
		self.VIDEO_ID = re.compile(r'video_id=([^&]+)')
		self.T = re.compile(r'&t=([^&]+)')

class __video:
	def __init__(self, ident):
		
		#tmp
		os.chdir("/tmp")
		
		self.regexps = regexps()

		self.id = ident
		self.link = self.__gen_link(self.id)
		self.source = self.__get_source(self.url)
		self.source_file = self.__write_source_to_tmp()
		
		self.token = self.__get_token()
		self.video_id = self.__get_video_id()
		
		self.temp_dl_link = self.__gen_temp_dl_link()
		
		self.title = self.__get_title()
		
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
	
		iter = 0
		for line in new_source:
			iter += 1
		
		title = ""
		for line in range(0, iter):
			line_source = new_source[line]
			if line_source != "":
				title += str(line_source.replace("    ", ""))
			
		if title.startswith("YouTube-"): title = title[7:]
	
		while title.startswith(" ") or title.startswith("-"):
			title = title[1:]
		
		while title.endswith(" "): title = title[:-1]
	
		return title
	
	def __get_token(self):
		token_regexp = self.regexps.T
		return token_regexp.findall(self.source)[0]
	
	def __get_video_id(self):
		video_id_regexp = self.regexps.VIDEO_ID
		return video_id_regexp.findall(self.source)[0]
		
	def __gen_temp_dl_link(self):
		temp_dl_link = "http://www.youtube.com/get_video?&video_id=" + str(self.video_id) + "&t="  + str(self.token) + "&asv=3"
		return temp_dl_link
	
	def get_flv(self):
		print "[+] Downloading .flv"
		flv_link = urllib.urlopen(self.temp_dl_link)
		
		self.flv_path = str(self.id) + ".flv"
		
		flv_file = open(self.flv_path, "wb")
		flv_file.write(flv_link.read())
		
		print "[+] Seems that we got the flv!"
		
		return True
	
	def flv_to_mp3(self):
		print "[+] Converting .flv to .mp3"
		try:
			os.popen('ffmpeg  -loglevel quiet -i "' + str(self.flv_path) + '" "' + str(self.title) + '.mp3" 2>/dev/null')
			print "[+] Writing mp3-file to /tmp - maybe succeeded"
		except:
			print "[-] There was an error!"
			
	def __del__():
		pass
		#TODO: raeume in /tmp auf, an eigenen daten (der klasse)
	
new_vid = __video(sys.argv[1])

new_vid.get_flv()
new_vid.flv_to_mp3()