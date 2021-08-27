# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 18:37:56 2019

@author: celia
"""

from mp3_tagger import MP3File
from pathlib import Path
import os
import PySimpleGUI as sg

def dir_print(to_print):
    '''Prints all the objects in the list'''
    for element in to_print:
        print(element)
    
def recursive(_dir):
    '''Find the files in the immediate directory and all sub directories 
    using a recursive method'''
    main_folder = Path(_dir)
    dir_list = []
        
    for path_name in main_folder.iterdir():   
        sub_dir = Path(path_name)    
        dir_list.append(path_name)
        
        if sub_dir.is_dir():
            dir_list.append(recursive(path_name))
    
    return dir_list

def function_recursion(dir_list, opt, function):
    for obj in dir_list:
        if type(obj) == list:
            function_recursion(obj, opt, function)
            
        else:
            try:
                function(obj, opt)
                
            except:
                print('Invalid')
                
def conflict_delete(obj, opt):
    new_obj = str(obj.absolute().as_posix())
    if (opt) in new_obj:
        print('Deleted:', new_obj)
        os.remove(new_obj)

def album_change(obj, opt):
    album_name = ''
    new_obj = str(obj.absolute().as_posix())
    album_name = new_obj.split('/')[-2]                
    if ('.mp3') in new_obj and ('.asd') not in new_obj:
        mp3 = MP3File(new_obj)
        if mp3.album != album_name:
            mp3.album = album_name
            mp3.save()
            print(f"{obj}, Album: {album_name}")
        
def auto_artist_set(obj, opt):
    new_obj = str(obj.absolute().as_posix())
    song_name = new_obj.split('/')[-1]
    if ('.mp3') in new_obj and ('.asd') not in new_obj and '-' in song_name:
        artist = song_name.split('-')[0]
        mp3 = MP3File(new_obj)
        mp3.artist = artist
        mp3.save()
        print(f'{new_obj} Artist: {artist}')
        
    elif ('.mp3') in new_obj and ('.asd') not in new_obj and '-' not in song_name:
        mp3 = MP3File(new_obj)
        del mp3.artist
        mp3.save()
                
def remove_excess_name(obj, remove):
    new_obj = str(obj.absolute().as_posix())
    if remove in new_obj:
        os.rename(new_obj, new_obj.replace(remove, ''))
        print('New Name:', new_obj.replace(remove, ''))
        
def append_name_from_left(obj, add):
    new_obj = str(obj.absolute().as_posix())
    path_list = new_obj.split('/')
    path_list[-1] = add + path_list[-1]
    new_path = ''.join(path_list)
    os.rename(new_obj, new_path)
    print('New Name:', new_path)
                
def remove_excess_tag(obj, remove):
    new_obj = new_obj = str(obj.absolute().as_posix())
    if ('.mp3') in new_obj and ('.asd') not in new_obj:
        mp3 = MP3File(new_obj)
        # tag_dict = mp3.get_tags()['ID3TagV1']
        # if tag_dict['song'] != None or tag_dict['genre'] != None or tag_dict['track'] != None or tag_dict['comment'] != None or tag_dict['year'] != None or tag_dict['artist'] != None:
        del mp3.album
        del mp3.song
        del mp3.genre
        del mp3.track
        del mp3.comment
        del mp3.year
        del mp3.artist
        print(f'Deleted Tags On: {obj}')
        mp3.save()
        
            
def gui_create():
    sg.theme('Dark Blue 3')  # please make your creations colorful

    layout = [  [sg.Text('Filename')],
                [sg.Input(''), sg.FolderBrowse()],
                [sg.Combo(['Album Change', 
                           'Auto Artist', 
                           'Append Name From Left',
                           'Conflict Delete',
                           'Remove Excess Name', 
                           'Remove Excess Tags'], size=(30, 6))],
                [sg.Input()],
                [sg.OK(), sg.Cancel()]] 
    
    window = sg.Window('Album/File Mass Organization Tool', layout)
    
    while True:
        event, values = window.Read()
        if event is None or event == 'Cancel':
            break
        
        dir_list = recursive(values[0])
        
        switch_statement(values[1], values[2], dir_list)
        
    window.close()

def switch_statement(args, opt, dir_list):
    dictionary = {'Album Change': album_change,
                  'Auto Artist': auto_artist_set,
                  'Append Name From Left': append_name_from_left,
                  'Conflict Delete': conflict_delete,
                  'Remove Excess Name': remove_excess_name,
                  'Remove Excess Tags': remove_excess_tag
                }
    
    function = dictionary.get(args, lambda: 'Invalid')
    function_recursion(dir_list, opt, function)
            
if __name__ == "__main__":
    gui_create()
    
    