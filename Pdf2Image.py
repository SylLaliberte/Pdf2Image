import PySimpleGUI as sg 
from pdf2image import convert_from_path
import os
from PIL import Image
from pathlib import Path 
import numpy as np
import sys

mypath = Path().absolute()
poppler_path=mypath/'Library'/'bin'
saving_folder = mypath

def convertToImg ():
    global newImg, img
    pdf_path= sg.popup_get_file('Open', no_window = True, default_extension='pdf')

    # pdf to image conversion
    pages = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path,dpi=600, single_file=True)

    # save pages in separate files
    c=1
    for page in pages:
        img_name=f"img-{c}.png"
        page.save(os.path.join(saving_folder, img_name), "PNG")
        c+=1

    # open image and crop then, convert image to a list of pixels
    img = Image.open(mypath/'img-1.png').crop((330,280,1650,2280)) #crop 300dpi = (165,140,825,1140) 600dpi=330,280,1650,2280 1200dpi=660,560,3300,4560
    pixels = list(img.getdata())

    # convert data list to contain only black or white
    threshold = 235
    newPixels = []
    for pixel in pixels:
        # if looks like black, convert to black
        if pixel[0] <= threshold:
            newPixel = (0, 0, 0)
        # if looks like white, convert to white
        else:
            newPixel = (255, 255, 255)
        newPixels.append(newPixel)

    # create a image and put data into it
    newImg = Image.new(img.mode, img.size)
    newImg.putdata(newPixels)
    newImg.show()
    return newImg
    
# control_col =   sg.Column([
#                     [sg.Text("'Nouvelle image' pour convertir un pdf", justification= 'center')],
#                     [sg.Text("Appuyer sur 'Enregistrer' pour sauvegarder l'image", justification= 'center')],
#                     [sg.Button('Nouvelle image', key = '-LOAD-', expand_x=True)],
#                     [sg.Button('Enregistrer', key = '-SAVE-', expand_x=True)],
# ])
    
#image_col = sg.Column([[sg.Image(img, key = '-IMAGE-')]])

def create_window(theme):
    sg.theme(theme)
    sg.set_options(font = 'Franklin 16')
    layout = [[sg.Push(),sg.Text("'Nouvelle image' pour convertir un pdf en image", justification= 'center'),sg.Push()],
                [sg.Push(),sg.Text("Appuyer sur 'Enregistrer' pour sauvegarder l'image", justification= 'center'),sg.Push()],
                [sg.Push(),sg.Button('Nouvelle image', key = '-LOAD-'),sg.Push()],
                [sg.Push(),sg.Button('Enregistrer', key = '-SAVE-', expand_x=False),sg.Push()],
                [sg.Push(),sg.Text("*Au moment d'enregistrer, ne pas écrire '.png' suite au nom de l'image", justification= 'center'),sg.Push()]]
    return sg.Window('Convertisseur PDF en image', layout)

window = create_window('Reddit')

while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break

    if event == '-LOAD-':
        convertToImg()
            

    if event == '-SAVE-':
        file_path = sg.popup_get_file('Save as', no_window=True, save_as = True) + '.png'
        newImg.save(file_path,'PNG')
        
window.close()