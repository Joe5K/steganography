from PIL import Image
import re


class Steganographer:
    MAX_HEADER_LENGTH = 1024

    def __init__(self, image_filename: str):
        self.image = Image.open(image_filename)

    def encrypt_text(self, text: str) -> Image:
        text = f"{0}{len(text)};{text}"
        binary_data = ''.join(format(ord(i), '08b') for i in text)

        self.write_binary(binary_data)

    def encrypt_file(self, filename: str) -> Image:
        with open(filename, "rb") as reader:
            data = reader.read()
        data = list(data)
        binary_data = ""
        for i in data:
            one_byte = bin(i)[2:]
            while len(one_byte) != 8:
                one_byte = '0' + one_byte
            binary_data += one_byte

        header = f"{1}{filename};{len(binary_data)};"
        binary_header = ''.join(format(ord(i), '08b') for i in header)

        binary_data = binary_header + binary_data

        self.write_binary(binary_data)

    def write_binary(self, binary_data):
        width, height = self.image.size
        total_space = width * height * len("rgb") - self.MAX_HEADER_LENGTH
        if len(binary_data) > total_space - 1:
            raise Exception("Not enough space on image")
        binary_data = iter(binary_data)
        finished = False

        for y in range(height):
            for x in range(width):
                one_pixel = self.image.getpixel((x, y))
                new_color = []
                for color_index, color in enumerate(one_pixel):
                    next_data = next(binary_data, None)
                    if next_data is not None:
                        new_color.append(color & 254 | int(next_data))
                    else:
                        new_color.append(color)
                        finished = True

                self.image.putpixel((x, y), tuple(new_color))

                if finished:
                    break
            if finished:
                break

    def decrypt(self) -> str:
        def get_bits():
            width, height = self.image.size
            for y in range(height):
                for x in range(width):
                    for color in self.image.getpixel((x, y)):
                        yield color & 1
        bits_generator = get_bits()

        def get_chars():
            bits = ""
            for bit in bits_generator:
                bits += str(bit)
                if len(bits) % 8 == 0:
                    yield chr(int(bits, 2))
                    bits = ""
        chars_generator = get_chars()

        def get_strings():
            string = ""
            for letter in chars_generator:
                if letter != ";":
                    string += letter
                else:
                    yield string
                    string = ""
        string_generator = get_strings()

        type = next(chars_generator)

        if type == "0":
            length = int(next(string_generator))
            text = ""
            for letter in chars_generator:
                text += letter
                if len(text) == length:
                    return f"Decryptovany text: {text}"

        elif type == "1":
            filename = next(string_generator)
            length = int(next(string_generator))
            bits = ""
            for bit in bits_generator:
                bits += str(bit)
                if len(bits) == length:
                    break

            bytes = re.findall(r'\d{1,8}', bits)
            bytes = [int(i, 2) for i in bytes]
            with open(filename, "wb") as writer:
                writer.write(bytearray(bytes))
            return f"Decryptovany subor {filename} bol ulozeny."

    def detect_steganography(self) -> bool:  # bonus konvoluce/ina metoda
        pass

    @staticmethod
    def read_file_binary(filename: str) -> list[bytes]:
        pass


print("Na všetky vstupy a vstupné súbory používajte šifrovanie ASCII (bez diakritiky) bez znaku `;`")
func = input("Pre zašifrovanie textu vložte 1, súboru 2, pre dešifrovanie 3, detekciu 4\n")

input_image_filename = input("Vložte názov súboru vstupného obrázku\n")
steganographer = Steganographer(input_image_filename)

if func == "1":
    input_text = input("Vložte text, ktorý chcete zašifrovať\n")
    output_file = input("Vložte názov súboru pre výstupný obrázok\n")

    steganographer.encrypt_text(input_text)
    steganographer.image.save(output_file)

elif func == "2":
    filename = input("Vložte názov súboru, ktorý chcete zašifrovať\n")
    output_file = input("Vložte názov súboru pre výstupný obrázok\n")

    steganographer.encrypt_file(filename)
    steganographer.image.save(output_file)
elif func == "3":
    print(steganographer.decrypt())
elif func == "4":
    pass
else:
    print("Neplatný vstup:")
