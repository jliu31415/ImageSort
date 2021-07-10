import os
import shutil
from PIL import Image

root = "C:\\Users\\jliu3\\Downloads\\2020\\"
output = root + "output\\"
error = root + "error\\"
# initialize output directory
if os.path.exists(output):
    shutil.rmtree(output)   
os.makedirs(output)
# initialize error directory
if os.path.exists(error):
    shutil.rmtree(error)   
os.makedirs(error)

# create output file path name
def filePath(date, counter, extension):
    return output + date + "_" + str(counter) + extension

# 306: DateTime
# 36867: DateTimeOriginal 
# from PIL.ExifTags import TAGS
# for tag in TAGS:
#     if ("Date" in TAGS[tag]):
#         print(tag, TAGS[tag])

for file in os.listdir(root):
    # skip folders
    if (not os.path.isfile(root + file)):
        continue
    
    # open image file if possible (may be .mov, etc)
    try:
        image = Image.open(root + file)
    except Exception:
        print("Can't open", file)
        shutil.copy(root + file, error + file)
        continue
    
    try:
        # retrieve the date, concatenate as YYYYMMDD
        if (306 in image._getexif().keys()):
            date = image._getexif().get(306)
        else:
            date = image._getexif().get(36867)
        date = date.split(" ")[0].replace(":", "")
    except Exception:
        # unable to retrieve data entry from exif
        print("Exif fail", file)
        shutil.copy(root + file, error + file)
        continue

    # retrieve file extension
    extension = os.path.splitext(file)[1]

    # add a unique counter XXXX to prevent name duplication
    counter = 0
    while os.path.exists(filePath(date, counter, extension)):
        counter += 1

    # copy file to output folder
    shutil.copy(root + file, filePath(date, counter, extension))
