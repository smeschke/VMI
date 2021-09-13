import cv2
import numpy as np
import os

drawers = []
font, scale, color, thick = cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2

# Mouse callback function
global click_list
positions, click_list = [], []
def callback(event, x, y, flags, param):
    if event == 1:
        click_list.append((x,y))

cv2.namedWindow('img')
cv2.setMouseCallback('img', callback)

location_data = []

sourcePath = '/home/stephen/Desktop/drawers_full/'
paths = os.listdir(sourcePath)
paths.sort()

for drawerPath in paths:
    img = cv2.imread(sourcePath + drawerPath)
    img = cv2.resize(img, (600,600))
    #print(drawerPath)
    #print(img.shape)
    textString = ""
    location_data.append([])
    drawerNumber = paths.index(drawerPath)
    while True:
        

        # Show frame
        if len(click_list) == 2:
            #print(textString)           
            a,b = click_list
            cv2.rectangle(img, a, b, (255,0,0), 12)
            org = (a[0]+b[0])/2, (a[1] + b[1])/2
            org = tuple(np.array(org, int))
            cv2.putText(img, textString, org, font, scale, color, thick, cv2.LINE_AA)
            location_data
            location_data[drawerNumber].append((textString, click_list))
            textString = ""
            click_list = []

        cv2.rectangle(img, (100,550), (500,600), 0, -1)
        cv2.putText(img, textString, (100,580), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow('img', img)
        k = cv2.waitKey(1)
        # Wait, and allow the user to quit with the 'esc' key
        if k > 1:
            textString += chr(k)
        
        if k == 27: break


for i in range(len(location_data)):
	print("drawer #" + str(i+1))
	for item in location_data[i]:
		print(item)
	print()

cv2.destroyAllWindows()
