from PIL import Image
import io

def resize_image(file, custom_width=None, custom_height=None):
    img = Image.open(file.stream)
    
    # Change the size of image depending upon the users wish
    if custom_width and custom_height:
        new_size = (custom_width, custom_height)
    else:
        # Dosnt change the size If the Height and width is not given 
        new_size = img.size

    # Resize the image with the LANCZOS filter, which is one of the best for preserving quality
    img = img.resize(new_size, Image.LANCZOS)
    
    # Save the resized image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=100)  # Use quality=100 to ensure the highest quality
    
    img_io.seek(0)
    return img_io
def compress_image(file, target_size_kb):
    img = Image.open(file.stream)
    img_io = io.BytesIO()

    # Function to calculate image size in KB
    def calculate_size(img, quality):
        img_io.seek(0)
        img_io.truncate(0)
        img.save(img_io, format='JPEG', quality=quality)
        return img_io.tell() / 1024

    # Iterative resizing and quality adjustment
    quality = 95
    step_quality = 5
    step_resize = 0.9

    while True:
        size_kb = calculate_size(img, quality)
        if size_kb <= target_size_kb:
            break
        if quality - step_quality < 5 and (img.width * step_resize < 100 or img.height * step_resize < 100):
            break  # Prevent from going too low in quality and size
        if size_kb > target_size_kb:
            if quality > step_quality:
                quality -= step_quality
            else:
                img = img.resize((int(img.width * step_resize), int(img.height * step_resize)), Image.LANCZOS)
                quality = 95  # Reset quality after resizing
        else:
            break

    # Final compression with determined quality
    img_io.seek(0)
    img_io.truncate(0)
    img.save(img_io, format='JPEG', quality=quality)
    
    if img_io.tell() / 1024 > target_size_kb:
        return None  # Couldn't compress to the desired size

    img_io.seek(0)
    return img_io
