import glob
from PIL import Image
from pdf2image import convert_from_path
import shutil
import os

def removeWatermark(inputfilename, outputfilename):
    ppdf = inputfilename
    print(os.getcwd(), ppdf)

    # lista de imagens do pdf
    images = convert_from_path(inputfilename)

    # se nao existir pasta ele cria
    if not os.path.exists(ppdf.split(".pd")[0]):
        # cria pasta com nome do arquivo sem a extensão
        os.makedirs(ppdf.split(".pd")[0])

    for i in range(len(images)):
        images[i].save(ppdf.split(".pd")[0] + "/" + str(i) + '.jpg', 'JPEG')

    imgs = []
    first = None

    # itera jpgs de pastas e subpastas
    for f in glob.glob("**/*.jpg"):
        print(f)
        image = Image.open(f)
        og_size = image.size
        cortaEsq = int((4 * min(range(og_size[0]))) / 100.0)
        cortaDir = int((4 * max(range(og_size[0])) + 1) / 100.0)
        cortaCima = int((4 * min(range(og_size[1]))) / 100.0)
        cortaBaixo = int((2 * max(range(og_size[1])) + 1) / 100.0)
        # left, up, right, down
        box = (min(range(og_size[0])), min(range(og_size[1])), max(range(og_size[0])) + 1,
               max(range(og_size[1])) + 1 - cortaBaixo)
        cropped_image = image.crop(box)
        cropped_image.save(f)
        # print(f.split(".jpg")[0])

        print(f.split("\\")[-1])

        if f.split("/")[-1] == "0.jpg" or f.split("\\")[-1] == "0.jpg":
            first = Image.open(f)
        else:
            imgs.append(f)

    imgs.sort(key=lambda x: float(x.split("\\")[-1].split(".jpg")[0]))
    first.save(outputfilename, "PDF", resolution=100.0, save_all=True, append_images=[Image.open(f) for f in imgs])
    print("O arquivo {} foi salvo".format(outputfilename))

    shutil.rmtree(ppdf.split(".pd")[0])
