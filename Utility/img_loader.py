# from PIL import Image
# import stagger
# import io, os
# from .constants import ROOTPATH

# def loader(path:str, nam):
#     folders = os.path.join(ROOTPATH,'covers')
#     img = 'defualt'
#     try:
#         mp3 = stagger.read_tag(path)
#         by_data = mp3[stagger.id3.APIC][0].data
#         im = io.BytesIO(by_data)
#         imageFile = Image.open(im)
#         imageFile.save(os.path.join(folders,f'{nam}.png'))
#         img = nam
#     except:
#         defualt_img_path = os.path.join(folders,'defualt.jpg')
#         if not os.path.exists(defualt_img_path):
#             imageFile = Image.open(os.path.join(ROOTPATH,'9.png'))
#             imageFile.save(defualt_img_path)
#     return img+'.png'


from PIL import Image
import mutagen
import io
import os
from .constants import ROOTPATH

def loader(path: str, nam: str) -> str:
    folders = os.path.join(ROOTPATH, 'covers')
    os.makedirs(folders, exist_ok=True)
    image_path = f'{nam}.png'
    
    img = 'defualt'
    try:
        # Use mutagen to read ID3 tags
        audio = mutagen.File(path)
        
        # Extract album art
        if audio and 'APIC:' in audio:
            cover = audio['APIC:']
            by_data = cover.data
            im = io.BytesIO(by_data)
            imageFile = Image.open(im)
            imageFile.save(os.path.join(folders, image_path))
            img = nam
            
    except Exception as e:
        print(f"Error extracting album art: {e}")
    
    # Handle default image
    defualt_img_path = os.path.join(folders, 'defualt.jpg')
    if img == 'defualt' and not os.path.exists(defualt_img_path):
        imageFile = Image.open(os.path.join(ROOTPATH, '9.png'))
        imageFile.save(defualt_img_path)
        image_path = 'defualt.jpg'
    
    return image_path