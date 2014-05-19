#!/usr/bin/python

from AbletonPlaylistExporter import *
import Tkconstants
import Tkinter
import tkFileDialog

class AbletonPlaylistExporterGUI(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        Tkinter.Button(self, text='Export playlist...', command=self.export_playlist).pack(**button_opt)

        self.als_opt = {}
        self.als_opt['defaultextension'] = '.als'
        self.als_opt['filetypes'] = [('Ableton Live Set', '*.als')]
        self.als_opt['title'] = 'Select the Ableton Live Set to export'

        self.txt_opt = {}
        self.txt_opt['defaultextension'] = '.txt'
        self.txt_opt['filetypes'] = [('Text file', '*.txt')]
        self.txt_opt['title'] = 'Playlist destination'

    def export_playlist(self):
        filename = tkFileDialog.askopenfilename(**self.als_opt)
        if filename:
            exporter = AbletonPlaylistExporter(filename)
            outFile = tkFileDialog.asksaveasfile(**self.txt_opt)
            outFile.write(exporter.export())
            outFile.close()

if __name__ == '__main__':
    root = Tkinter.Tk()
    AbletonPlaylistExporterGUI(root).pack()
    root.mainloop()