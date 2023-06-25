from PIL import Image
from random import randint
import binascii

base_image = Image.open("./symatrix.png")

base_x, base_y = base_image.size

x_len = int(base_x / 2)
y_len = int(base_y)

left_image = Image.new("RGB", (x_len, y_len))
right_image = Image.new("RGB", (x_len, y_len))

base_matrix = base_image.load()
left_matrix = left_image.load()
right_matrix = right_image.load()

for i_y in range(0, base_y):
    for i_x in range(0, base_x):
        pixel = base_matrix[i_x, i_y]

        if i_x < x_len:
            left_matrix[i_x, i_y] = pixel
        else:
            local_x = int(x_len - i_x - 1)
            right_matrix[local_x, i_y] = pixel

left_image.save("./pic1.png")
right_image.save("./pic2.png")

print("Saved pictures. Let's calculate diff")

def binstr_to_hexstr(binstr):
    return "{0:0>4X}".format(int(binstr, 2))

i = 1
binstr = ""
for i_y in range(0, y_len - 1):
    for i_x in range(0, x_len - 1):
        left_data_pixel = left_matrix[i_x, i_y]
        right_data_pixel = right_matrix[i_x, i_y]
        if left_data_pixel != right_data_pixel and right_data_pixel[1] == 1:
            diff_data_pixel = int(right_data_pixel[2] - left_data_pixel[2])
            print(str(diff_data_pixel), end="")
            binstr = binstr + str(diff_data_pixel)
            i = i + 1

left_image.close()
right_image.close()

def unhex(value):
    return binascii.unhexlify(value)

print()
print("HexPossible value: " + bytes.fromhex(binstr_to_hexstr(binstr)).decode('utf-8'))
print("Flag! " + (bytes.fromhex(binstr).decode("utf-8")))
