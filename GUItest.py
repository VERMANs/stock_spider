import cv2

def getImage(code):
    img_src = "http://image.sinajs.cn/newchart/daily/n/sh"+ code +".gif"
    cap = cv2.VideoCapture(img_src)
    if (cap.isOpened()):
        ret, img = cap.read()
        cv2.imshow("image", img)
        cv2.waitKey(10)


