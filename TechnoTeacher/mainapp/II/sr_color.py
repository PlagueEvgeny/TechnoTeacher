from PIL import Image


def sr_color(image_color):
    image = Image.open(image_color)

    w, h = image.size

    pixel = []

    for x in range(w):
        for y in range(h):
            r, g, b = image.getpixel((x, y))
            pixel.append([r, g, b])

    avr = [sum(x) // len(x) for x in zip(*pixel)]

    r, g, b = avr[0], avr[1], avr[2]

    return r, g, b


print(sr_color('1.jpeg'))
print(sr_color('2.jpeg'))
print(sr_color('3.jpg'))
print(sr_color('4.jpg'))
