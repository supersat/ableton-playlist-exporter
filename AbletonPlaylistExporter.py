#!/usr/bin/python

# WARNING: This program is vulnerable to DoS attacks by malicious ALS files.
# See https://docs.python.org/2/library/xml.html#xml-vulnerabilities
# Run only on trusted Ableton sets.

import argparse
import gzip
import mutagen
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
            fileRefData = ''.join(fileRef.find('Data').text.split())
            fileName = fileRefData.decode('hex').decode('utf16')
            metadata = mutagen.File(fileName, easy=True)
            song = {'timestamp': float(startTime), 'filename': fileName }
            if 'album' in metadata:
                song['album'] = metadata['album'][0]
            else:
                song['album'] = ''
            if 'artist' in metadata:
                song['artist'] = metadata['artist'][0]
            else:
                song['artist'] = ''
            if 'title' in metadata:
                song['title'] = metadata['title'][0]
            else:
                song['title'] = ''
            songs.append(song)
        songs = sorted(songs, key=lambda k: k['timestamp'])
        for song in songs:
            print '%s\t%s\t%s\t%s' % (song['timestamp'], song['artist'], song['title'], song['album'])

if __name__ == '__main__':
    exporter = AbletonPlaylistExporter(sys.argv[1])
    exporter.export()