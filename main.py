from PIL import Image


def encrypt_text(image: Image, text: str) -> Image:
    pixel_data = image.load()
    width, height = image.size
    number_of_bits = width * height * 3 - 128
    binary_text = ''.join(format(ord(i), '08b') for i in text)

    type = "0"

    iterator = iter(binary_text)

    for y in range(height):
        for x in range(width):
            one_pixel = pixel_data[x, y]
            new_color = []
            for color_index, color in enumerate(one_pixel):
                next_bit = next(iterator)
                color_binary = bin(color)
                new_color_binary = color_binary[:-1] + next_bit
                new_color_one = int(new_color_binary, 2)
                new_color.append(new_color_one)
            pixel_data[x, y] = tuple(new_color)


def encrypt_file(image: Image, file: list[bytes]) -> Image:  # bonus roztiahnut vstupny image ak sa subor nezmesti
    pass


def decrypt_text(image: Image) -> str:
    pass


def decrypt_file(image: Image) -> list[bytes]:
    pass


def read_file_binary(filename: str) -> list[bytes]:
    pass


def detect_steganografy(image: Image) -> bool:  # bonus konvoluce/ina metoda
    pass

print("Na všetky vstupy a vstupné súbory používajte šifrovanie ASCII (bez diakritiky)")
func = "1"#input("Pre zašifrovanie textu vložte 1, súboru 2, pre dešifrovanie 3, detekciu 4")

input_image_filename = "download.jpeg" #input("Vložte názov súboru vstupného obrázku")
input_image = Image.open(input_image_filename)

if func == "1":
    input_text = "h" #input("Vložte text, ktorý chcete zašifrovať")
    output_file = "output.jpeg" #input("Vložte názov súboru pre výstupný obrázok")
    output_image = encrypt_text(input_image, input_text)

elif func == "2":
    pass
elif func == "3":
    pass
elif func == "4":
    pass
else:
    print("Neplatný vstup:")
im = Image.open('download.jpeg') # Can be many different formats.
pixel_data = im.load()
print(im.size) # kontrolovat  # Get the width and hight of the image for iterating over
print(pixel_data[0, 0])
pixel_data[0,0] = (255, 255, 255)
print(pixel_data[0, 0])
im.save("new.jpeg")

input("vlozte filename")


with open("download.jpeg", "rb") as reader:
    content = reader.read()

