from PIL import Image
from io import BytesIO

def sr_color(image_color):

    if "*png" in image_color:
        with BytesIO() as f:
            image_color.save(f, format='JPEG')
            f.seek(0)
            image = Image.open(f)
    else:
        image = Image.open(image_color)    

    w, h = image.size

    pixel = []

    for x in range(w):
        for y in range(h):
            r, g, b = image.getpixel((x, y))
            pixel.append([r, g, b])

    avr = [sum(x) // len(x) for x in zip(*pixel)]

    r, g, b = avr[0], avr[1], avr[2]

    def rgb(r, g, b):
        round = lambda x: min(255, max(x, 0))
        
    return ("{:02X}" * 3).format(round(r), round(g), round(b))




print(sr_color('1.jpeg'))
print(sr_color('default.png'))
print(sr_color('3.jpg'))
print(sr_color('4.jpg'))
