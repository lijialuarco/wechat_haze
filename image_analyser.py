import joint_image
import json
import pygame
import os
import re
from PIL import Image

UNIT_SIZE = 1000
size = (50, 50)


def get_images(image_names):
    f = open('./data/res.json', 'r')
    data_set = json.loads(f.read())
    pygame.font.init()

    res = dict()
    for image_name in image_names:
        for key in data_set.keys():
            if key.find(image_name) != -1:
                res.update({key: data_set[key]})
    print(res)

    target = Image.new('RGB', (140, 250), (255, 255, 255))  # result is 2*5
    x = 0
    y = 0

    for text in res:
        short_text = re.sub('时', '-', re.sub('日', '-', text[8:13]))
        font = pygame.font.SysFont('simsun', 18)
        rtext = font.render(short_text, True, (0, 0, 0), (res[text]['r'], res[text]['g'], res[text]['b']))

        pygame.image.save(rtext, "t.png")

        line = Image.open("t.png")
        target.paste(line, (x, y))
        x += 35
        if x == 140:
            y += 15
            x = 0
    base = Image.open("base.jpg")
    target.paste(base, (10, 220))
    target.show()
    target.save("s.png")
    return 's.png'
