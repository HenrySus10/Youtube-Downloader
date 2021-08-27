# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 18:05:29 2020

@author: celia
"""

import youtube_dl
import PySimpleGUI as sg

# ydl_opts = {}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download()

def mp4(url, directory):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
        'outtmpl': directory + '/' + '%(title)s.mp4',
        'noplaylist': False
    }
    
    download(url, ydl_opts)
    
def mp3(url, directory):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': directory + '/' + '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False,
    }
    
    download(url, ydl_opts)
    
def download(url, ydl_opts):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
def gui_create():
    sg.theme('Dark Blue 3')  # please make your creations colorful

    layout = [  [sg.Text('Youtube URL')],
                [sg.Input('')],
                [sg.Text('Output Directory')],
                [sg.Input(''), sg.FolderBrowse()],
                [sg.OK(), sg.Cancel(), sg.Listbox(['mp3', 'mp4'], size=(10, 3), default_values='mp3')]]
    
    window = sg.Window('Youtube Downloader', layout)
    
    while True:
        event, values = window.Read()
        if event is None or event == 'Cancel':
            break
        try:
            switch_statement(values[2][0], values[1], values[0])
        except:
            print("Can't Complete Action")
        
    window.close()
    
def switch_statement(args, directory, url):
    dictionary = {'mp3': mp3,
                  'mp4': mp4
                }
    
    function = dictionary.get(args, lambda: 'Invalid')
    function(url, directory)
    
if __name__ == '__main__':
    gui_create()