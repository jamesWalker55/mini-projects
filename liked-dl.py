# liked-dl.py Downloads liked videos' audio and adds metadata

# Just run, it will open a browser window for authenication
# Then the browser will fail to connect: Copy the url and paste to the prompt

import youtube_dl
import pyyoutube
import webbrowser  # to open link in browser automatically
import os, fnmatch  # for listing all songs in a folder
import mutagen  # audio tag handling
from pprint import pprint
import time

# ===================== SETTINGS =====================
# The most recent X videos will be checked and downloaded
numVideos = 100
# Where to download and process files
path = r"D:\Programming\youtube-dl liked videos\YouTube Liked Music" + "\\"
archivePath = r'D:\Programming\youtube-dl liked videos\archive.txt'
downloadPath = r"D:\Programming\youtube-dl liked videos\processing" + "\\"
finalPath = r"D:\Soundtracks\YouTube Liked Music" + '\\'

youtube_base = r"https://www.youtube.com/watch?v="
client_id = "139956475808-h70vgd19l1anpqpj5m1ctafsqp5sk3c2.apps.googleusercontent.com"
client_secret="Tmbp7B9vRx1fPPvQvs1tk0or"

# ===================== Archive functions =====================
def loadArchiveFile(archivePath):
	with open(archivePath) as f:
		archive = []
		for line in f:
			archivedLink = line.strip("\n")
			archive.append(archivedLink)
	return archive

def checkInArchive(archive, link):
	if link in archive:
		return True
	else:
		return False

def addToArchiveFile(link):
	with open(archivePath, 'a') as f: # open file in "append" mode
		f.write("{}\n".format(link))


# ===================== Get API approval =====================
# youtube api shit
api = pyyoutube.Api(client_id=client_id, client_secret=client_secret)

webbrowser.open(api.get_authorization_url()[0], new=1, autoraise=True)

print("Please input the authorization response: (Input 'quit' to quit)")
auth = input(" > ")

if auth.lower() == 'quit':
	print("'quit' detected, exiting program...")
	quit()

token = api.exchange_code_to_access_token(authorization_response=auth)

# ===================== Get playlist =====================
print("Getting 'Liked Videos' playlist")
playlistItems = api.get_playlist_items(
	playlist_id="LLCYDWQLKkmjFj90-k8j8r6Q", 
	parts="snippet", 
	return_json=True, 
	count=numVideos, 
	limit=50)

playlist_dict = {}
title_list = []
for i in range(len(playlistItems["items"])):
	snippet = playlistItems["items"][i]["snippet"]
	title = snippet["title"]
	date = snippet["publishedAt"]
	videoId = snippet["resourceId"]['videoId']
	playlist_dict[videoId] = {"date": date, "title": title}


# # Example of "snippet"
# {'publishedAt': '2020-05-24T03:14:29Z',
#  'channelId': 'UCCYDWQLKkmjFj90-k8j8r6Q',
#  'title': '伊東歌詞太郎 - 僕は初音ミクとキスをした',
#  'description': 'Song : 僕は初音ミクとキスをした\nVocal : 伊東歌詞太郎\nProducer : みきとP\nAlbum : 二律背反',
#  'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/577CqLcX4k4/default.jpg',
#    'width': 120,
#    'height': 90},
#   'medium': {'url': 'https://i.ytimg.com/vi/577CqLcX4k4/mqdefault.jpg',
#    'width': 320,
#    'height': 180},
#   'high': {'url': 'https://i.ytimg.com/vi/577CqLcX4k4/hqdefault.jpg',
#    'width': 480,
#    'height': 360}},
#  'channelTitle': 'Wong Chun Ho',
#  'playlistId': 'LLCYDWQLKkmjFj90-k8j8r6Q',
#  'position': 24,
#  'resourceId': {'kind': 'youtube#video', 'videoId': '577CqLcX4k4'}}

# # Sample playlist_dict for testing
# playlist_dict = {'8RYQBFvcG4E': {'date': '2020-07-98T06:05:03Z', 'title': 'test video 1'},
# 'mqLFH4MXMOY': {'date': '2020-07-99T06:05:03Z', 'title': 'test video 2'},
# '5xHpBN3TnA0': {'date': '2020-07-31T06:05:03Z', 'title': 'aaa'}, 
# 'eSnmkVB-olE': {'date': '2020-07-30T08:54:09Z', 'title': 'bbb'}, 
# 'bBIZ7tt3S_Y': {'date': '2020-07-30T07:48:18Z', 'title': 'ccc'}}

# ===================== Find new videos =====================
print("Finding new videos in playlist, comparing to archive...")
archive = loadArchiveFile(archivePath)
to_download = []
for videoId in playlist_dict:
	if not videoId in archive:
		to_download.append(videoId)

print("New videos detected:")
pprint(to_download)

# ===================== Fix for youtube random errors =====================

def tryError():
	# returns False when there is no error
	# returns True when it errors
	try:
		temp = mutagen.File(downloadPath + os.listdir(downloadPath)[0])
		return False
	except IndexError:
		return True


# ===================== Start Downloading =====================
for i in range(len(to_download)):
	print("Downloading video: {}".format(to_download[i]))
	command = 'youtube-dl -f "(bestaudio[acodec=opus]/bestaudio)/best" -q --extract-audio -o "{}%(title)s.%(ext)s" {}'
	command = command.format(downloadPath,youtube_base + to_download[i])
	# YouTube now randomly errors with "YouTube said: Unable to extract video data"
	# This is a short fix that repeats the command until it works
	while tryError():
		os.system(command)
		time.sleep(2)
	opened_file = mutagen.File(downloadPath + os.listdir(downloadPath)[0])
	opened_file["album"] = 'Youtube Liked Playlist'
	opened_file["title"] = playlist_dict[to_download[i]]["title"]
	opened_file["date"] = playlist_dict[to_download[i]]["date"]
	opened_file.save()
	fromFile = downloadPath + os.listdir(downloadPath)[0]
	toFile = finalPath + os.listdir(downloadPath)[0]
	os.rename(fromFile, toFile)
	addToArchiveFile(to_download[i])


