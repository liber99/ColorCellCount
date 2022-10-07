import cv2
import numpy as np

def empty(v):
    pass

def drawRect(v):
    barH = 50
    barW = 640
    #for i in list([1,4,7]):
    #    cv2.rectangle('TrackBar',(0, barH*i),(barW, barH*i+barH),(0,255,0),-1)

orgImg = cv2.imread('Test2.jpg')
#img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

hsv = cv2.cvtColor(orgImg, cv2.COLOR_BGR2HSV)
curH, curS, curV = 0,0,0
def pickColor(event, x, y, flags, param):
    global curH, curS, curV
    if event == cv2.EVENT_LBUTTONUP:
        #cv2.circle(img,(x,y),100,(255,0,0),-1)
        #print("At (", x, ",", y, "), HSV = " , hsv[y, x, :])
        curH, curS, curV = hsv[y, x, 0], hsv[y, x, 1], hsv[y, x, 2]
        cv2.setTrackbarPos('Hue Cur', 'TrackBar', curH)
        cv2.setTrackbarPos('Sat Cur', 'TrackBar', curS)
        cv2.setTrackbarPos('Val Cur', 'TrackBar', curV)

maskOrOrg = 0
#def switchImg(event, x, y, flags, param):
def switchImg(*args):    
    global maskOrOrg
    maskOrOrg = 1 if (maskOrOrg == 0) else  0
    print("switchImg clicked!  maskOrOrg = ", maskOrOrg)

wndName = 'SpaceKeyTagOrigMask'
cv2.namedWindow(wndName)
cv2.setMouseCallback(wndName, pickColor)
cv2.imshow(wndName, orgImg)
#cv2.setMouseCallback(wndName, switchImg)

# About TrackBar
cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 640, 800)

cv2.createTrackbar('Hue Min', 'TrackBar', 0, 179, empty)
cv2.createTrackbar('Hue Cur', 'TrackBar', 90, 179, drawRect)
cv2.createTrackbar('Hue Max', 'TrackBar', 15, 179, empty)
cv2.createTrackbar('Hue Min2', 'TrackBar', 160, 179, empty)
cv2.createTrackbar('Hue Max2', 'TrackBar', 179, 179, empty)
cv2.createTrackbar('Sat Min', 'TrackBar', 128, 255, empty)
cv2.createTrackbar('Sat Cur', 'TrackBar', 128, 255, drawRect)
cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBar', 105, 255, empty)
cv2.createTrackbar('Val Cur', 'TrackBar', 128, 255, drawRect)
cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('Area min', 'TrackBar', 5, 50, empty)

# Create a black image, a window and bind the function to window
cv2.namedWindow('Info')
cv2.resizeWindow('Info', 600, 400)
infoImg = np.zeros((100,600,3), np.uint8)
infoImg.fill(128)
cv2.putText(img=infoImg, text='Picked color:', org=(10, 20), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 255, 0),thickness=1)

imgIndex = 2
preIndex = 1
while True:
    #cv2.imshow('orgImage', orgImg)
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    h_min2 = cv2.getTrackbarPos('Hue Min2', 'TrackBar')
    h_max2 = cv2.getTrackbarPos('Hue Max2', 'TrackBar')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    a_min = cv2.getTrackbarPos('Area min', 'TrackBar')
    #print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask1 = cv2.inRange(hsv, lower, upper)

    lower = np.array([h_min2, s_min, v_min])
    upper = np.array([h_max2, s_max, v_max])
    mask2 = cv2.inRange(hsv, lower, upper)

    mask = cv2.bitwise_or(mask1, mask2)
    result = cv2.bitwise_and(orgImg, orgImg, mask=mask)

    # Find shape
    imgContour = result.copy()
    img = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(img, 150, 200)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    iCnt = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > a_min):
            cv2.drawContours(imgContour, cnt, -1, (255, 255, 255), 1)
            iCnt = iCnt + 1

    #cv2.imshow('ImgContours', imgContour)
    if (imgIndex == 1):
        cv2.imshow(wndName, orgImg)
    elif (imgIndex == 2):
        cv2.imshow(wndName, imgContour)
    elif (imgIndex == 3):
        cv2.imshow(wndName, mask)

    # Information Window
    infoImg2 = infoImg.copy()
    cv2.putText(img=infoImg2, text='Counts=:'+str(iCnt), org=(150, 20), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(255, 0, 0),thickness=1)

    rgb = cv2.cvtColor(np.uint8([[(curH, curS, curV)]]), cv2.COLOR_HSV2BGR)[0][0]
    cv2.rectangle(infoImg2, (10,30), (120,90), rgb.tolist(),-1)
    cv2.imshow('Info', infoImg2)

    tmpKey = cv2.waitKey(1) & 0xFF
    if tmpKey == 32:  # Space
        tSwap = imgIndex
        imgIndex = preIndex
        preIndex = tSwap
        #maskOrOrg = 1 if (maskOrOrg == 0) else  0
        #if (maskOrOrg == 1):
        #    cv2.imshow('ImgContours', imgContour)
        #else:
        #    cv2.imshow('ImgContours', orgImg)
    elif tmpKey == 49:
        imgIndex = 1
    elif tmpKey == 50:
        imgIndex = 2
    elif tmpKey == 51:
        imgIndex = 3
    elif tmpKey != 255:
        print(tmpKey)
        


