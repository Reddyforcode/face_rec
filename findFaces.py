import face_recognition
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

fig = plt.figure()

image = face_recognition.load_image_file("perdonas_22.jpg")
face_locations = face_recognition.face_locations(image)

print(format(len(face_locations)))  #number of faces in the pic

i = 0

for face_location in face_locations:
    top, right, bottom, left = face_location
    #print("bla {}bla{} lba{} right{}", format(top, left, bottom, right))
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.save("face-{}.png".format(i))
    i = i+1


my_list = []    #almacena las imagenes leidas por face:recognition
for j in range (0, i):
    my_list.append(face_recognition.load_image_file("face-{}.png".format(j)))

#print(my_list)
#lista de imagenes #inputs
plt.imshow(my_list.pop())


plt.show()


"""
#si la imagen uno esta dentro de la imagen
def facesInAPic(image):
    face_locations = face_recognition.face_locations(image)
    return len(face_locations)

image = face_recognition.load_image_file("face-12.jpg")
unknow_image = face_recognition.load_image_file("perdonas_22.jpg")

if(facesInAPic(image) > 0):
    faceX_encoding  = face_recognition.face_encodings(image)[0]
    unknow_encoding = face_recognition.face_encodings(unknow_image)[0]
    result = face_recognition.compare_faces([faceX_encoding], unknow_encoding)
    print(result)
    print("hay al menos un rostro en la imagen")
else:
    print("No hay rostros en la imagen")
    """
