from PIL import Image
import io

def resize_image(file, custom_width=None, custom_height=None):
    img = Image.open(file.stream)
    
    if custom_width and custom_height:
        new_size = (custom_width, custom_height)
    else:
        new_size = img.size

    img = img.resize(new_size, Image.LANCZOS)
    
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=100)  
    
    img_io.seek(0)
    return img_io
def compress_image(file, target_size_kb):
    img = Image.open(file.stream)
    img_io = io.BytesIO()

    def calculate_size(img, quality):
        img_io.seek(0)
        img_io.truncate(0)
        img.save(img_io, format='JPEG', quality=quality)
        return img_io.tell() / 1024

    quality = 95
    step_quality = 5
    step_resize = 0.9

    while True:
        size_kb = calculate_size(img, quality)
        if size_kb <= target_size_kb:
            break
        if quality - step_quality < 5 and (img.width * step_resize < 100 or img.height * step_resize < 100):
            break  #This line Prevent from going too low quality and size
        if size_kb > target_size_kb:
            if quality > step_quality:
                quality -= step_quality
            else:
                img = img.resize((int(img.width * step_resize), int(img.height * step_resize)), Image.LANCZOS)
                quality = 95  
        else:
            break

    # Final compression with determined quality
    img_io.seek(0)
    img_io.truncate(0)
    img.save(img_io, format='JPEG', quality=quality)
    
    if img_io.tell() / 1024 > target_size_kb:
        return None  

    img_io.seek(0)
    return img_io
