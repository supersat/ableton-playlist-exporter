#!/usr/bin/python

# WARNING: This program is vulnerable to DoS attacks by malicious ALS files.
# See https://docs.python.org/2/library/xml.html#xml-vulnerabilities
# Run only on trusted Ableton sets.

import argparse
import gzip
import mutagen
import os
import sys
import xml.etree.ElementTree as ET

class AbletonPlaylistExporter:
    def __init__(self, filename):
        self._filename = filename

    def export(self):
        songs = []
        alsTree = ET.parse(gzip.open(self._filename, 'rb'))
        clips = alsTree.findall('./LiveSet/Tracks/AudioTrack/DeviceChain/MainSequencer/Sample/ArrangerAutomation/Events/AudioClip')
        for clip in clips:
            startTime = clip.find('CurrentStart').get('Value')
            fileRef = clip.find('./SampleRef/FileRef')
            fileRefType = fileRef.find('Type').get('Value')
            if fileRefType == 1: # Windows file ref?
                fileRefData = ''.join(fileRef.find('Data').text.split())
                fileName = fileRefData.decode('hex')[0:-2].decode('utf16')
            else: # OSX file ref?
                pathParts = [part.get('Dir') for part in fileRef.findall('./SearchHint/PathHint/RelativePathElement')]
                fileName = os.sep + os.sep.join(pathParts) + os.sep + fileRef.find('Name').get('Value')
            song = {'timestamp': float(startTime), 'filename': fileName, 'title': fileName, 'artist': '', 'album': '' }
            try:
                metadata = mutagen.File(fileName, easy=True)
                if 'album' in metadata:
                    song['album'] = metadata['album'][0]
                if 'artist' in metadata:
                    song['artist'] = metadata['artist'][0]
                if 'title' in metadata:
                    song['title'] = metadata['title'][0]
            except:
                pass
            songs.append(song)
        playlist = ''
        songs = sorted(songs, key=lambda k: k['timestamp'])
        for song in songs:
            playlist = playlist + '%s\t%s\t%s\t%s\n' % (song['timestamp'], song['artist'], song['title'], song['album'])
        return playlist

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Filename of an Ableton Live Set (.als) file')
    args = parser.parse_args()
    exporter = AbletonPlaylistExporter(args.filename)
    print exporter.export()