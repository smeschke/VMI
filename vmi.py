import cv2
import numpy as np
import os

# Definitions:
#     Cabinet - a chest of drawers
#     Bin - a location where one type of item is stored
#     Drawer - a horizontal plane containing one or more bins, located in a cabinet

drawerImages = []
for drawerPath in list(os.listdir('/home/stephen/Desktop/drawers')):
    img = cv2.imread('/home/stephen/Desktop/drawers/' + drawerPath)
    drawerImages.append(img)

font, scale, color, thick = cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2

location_data = [[('milk duds , 10, 20', [(59, 44), (562, 256)]), ('kit kat, 15, 30', [(49, 274), (527, 571)])], [('rolo, 10, 20', [(53, 43), (517, 276)]), ('heath,5,15', [(64, 297), (521, 533)])], [('whoppers,10,25', [(41, 66), (527, 259)]), ("reese's,15,25", [(33, 297), (504, 546)])], [('bulk almonds á(shavedá),.5lbs,1lbs.', [(146, 85), (397, 283)]), ('bulk sunflower seeds,.5,1', [(135, 313), (373, 522)])], [('cammomile tea,10 bags,20 bags', [(81, 103), (487, 275)]), ('berry tea, 10 bags, 20 bags', [(66, 298), (500, 508)])]]

# Mouse callback function
global click_list
positions, click_list = [], []
def callback(event, x, y, flags, param):
    if event == 1:
        click_list.append((x,y))   

cv2.namedWindow('img')
cv2.setMouseCallback('img', callback)

# Make a list of drawer locations
currentDrawerNumber = 0
drawerXstart, drawerXend = 20, 350
drawerTop = 25
drawerHeight = 80
drawerBufferY = 25
drawerNames = ['Candy 1', 'Candy 2', 'Candy 3', 'Nuts and Seeds', 'Tea']
numDrawers = 5
drawerLocations = []
for drawerNum in range(numDrawers):
    drawerTop += drawerHeight + drawerBufferY
    drawerLocations.append((drawerXstart, drawerXend, drawerTop, drawerTop + drawerHeight))

# Get images of drawers
paths = os.listdir('/home/stephen/Desktop/drawers')
paths.sort()
drawerImages = []
for drawerPath in paths:
    img = cv2.imread('/home/stephen/Desktop/drawers/' + drawerPath)
    drawerImages.append(img)

# Draw the file cabinet
bg = np.zeros((900,1500,3), np.uint8)
for drawer, name in zip(drawerLocations, drawerNames):
    a,b = (drawer[0], drawer[2]), (drawer[1], drawer[3])
    cv2.rectangle(bg, a, b, (0,255,255), 2)
    org = drawer[0]+50, drawer[2]+50
    cv2.putText(bg, name, org, font, scale, (0,255,255), thick, cv2.LINE_AA)

   
# Number to define the position of the current drawer in the list drawers
currentDrawer = 0
# Number to define the current part that is selected
currentPart = 0
# Number for the quantity on hand
quantityOnHand = 0
# Number for the quantity to order
quantityToOrder = 0
# Create a list for items to order
order = []
# Countdown value for displaying order to user
countdownValue = 0
# current drawer Name
currentDrawerName = drawerNames[currentDrawerNumber]

# Main loop
while True:
    # Create black image
    img = bg.copy()

    # Get the location of parts within that drawer
    parts = location_data[currentDrawerNumber]
       
    # Run this code if user has made a click
    if len(click_list) > 0:
        # Get the click from the mouse callback function
        x,y = click_list.pop(0)

        # Change the drawer if the user clicked on the cabinet
        for (left, right, bottom, top), name in zip(drawerLocations, drawerNames):
            #print(top, bottom, y)
            if x > left and x < right and y > bottom and y < top:
                currentDrawerNumber = drawerNames.index(name)
                currentDrawerName = drawerNames[currentDrawerNumber]
                currentPart = 0

        # Highlight the part if the user clicked in a bin
        # Move the x and y over to match the drawer image        
        xBuffer, yBuffer = 800,100
        x-=xBuffer
        y-=yBuffer
        drawerIndex = 0
        # Iterate through the bins
        for name, (a,b) in parts:
            # If the user clicks within a bin, that bin becomes the new selected bin
            if x > a[0] and x < b[0] and y > a[1] and y < b[1]: currentPart = drawerIndex
            drawerIndex += 1      
                
    # Get the image for the current drawer
    cdi = drawerImages[currentDrawerNumber]
    # Drawer the bin devisions in the drawer
    for name, (a,b) in parts:
        cdi = cv2.resize(cdi, (600,600))
        cv2.rectangle(cdi, a, b, (12,12,12), 2)
    # Highlight the bin that is currently selected
    name, (a,b) = parts[currentPart]
    cv2.rectangle(cdi, a, b, (0,255,0), 4)

    # Overlay the drawer on the background image
    img[100:700, 800:1400] = cdi

    # Highlight the drawer that is currently selected
    drawer = drawerLocations[currentDrawerNumber]
    a,b = (drawer[0], drawer[2]), (drawer[1], drawer[3])
    cv2.rectangle(img, a, b, (0,255,0), 8)

    # Put text to show the drawer, bin, min, max, on hand, and on order
    org = drawerXend + 25, 100
    binName, minimum, maximum = name.split(',')[:5]
    cv2.putText(img, 'bin: ' + binName, (400,130), font, scale, (255,255,0), thick, cv2.LINE_AA)
    cv2.putText(img, 'min: ' + minimum, (400,130+40), font, scale, (255,255,0), thick, cv2.LINE_AA)
    cv2.putText(img, 'max: ' + maximum, (400,130+80), font, scale, (255,255,0), thick, cv2.LINE_AA)
    cv2.putText(img, 'on hand: ' + str(quantityOnHand), (400,130+120), font, scale, (255,255,0), thick, cv2.LINE_AA)
    cv2.putText(img, 'qtyOrder: ' + str(quantityToOrder), (400,130+160), font, scale, (255,255,0), thick, cv2.LINE_AA)
    
    # Show the user that an order has been placed
    if countdownValue > 0:
        countdownValue -= 1
        partName, ohv, ov = order[-1]
        orderString = 'New Input: ' + partName
        orderString += '  On Hand: ' + str(ohv)
        orderString += '  On Order: ' + str(ov)
        cv2.putText(img, orderString, (100,800), font, 2, (255,2,255), 3)
        
    # Show frame    
    cv2.imshow('img', img)
    
    # Wait, and allow the user to quit with the 'esc' key
    k = cv2.waitKey(1)
    if k == 27: break

    # Get user input to collect quantity on hand and quantity to order
    if k == 56: quantityOnHand+=1
    if k == 50: quantityOnHand-=1
    if k == 54: quantityToOrder+=1
    if k == 52: quantityToOrder-=1

    # User has pressed enter to make an order
    if k == 13:
        order.append((name.split(',')[0], quantityOnHand, quantityToOrder))
        quantityOnHand=0
        quantityToOrder=0
        countdownValue = 240


cv2.destroyAllWindows()
print(order)

