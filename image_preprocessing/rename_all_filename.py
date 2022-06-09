import os

path = "./source"
name = os.listdir(path)

i = 1

for n in name:
    src = os.path.join(path, n)
    dst = "S" + str(i) + ".jpg"
    dst = os.path.join(path, dst)
    os.rename(src, dst)
    i += 1
