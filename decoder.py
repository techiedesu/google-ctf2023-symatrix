from PIL import Image
from random import randint
import binascii

def hexstr_to_binstr(hexstr):
    n = int(hexstr, 16)
    bstr = ''
    while n > 0:
        bstr = str(n % 2) + bstr
        n = n >> 1
    if len(bstr) % 8 != 0:
        bstr = '0' + bstr

    print("input hex is '" + hexstr + "' -> " + bstr)
    return bstr

def binstr_to_hexstr(binstr):
    return "{0:0>4X}".format(int(binstr, 2))

def pixel_bit(b):
    return tuple((0, 1, b))

def embed(t1, t2):
    return tuple((t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]))

# пиксель имеет максимальное значение
def full_pixel(pixel):
    return pixel[1] == 255 or pixel[2] == 255

print("Embedding file...")

bin_data = open("./flag.txt", 'rb').read()
data_to_hide = binascii.hexlify(bin_data).decode('utf-8')

base_image = Image.open("./original.png")

x_len, y_len = base_image.size
nx_len = x_len * 2

new_image = Image.new("RGB", (nx_len, y_len))

base_matrix = base_image.load()
new_matrix = new_image.load()

binary_string = hexstr_to_binstr(data_to_hide)
remaining_bits = len(binary_string)

nx_len = nx_len - 1
next_position = 0

for i in range(0, y_len):
    for j in range(0, x_len):

        # пробегаемся по всем пикселям в картинке и назначаем их в новой матрице
        # для последующей модификации
        pixel = new_matrix[j, i] = base_matrix[j, i]

        # remaining_bits -- количество оставшихся байтов для записи
        # следовательно, если если есть данные для записи и
        #
        # next_position -- позиция где записывается байт пейлоада (отступ), который
        # явно равен или больше опрделеённого числа рандомом
        if remaining_bits > 0 and next_position <= 0 and not full_pixel(pixel):
            # здесь развёрнуто, но в декодере уже отзеркалил пикчу
            new_matrix[nx_len - j, i] = embed(pixel_bit(int(binary_string[0])), pixel) 
            # смешиваем два пикселя через embed
            
            # получается, минимальный отступ 1 и максимальный 17 или больше
            # для начала, возьмём максимальную разницу между пикселями 19
            next_position = randint(1, 17)
            print("next_position is " + str(next_position))
            binary_string = binary_string[1:] # забираем первый элемент от коллекции (1, 2, 3) -> 1 :: (2, 3)
            remaining_bits -= 1
        else:
            # записываем пиксель с оригинального изображения
            # но просто разворачиваем (зеркальная картинка)
            new_matrix[nx_len - j, i] = pixel
            next_position -= 1

new_image.save("./symatrix-old.png")
new_image.close()
base_image.close()

print("Work done!")
exit(1)
