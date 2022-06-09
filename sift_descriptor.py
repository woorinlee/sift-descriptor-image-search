import os
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from collections import Counter
from matplotlib import pyplot as plt

# 입력된 배열에서 첫 번째, 두 번째, 세 번째, 네 번째로 큰 값을 찾고 반환한다.
def get_largest(arr):
    first_largest = None
    second_largest = None
    third_largest = None
    fourth_largest = None

    for i in arr:
        if first_largest is None:
            first_largest = i
        else:
            if i > first_largest:
                second_largest = first_largest
                first_largest = i
            else:
                if second_largest is None:
                    second_largest = i
                else:
                    if i > second_largest:
                        third_largest = second_largest
                        second_largest = i
                    else:
                        if third_largest is None:
                            third_largest = i
                        else:
                            if i > third_largest:
                                fourth_largest = third_largest
                                third_largest = i
                            else:
                                if fourth_largest is None:
                                    fourth_largest = i
                                else:
                                    if i > fourth_largest:
                                        fourth_largest = i

    return first_largest, second_largest, third_largest, fourth_largest

# 검색된 영상을 matplotplib를 통해 다중 출력한다.
def open_multiple_img(path0, img_list):
    src = []
    rows = 1
    cols = 5

    # 입력된 숫자가 한 자리이면 앞에 "00"을 붙이고, 두 자리이면 앞에 "0"을 붙인다. (001, 011, 021, ...)
    for i in range(0, len(img_list)):
        if len(str(img_list[i])) == 1:
            img_list[i] = "00" + str(img_list[i])
        elif len(str(img_list[i])) == 2:
            img_list[i] = "0" + str(img_list[i])
        else:
            img_list[i] = str(img_list[i])

        # cv2를 통해 영상 리스트에서 하나씩 이미지를 읽어와서 src 배열에 저장한다.
        path1 = "./source/S" + img_list[i] + ".jpg"
        temp_1 = cv2.imread(path1)
        temp_2 = cv2.cvtColor(temp_1, cv2.COLOR_BGR2RGB)
        src.append(temp_2)

    # matplotlib을 통해 창을 설정한다.
    fig = plt.figure(figsize=(12, 6))

    # 비교를 위해 선택한 영상을 출력한다.
    src0 = cv2.cvtColor(cv2.imread(path0), cv2.COLOR_BGR2RGB)
    ax0 = fig.add_subplot(rows, cols, 1)
    ax0.imshow(src0)
    ax0.set_title('Original')
    ax0.axis("off")

    # src 배열의 값이 None이 아니면 해당 영상을 출력한다.
    try:
        if src[0] is not None:
            ax1 = fig.add_subplot(rows, cols, 2)
            ax1.imshow(src[0])
            ax1.set_title('IMG 1')
            ax1.axis("off")

        if src[1] is not None:
            ax2 = fig.add_subplot(rows, cols, 3)
            ax2.imshow(src[1])
            ax2.set_title('IMG 2')
            ax2.axis("off")

        if src[2] is not None:
            ax3 = fig.add_subplot(rows, cols, 4)
            ax3.imshow(src[2])
            ax3.set_title('IMG 3')
            ax3.axis("off")

        if src[3] is not None:
            ax4 = fig.add_subplot(rows, cols, 5)
            ax4.imshow(src[3])
            ax4.set_title('IMG 4')
            ax4.axis("off")

    except IndexError:
        # src[n]이 존재하지 않을 경우 IndexError를 발생시키기 때문에 예외처리를 한다.
        plt.show()

    # 창을 보여준다.
    plt.show()

# 입력된 리스트에서 입력된 값의 위치를 찾고 sim_img 배열에 넣는다.
def get_list_count(temp_list, value):
    result_list = list(filter(lambda f: temp_list[f] == value, range(len(temp_list))))
    for i in result_list:
        sim_img.append(i)

