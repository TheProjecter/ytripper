#!/bin/bash python
#from mutagen.mp3 import MP3
import os
import sys
import ID3


class ID3Edit:
	def __init__(self):
		self.help_string = '''
			ID3Edit - Options
			
			\033[1mSyntax\033[m
			    id3edit [OPTIONS ...] [FILES ...] [PARAMETERS ...]
			
			\033[1mOptions\033[m
			    --copy, -c
			    	Make copies of all the files when changing something (default)
			    	
			    --nocopy, -n
			    	Do not make a copy of the original file, when chaning something.
			    	Instead write changes to the original file
			    	
			    -w
			        Write ID3tags as specified in the parameters (watch below)
			        (If you use this option, only the first given file will be
			        processed)
	    
			    -a
			        Write ID3tags as specified in the parameters to all given files
			        (e.g. a whole directory)
			        
			    --help, -?
			    	Shows this and exits
	    
	    
			\033[1mParameters\033[m
			    --artist=ARTIST, -i=ARTIST
			        Specify artist
			        
			    --album=ALBUM, -b=ALBUM
			    	Specify album
			    	
			    --title=TITLE, -t=TITLE
			        Specify title
			       
			    --file-name=FILENAME, -f=FILENAME
			    	Specify name of the output file (NOTE: it will be a copy, even
			    	with -n)
    	
    	
			\033[1mExamples\033[m
    			Set the artist for all given files and write the output to the
			    original file:

			        id3edit -a -n  /path/to/dir -i "Name of the artist" 
		'''
			
		self.args = sys.argv[1:]
		
		if self.is_help(self.args):
			print self.help_string
			sys.exit()
			
		# defining the default values
		self.modes = {"copy": True, "write_mode": False, "write_all": False}
		self.params = {"artist": None, "album": None, "title": None, \
		"file_name": None}
		self.files = []
		
		# parse the given arguments
		self.parse_options(self.args)
			
	def is_help(self, args):
		help = False
		for arg in args:
			if arg == "--help" or arg == "-?":
				help = True
				
		return help

	def parse_options(self, args):
		for arg in args:
			# first check for params
			if arg.startswith("-i="):
				artist = arg.replace("-i=", "").replace('"', '')
				self.params["artist"] = artist
			elif arg.startswith("--artist"):
				artist = arg.replace("--artist=", "").replace('"', '')
				self.params["artist"] = artist
			
			elif arg.startswith("-b="):
				album = arg.replace("-b=", "").replace('"', '')
				self.params["album"] = album
			elif arg.startswith("--album="):
				album = arg.replace("--album=", "").replace('"', '')
				self.params["album"] = album
			
			elif arg.startswith("-t="):
				title = arg.replace("-t=", "").replace('"', '')
				self.params["title"] = title
			elif arg.startswith("--title="):
				title = arg.replace("--title=", "").replace('"', '')
				self.params["title"] = title
			
			elif arg.startswith("-f="):
				file_name = arg.replace("-f=", "").replace('"', '')
				self.params["file_name"] = file_name
			elif arg.startswith("--file-name="):
				file_name = arg.replace("--file-name=", "").replace('"', '')
				self.params["file_name"] = file_name
			
			# check for modes
			elif arg == "--copy":
				self.modes["copy"] = True
			elif arg == "-c":
				self.modes["copy"] = True
						
			elif arg == "--nocopy":
				self.modes["copy"] = False
			elif arg == "-n":
				self.modes["copy"] = False
						
			elif arg == "-w":
				self.modes["write_mode"] = True
			elif arg == "-a":
				self.modes["write_all"] = True
				self.modes["write_mode"] = True
						
			else:
				if os.path.isdir(arg):
					print "[+] Checking dir " + str(arg)
					path = arg
					if not path.endswith("/"): path = path + "/"
					
					files = os.listdir(path)
				
					for mfile in files:
						mfile = mfile.upper()
						fiter = 0
						if mfile.endswith("MP3"):
							fiter += 1
							self.files.append(path + f)
						
					if not fiter:
						print "[-] No valid files found in directory " + str(path)
					
				elif os.path.exists(arg):
					self.files.append(arg)
				else:
					print "[-] Not a valid file or directory: " + str(arg)
		
		return

	def print_tags(self, fpath):
		audio = ID3.ID3(fpath)
	
		#artist
		if audio.has_key('ARTIST'):
			print "Artist:        ", audio['ARTIST']
		else:
			print "Artist:        ", "-"	
		
		#title
		if audio.has_key('TITLE'):
			print "Title:         ", audio['TITLE']
		else:
			print "Title:         ", "-"
		
		#album
		if audio.has_key('ALBUM'):
			print "Album:         ", audio['ALBUM']
		else:
			print "Album:         ", "-"
			
		#year
		if audio.has_key('YEAR'):
			print "Year:          ", audio['YEAR']
		else:
			print "Year:          ", "-"
	
		#genre
		if audio.has_key('GENRE'):
			print "Genre:         ", audio['GENRE']
		else:
			print "Genre:         ", "-"
		
		#tracknumber
		if audio.has_key('TRACKNUMBER'):
			print "Tracknumber:   ", audio['TRACKNUMBER']
		else:
				print "Tracknumber:   ", "-"
	
		#comment
		if audio.has_key('COMMENT'):
			print "Comment:       ", audio['COMMENT']
		else:
			print "Comment:       ", "-"
		
		#filesize
		fsize = float(os.path.getsize(fpath))
	
		if fsize >= 1048576:
			fsize = fsize/1048576
			measure = "MB"
		elif fsize >= 1024:
			fsize = fsize/1024
			measure = KB
		print "Size:          ", fsize, measure
		
		#filename
		print "File:          ", fpath
	
		print "============================================================"

if __name__ == "__main__":
	tagedit = ID3Edit()

	# write_mode
	if tagedit.modes["write_mode"]:
		print "[+] Entered writing mode"
		
		if tagedit.modes["write_all"]:
			# write_all is True
			print "[+] Writing given information to all files"
			
			if len(tagedit.files):
				# has valid files
				for f in tagedit.files:
					print f #2come
			else:
				# no files given
				print "[-] Fatal Error: No valid files given"
				sys.exit()
		else:
			print "[+] Writing information to first given file"
			vic = tagedit.files[0]
			print vic
			
			if tagedit.params["file_name"]:
				print os.popen('cp "' + str(vic) + '" "' + str(tagedit.params["file_name"]) + '_new"').read()
				vic = tagedit.params["file_name"]
				
			if tagedit.modes["copy"]:
				os.popen('cp "' + str(vic) + '" "' + str(vic) + '_new"')
				vic = str(vic) + "_new"
					
			track = ID3.ID3(vic)
			
			for info in tagedit.params:
				if info == "album" and tagedit.params["album"]:
					track["ALBUM"] = tagedit.params["album"]
					print "[+] Written ALBUM '\
" + str(tagedit.params["album"]) + "' to file " + str(tagedit.files[0])

				elif info == "artist" and tagedit.params["artist"]:
					track["ARTIST"] = tagedit.params["artist"]
					print "[+] Written ARTIST '\
" + str(tagedit.params["artist"]) + "' to file " + str(vic)

				elif info == "title" and tagedit.params["title"]:
					
	else:
		# readonly mode
		if len(tagedit.files):
			print "[+] Printing information of given files"
			for f in tagedit.files:
				try:
					tagedit.print_tags(f)
				except:
					print "[-] Could not print information of file " + str(f)
		else:
			print "[-] No files, aborting"
			sys.exit()