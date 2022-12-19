# -*- coding: utf-8 -*-
"""
GUI for transcribing Entry Form

Form collects Name, Phone No., Address (I'm capturing name only')
Member Y/N
Entries:
    Class
    Description  (display from class)
    1/2
Total entries count

@author: Mark
"""

from PySimpleGUI import Window, T, Text, Input, Button, WIN_CLOSED


layout = [
    [T('Entry Form', font='_ 14', justification='c', expand_x=True)],
    [Text("Name"), Input()],
    [Text('Class'), Input()],
    [Button('Save'), Button('Cancel')]
]
window = Window("Badenoch Gardening Club Show",
                layout, finalize=True)
while True:
    event, values = window.read()
    print(event, values)
    # If user closed window with X or if user clicked "Exit" button then exit
    if event == WIN_CLOSED:
        break
window.close()