def sift_descriptor(path1):
    src_path = "./source"
    src_path_list = os.listdir(src_path)
    src_count = len(src_path_list)
    sim_list = []
    global sim_img
    sim_img = []

    # /source 폴더에서 영상을 하나씩 읽어와서 SIFT 디스크립터를 이용해 매칭점을 찾는다.
    for i in range(1, src_count+1):
        path2 = src_path + "/" + src_path_list[i-1]
        sim_list.append(sift_descriptor_compare(path1, path2))
        print(path2 + ": " + str(sim_list[i-1]))

    # sim_list에서 저장된 값의 빈도를 확인한다.
    count_value = Counter(sim_list)
    print(count_value)

    # get_largest 함수를 통해 첫 번째로 큰 값, 두 번째로 큰 값, 세 번째로 큰 값, 네 번째로 큰 값을 찾는다.
    first_largest, second_largest, third_largest, fourth_largest = get_largest(sim_list)
    print("first_largest : ", first_largest)
    print("second_largest : ", second_largest)
    print("third_largest : ", third_largest)
    print("fourth_largest : ", fourth_largest)

    # get_list_count 함수를 통해 첫 번째로 큰 값, 두 번째로 큰 값, 세 번째로 큰 값, 네 번째로 큰 값의 위치를 찾아서 sim_img에 저장한다.
    get_list_count(sim_list, first_largest)
    get_list_count(sim_list, second_largest)
    get_list_count(sim_list, third_largest)
    get_list_count(sim_list, fourth_largest)

    # 저장된 위치의 영상을 open_multiple_img 함수를 통해 다중 출력한다.
    open_multiple_img(path1, sim_img)

def sift_descriptor_compare(path1, path2):
    src1 = cv2.imread(path1)
    src2 = cv2.imread(path2)

    img1= cv2.cvtColor(src1,cv2.COLOR_BGR2GRAY)
    img2= cv2.cvtColor(src2,cv2.COLOR_BGR2GRAY)

    siftF = cv2.SIFT_create(edgeThreshold = 80)
    kp1, des1 = siftF.detectAndCompute(img1, None)
    kp2, des2 = siftF.detectAndCompute(img2, None)

    # L2-Norm을 통해 매칭점을 찾는다.
    bf = cv2.BFMatcher_create(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1,des2)

    matches = sorted(matches, key = lambda m: m.distance)
    minDist = matches[0].distance
    good_matches = list(filter(lambda m: m.distance<5*minDist, matches))
    if len(good_matches) < 5:
        print('sorry, too small good matches')
        exit()

    src1_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches])
    src2_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches])

    H, mask = cv2.findHomography(src1_pts, src2_pts, cv2.RANSAC, 3.0)
    mask_matches = mask.ravel().tolist()

    cv2.waitKey()
    cv2.destroyAllWindows()

    return mask_matches.count(1)

# filedialog 함수를 통해 영상을 선택한다.
def select_img():
    global path
    path = None
    path = filedialog.askopenfilename(filetypes=[('Image File', '.jpg'), ('Image File', '.png'), ('Image File', '.gif'), ('Image File', '.bmp')])
    if path is not None and path != "":
        path = path.replace('\\', '/')
        name = get_filename(path)
        img_lbl.config(text="\"" + name + "\" is selected.")
    elif path == "":
        img_lbl.config(text="Please select an image.")

# 이미지가 선택되었으면 sift_descriptor 함수를 통해 매칭점을 찾아서 출력한다.
def compare_img():
    while True:
        try:
            if path is not None and path != "":
                sift_descriptor(path)
            elif path == "":
                img_lbl.config(text="Please select an image.")
            break
        except NameError:
            img_lbl.config(text="Please select an image.")
            break

# 경로에서 파일명을 추출한다.
def get_filename(img_path):
    name_list = img_path.split('/')
    name = name_list[len(name_list)-1]
    return name

# TKinter를 통해 창을 구성한다.
root = Tk()

root.title("SIFT Descriptor")
root.geometry("250x170")
root.resizable(False, False)

temp_1_lbl = Label(root, text="")
temp_1_lbl.pack()

main_lbl = Label(root, text="SIFT Descriptor")
main_lbl.pack()

# 영상을 선택하는 버튼을 구성한다.
select_btn = Button(root, text="Select Image", overrelief = "solid", command=select_img)
select_btn.pack()

temp_2_lbl = Label(root, text="")
temp_2_lbl.pack()

img_lbl = Label(root, text="Click Select Image Button")
img_lbl.pack()

# 영상을 검색하는 버튼을 구성한다.
compare_btn = Button(root, text="Compare Image", overrelief = "solid", command=compare_img)
compare_btn.pack()

root.mainloop()