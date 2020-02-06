# Import requests, shutil python module.
#copy the image-Sentiment-polarity-DFE.csv to current directory -same as the python file.
#
import requests
import shutil
import os
import pathlib
import pandas as pd
import numpy as np
import glob
import datetime
#Import 'image_resize_zee' for resize function
from image_resize_zee import image_resize

print(datetime.datetime.now())
default_dir = os.getcwd()
filelist = glob.glob(default_dir + "\\*.jpg")
                     #clean up default directory "\\*.jpg")
for file in filelist:
     os.remove(file)

#Get the current directory and set the target directory for download images
curr_dir=pathlib.Path(__file__).resolve().parent
tgt_dir = str(curr_dir) + "\\" + 'dwnld'
if not os.path.exists(tgt_dir):
    os.makedirs(tgt_dir)

#create target resize dir under download (tgt_dir)
rsize_dir=str(curr_dir) + "\\" + 'rsize'
if not os.path.exists(rsize_dir):
    os.makedirs(rsize_dir)

#setting the log file to capture the steps of downloading images
file1 = open(tgt_dir + "\\download.log","w")
file1.write(str(datetime.datetime.now()) + "\n")

#read the csv file of the metadata of the download images
image_file_raw = pd.read_csv(str(curr_dir) + "\\" + "image-Sentiment-polarity-DFE.csv")
image_file = image_file_raw.iloc[:,0:9]

#image_file = image_file_1[(image_file_1['_unit_id'] >= 694551359) & (image_file_1['_unit_id'] <= 694551370)]
#image_file = image_file_1[(image_file_1['_unit_id'] >= 694551359) & (image_file_1['_unit_id'] <= 694551370)]
file_range = image_file.count
#add two new columns for flagging images exist and filename
image_file['image_exists']="NA"
image_file['file_name']="NA"

file1.write(tgt_dir + "--\n")

#For loop to download each image, flag when the return code is not 200
#for i in range(len(image_file)):
for i in range(10):
    #print(i)
    file1.write(str(i))
    image_url = image_file.iloc[i, 7]
   # image_url = "https://farm1.static.flickr.com/170/413562322_8a3fc74ce2.jpg"

    resp = requests.get(image_url)
    #print(resp.status_code)
    local_file=""
    if resp.status_code==200:
        local_file = open(image_url[image_url.rfind("/")+1:], 'wb')
        #file_loc="c:/Swadesh/MMAI/Research_paper/" + local_file.name
        file_loc = tgt_dir + "\\" + local_file.name
        file_name=local_file.name
        #print(file_loc + "--")
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        file1.write(file_loc + "--")
        resp.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        #shutil.copyfileobj(resp.raw, local_file)
        with open(file_loc, 'wb') as f:
            f.write(resp.content)
    # Remove the image url response object.
        #add new column
        image_file.iloc[i, 9]='YES'
        image_file.iloc[i, 10]=local_file.name
        file1.write("in the if block-")
        file1.write(str(resp.status_code) + "\n")
        #image_file['image_exists']='YES'
        #print("in the if block")
        #print(resp.status_code)
        local_file.close()
        #print(file_name)
        image_resize(file_name,tgt_dir,rsize_dir, 500)
    else:
       # print("in the else block")
       # print(resp.status_code)
       file1.write("in the if block")
       file1.write(str(resp.status_code) + "\n")
       image_file.iloc[i, 9]='NO'
       #image_file.iloc[i, 10]=local_file.name
#removing the temporary files
print(default_dir)
filelist=glob.glob(default_dir + "\\*.jpg")
for file in filelist:
    os.remove(file)
#save the updated metadata file.
image_file.to_csv(tgt_dir + "\\" + 'out_image-Sentiment-polarity.csv')
file1.write(str(datetime.datetime.now()) + "\n")
print(datetime.datetime.now())