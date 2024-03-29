#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.


import zipfile as zf
from PIL import Image
import pytesseract as pt
import cv2 as cv
import numpy as np
from IPython.display import display
#from io import StringIO

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('readonly/haarcascade_eye.xml')
images_zip = "readonly/images.zip"
small_zip = 'readonly/small_img.zip'

def cropping_faces(pil_img,faces,filename):
    
    
    print("Results found in file {}".format(filename))  
    
    if len(faces)==0:
        print("But there were no faces in that file!")
    else:
        row_n = len(faces)//5 + int(len(faces)%5 != 0)
        print(pil_img.size)
        contact_sheet = Image.new(mode = 'RGB', size=(500,100 * row_n))
    
        i,j = 0,0
        for x,y,w,h in faces:
            
            face = pil_img.crop(box=(x,y,x+w,y+h))
            
            face.thumbnail(size=(100,100))
            if i>=5:
                i=0
                j += 1
            contact_sheet.paste(face,box = (i*100,j*100))
            i += 1
        display(contact_sheet)
        
def text_scrub(pil_img):
    img = pil_img.convert('1')
    pt.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    return pt.image_to_string(img)



def build_data(image_zip):
    
    with zf.ZipFile(image_zip) as img_files:
    
        zip_data = []
        
        
        zfiles = img_files.namelist()
        print("there are {} files in the zip".format(len(zfiles)))
        
        for zfile in zfiles[0:]: 
            img_data={}
            print("now it is file {} ".format(zfile))
            img_data['filename'] = zfile
          
            im_buffer = img_files.read(zfile) 
            cv_array = cv.imdecode(np.frombuffer(im_buffer,np.uint8),cv.IMREAD_GRAYSCALE)
             
            faces = face_cascade.detectMultiScale(cv_array,scaleFactor = 1.30,minNeighbors = 5, minSize = (50,50))
            img_data['faces'] =faces
            with Image.open(img_files.open(zfile)) as pil_img:    
                img_data['text']= text_scrub(pil_img)
            
            zip_data.append(img_data)
            print("there are {} items in the zip_info".format(len(zip_data)))
            #
            #print(zip_data)
            
    return zip_data

def word_around_face(image_zip,word):
    zip_info = build_data(image_zip)
    
    with zf.ZipFile(image_zip) as img_files:
    
        for image in zip_info:
            if word in image['text']:
                with Image.open(img_files.open(image['filename'])) as pil_img:
                    cropping_faces(pil_img,image['faces'],image['filename'])
            else:
                print("For {}: The word we look for is not here!".format(image['filename']))
    
   
word_around_face(images_zip,'Mark')          
#word_around_face(small_zip,'Christopher')           
