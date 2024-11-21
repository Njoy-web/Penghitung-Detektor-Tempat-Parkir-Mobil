import cv2
import numpy as np
import pickle

rectW, rectH = 107, 48

cap = cv2.VideoCapture('ParkirMobil.mp4')

with open('posParkirMobil', 'rb') as f:
    posList = pickle.load(f)


def check(imgPro):
    spaceCount = 0
    for pos in posList:
        x, y = pos
        crop = imgPro[y:y + rectH, x:x + rectW]
        count = cv2.countNonZero(crop)
        if count < 900:
            spaceCount += 1
            color = (0, 255, 0)
            thick = 5
        else:
            color = (0, 0, 255)
            thick = 2
            
        cv2.rectangle(img, pos, (pos[0]+rectW, pos[1]+rectH), color, thick)
    cv2.rectangle(img, (45, 30), (250, 75), (180, 0, 180), -1)
    cv2.putText(img, f'Kosong: {spaceCount}/{len(posList)}', (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
while True:
    ret, img = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(thre, 5)
    kernal = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(blur, kernal, iterations=1)

    check(dilate)
    cv2.imshow('Image', img)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()