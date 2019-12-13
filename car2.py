import cv2
import json
import io

from skimage import io
import imutils

import os
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
print("Enter position of image which you want to see ")
b=int(input())

a=[]
with open('plate.json') as f:
    for line in f:
        a.append(json.loads(line))
image = io.imread(a[b]['content'])
image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gray= cv2.bilateralFilter(gray,11,17,17)


gray= cv2.Canny(gray,170,200)


cnts, new =cv2.findContours(gray.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


img1=image.copy()
cv2.drawContours(img1,cnts,-1,(0,255,0),3)


cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:30]
PlateCnt = None 


img2 = image.copy()
cv2.drawContours(img2,cnts,-1,(0,255,0),3)

count=0
idx=7
for c in cnts:
    peri= cv2.arcLength (c, True)
    approx = cv2.approxPolyDP(c, 0.02* peri, True)

    if len(approx)== 4: 
        PlateCnt = approx 

        x,y,w,h = cv2.boundingRect (c) 
        new_img= image[y:y+ h, x:x+w] 
        cv2.imwrite('Car4/' + str(idx) +'.png', new_img) 
        idx+=1

        break

cv2.drawContours(image, [PlateCnt], -1 ,(0,255,0),3)


Cropped = 'Car4/7.png'



text=''
text = pytesseract.image_to_string(Cropped,config = '--psm 6')
print("Number is :",text)

