import os
from re import search
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import Destination
from pdf2image import convert_from_path
import glob
from PIL import Image
import shutil
import z

if __name__ == '__main__':
    root = os.getcwd()
    dirsSubdirs = [root,]

    path = os.path.dirname(__file__)

    for path, subdirs, files in os.walk(path):
        for dir in subdirs:
            dirsSubdirs.append((path+"\\" +dir))

    
    for i in range(len(dirsSubdirs)):
        os.chdir(dirsSubdirs[i])
    
        files = os.listdir(dirsSubdirs[i])
    
        for filename in files:
            if filename.endswith(('.pdf')):
                try:
                    z.removeWatermark(os.path.splitext(filename)[0] + ".pdf", "para2_" + os.path.splitext(filename)[0] + ".pdf")
                except Exception as e:
                    print("Não foi possível abrir {}".format(os.getcwd()+"\\"+filename))
                    print(e)

    for x in range(len(dirsSubdirs)):
        os.chdir(dirsSubdirs[x])
        files = os.listdir(dirsSubdirs[x])
        for filename in files:
            if "para2_" in filename:
                src = os.getcwd() + "\\"+ filename
                dst = root +"\\pdfs_modificados"+ os.getcwd().split(root)[1]
                # dst += "\\Notas da Aula (PDFs)"
                dst += "\\" + filename.split("para2_")[1]
                
                newdir = "pdfs_modificados\\"+ os.getcwd().split(root)[1]
                # newdir += "\\Notas da Aula (PDFs)"
                print("Criando {}\n".format(newdir))

                ult_caminho = os.getcwd()

                os.chdir(root)
                if not os.path.exists(newdir):
                    os.system("mkdir \"{}\"".format(newdir))
                
                print("Movendo arquivo de {} para {}\n".format(src,dst))

                os.replace(src, dst)
                os.chdir(ult_caminho)
                # os.system("mv \"{}\" \"{}\"".format(src,dst))
                    