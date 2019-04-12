from PIL import Image


path_image = 'base.jpeg'
out_path_image = 'out.jpeg'
basewidth = 1000
img = Image.open(path_image)
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save(out_path_image) 