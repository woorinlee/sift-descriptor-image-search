import os
import random

path = "./source"
name = os.listdir(path)

count_list = []
for i in range(0, len(name)):
    if len(str(i)) == 1:
        count_list.append("00" + str(i))
    elif len(str(i)) == 2:
        count_list.append("0" + str(i))
    else:
        count_list.append(i)

i = 1
for n in name:
    random_num = random.choice(count_list)
    count_list.remove(random_num)
    src = os.path.join(path, n)
    dst = "S" + str(random_num) + ".jpg"
    dst = os.path.join(path, dst)
    os.rename(src, dst)
    i += 1