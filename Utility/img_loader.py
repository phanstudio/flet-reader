from PIL import Image
import stagger
import io, os

def loader(path:str, nam):
    root_path = os.getenv("FLET_ASSETS_PATH")
    folders = os.path.join(root_path,'covers')
    img = 'defualt'
    try:
        mp3 = stagger.read_tag(path)
        by_data = mp3[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)
        imageFile = Image.open(im)
        imageFile.save(os.path.join(folders,f'{nam}.png'))
        img = nam
    except:
        defualt_img_path = os.path.join(folders,'defualt.png')
        if not os.path.exists(defualt_img_path):
            imageFile = Image.open(os.path.join(root_path,'9.png'))
            imageFile.save(defualt_img_path)
    return img+'.png'
