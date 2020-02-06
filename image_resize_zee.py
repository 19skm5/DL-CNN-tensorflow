from PIL import Image, ImageOps
#desired_size = 500
def image_resize(file_name,src_loc, rsz_dir, desired_size):
    # im_pth = "C:/Swadesh/MMAI/MMAI 894/CNN/rsize/1002435248_97773f5484.jpg"


    im_pth= str(src_loc) + "\\" + file_name
    #print(im_pth)
    im = Image.open(im_pth)
    old_size = im.size  # old_size[0] is in (width, height) format
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    # use thumbnail() or resize() method to resize the input image
    # thumbnail is a in-place operation
    # im.thumbnail(new_size, Image.ANTIALIAS)
    im = im.resize(new_size, Image.NEAREST)
    # create a new image and paste the resized on it
    new_im = Image.new("RGB", (desired_size, desired_size))
    new_im.paste(im, ((desired_size-new_size[0])//2,
                      (desired_size-new_size[1])//2))
    #new_im.show()
    im_pth= str(rsz_dir) + "\\" + file_name
    #print(im_pth)
    new_im.save(im_pth , "JPEG")