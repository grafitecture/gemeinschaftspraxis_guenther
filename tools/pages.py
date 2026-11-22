import sys
from PIL import Image
src, prefix, h = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src); W, H = im.size
n = 0
for y in range(0, H, h):
    im.crop((0, y, W, min(H, y + h))).save(f"{prefix}{n}.png"); n += 1
print(W, H, n)
