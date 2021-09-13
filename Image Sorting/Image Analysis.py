import cv2
from PIL import Image
import face_recognition
import requests
import webbrowser
from bs4 import BeautifulSoup
import pandas as pd
import io
import urllib.request
import os
import shutil

image_loc = './test jpg'

def FR_cnn_method():
    image_url = image_loc + '/0eyub1ghdxu21.jpg'
    image = face_recognition.load_image_file(image_url)

    # Find all the faces in the images using a pre-trained convolutional neural network.
    # This method is more accurate than the default HOG model, but it's slower
    # unless you have an nvidia GPU and dlib compiled with CUDA extensions. But if you do,
    # this will use GPU acceleration and perform well.
    # See also: find_faces_in_picture.py
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    for face_location in face_locations:
    
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        print(type(pil_image))
        pil_image.save(image_loc + '/face.jpg')
        face_url = image_loc + '/face.jpg'
        Reverse_Image_search(face_url)

# Function input needs to be changed 
def Reverse_Image_search(image):

    filePath = image
    searchUrl = 'https://www.google.com.au//searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    print(fetchUrl)
    # Perform the request
    request = urllib.request.Request(fetchUrl)

    # Set a normal User Agent header, otherwise Google will block the request.
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()

    # Read the repsonse as a utf-8 string
    html = raw_response.decode("utf-8")

    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('input').get('value')
    print(name)
    # current_dir = image_loc
    #file_sorter(image_loc, name)

## Fix image sorting after Identity has been identified
## Add code to check if id is already known
    
def file_sorter(path, name):
    list_ = os.listdir(path)

    # This will go through each and every file
    for file_ in list_:
        name, ext = os.path.splitext(file_)
    
        # This is going to store the extension type
        ext = ext[1:]
    
        # This forces the next iteration,
        # if it is the directory
        if ext == '':
            continue
    
        # This will move the file to the directory
        # where the name 'ext' already exists
        if os.path.exists(path+'/'+name):
            shutil.move(path+'/'+file_, path+'/'+name+'/'+file_)
    
        # This will create a new directory,
        # if the directory does not already exist
        else:
            os.makedirs(path+'/'+name)
            shutil.move(path+'/'+file_, path+'/'+name+'/'+file_)

if __name__ == '__main__':
    FR_cnn_method()


