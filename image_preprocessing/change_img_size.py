import os
import cv2

path = "C:/Users/lenya/Documents/python_project/quest_test/2"
name = os.listdir(path)

for i in range(1, len(name)+1):
    img = cv2.imread(path + "/" + str(i) + ".jpg")
    img = cv2.resize(img, dsize=(600, 800))
    cv2.imwrite(path + "/" + str(i) + ".jpg", img) 
    print(str(i) + ".jpg")
    #cv2.waitKey()
    #cv2.destroyAllWindows()