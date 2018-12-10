import os
from PIL import Image

UNIT_SIZE = 230


def pinjie(images):
    target = Image.new('RGB', (UNIT_SIZE * 5, UNIT_SIZE * 2))  # result is 2*5
    leftone = 0
    lefttwo = 0
    rightone = UNIT_SIZE
    righttwo = UNIT_SIZE
    i = 0
    for key in images.keys():
        print(key)
        print(images[key])
        if (i % 2 == 0):
            target.paste(Image.new('RGB', (50, 20), (images[key]['r'], images[key]['g'], images[key]['b'])),
                         (leftone, 0, rightone, UNIT_SIZE))
            target.show()
            leftone += UNIT_SIZE  # 第一行左上角右移
            rightone += UNIT_SIZE  # 右下角右移
        else:
            target.paste(Image.new('RGB', (50, 20), (images[key]['r'], images[key]['g'], images[key]['b'])), (
                lefttwo, UNIT_SIZE, righttwo, UNIT_SIZE * 2))
            lefttwo += UNIT_SIZE  # 第二行左上角右移
            righttwo += UNIT_SIZE  # 右下角右移
        i = i + 1
    quality_value = 100
    target.save('./photo/res.jpg', quality=quality_value)

#
#
# path = "C:/Users/laojbdao/Desktop/FinalResult/result4/different_distribution/"
# dirlist = []  # all dir name
# for root, dirs, files in os.walk(path):
#     for dir in dirs:
#         dirlist.append(dir)
#
# num = 0
# for dir in dirlist:
#     images = []  # images in each folder
#     for root, dirs, files in os.walk(path + dir):  # traverse each folder
#         for file in files:
#             images.append(Image.open(path + dir + '/' + file))
#     pinjie(images, num)
#     num += 1
#     images = []
