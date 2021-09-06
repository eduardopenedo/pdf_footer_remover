from pdf2image import convert_from_path
from PIL.Image import Image
import os

def save_images(cropped_images,output_img,filename):
    for img_index in range(len(cropped_images)):
        path = output_img + "\\" + f"{img_index}.jpg"
        cropped_images[img_index].save(path, "jpeg")


def crop_images(images):
    cropped_images = []
    for image_index in range(len(images)):
        image: Image = images[image_index]

        left = 0
        upper = 0
        right = image.width
        lower = image.height * 0.97

        cropped_images.append(image.crop(box=(left, upper, right, lower)))
    return cropped_images


def makedirs(root,pdf_path,filename,save_imgs):
    path_root_to_file_folder = os.path.dirname(pdf_path).split(os.path.dirname(__file__)+"\\")[-1]
    
    if "\\pdf" in pdf_path or "\\PDF" in pdf_path:  
        output_pdf = root + "\\" + path_root_to_file_folder
        output_img = root + "\\" + path_root_to_file_folder + "\\" + filename
    else:
        output_pdf = root + "\\" + path_root_to_file_folder + "\\" + "PDFs"
        output_img = root + "\\" + path_root_to_file_folder + "\\" + "PDFs"  + "\\" +  filename

    
    if not os.path.exists(output_pdf):
        os.makedirs(output_pdf)
    if save_imgs and not os.path.exists(output_img):
        os.makedirs(output_img)

    return {"output_pdf": output_pdf,"output_img":output_img}


def make_images(
        pdf_path,
        root,
        save_jpgs = True
    ):
    images = convert_from_path(pdf_path)

    filename = os.path.split(pdf_path)[-1].split(".")[-2]

    cropped_images = crop_images(images)

    output = makedirs(root,pdf_path,filename,save_jpgs)

    if save_jpgs:
        save_images(cropped_images,output["output_img"],filename)

    return {"images":cropped_images,"filename":filename, "output_pdf":output["output_pdf"]}


def main():
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            file_path = (f"{dirpath}\\{filename}")

            if filename.endswith(('.pdf')):
                res = make_images(file_path, os.path.dirname(__file__)+"\\Patched PDFs",True)

                if len(res["images"]) != 1:
                    first = res["images"][0]
                    print(f"{res['output_pdf']}\\{filename}")
                    first.save(f"{res['output_pdf']}\\{filename}", "PDF", resolution=100.0, save_all=True, append_images=res["images"][1:])
                else:
                    res["images"][0].save(f"{res['output_pdf']}\\{filename}", "PDF", resolution=100.0, save_all=True, append_images=res["images"][1:])

main()
