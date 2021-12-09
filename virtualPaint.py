import cv2
import numpy as np

def empty(x):
    pass

# cv2.namedWindow("TrackBars")
# cv2.resizeWindow("TrackBars",640,240)
# cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
# cv2.createTrackbar("Hue Max","TrackBars",0,179,empty)
# cv2.createTrackbar("Sat Min","TrackBars",0,179,empty)
# cv2.createTrackbar("Sat Max","TrackBars",0,179,empty)
# cv2.createTrackbar("Val Min","TrackBars",0,179,empty)
# cv2.createTrackbar("Val Max","TrackBars",0,179,empty)

myColors=np.array([69,179,0,47,0,140])








def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>2000:
            #cv2.drawContours(imgContour,cnt,-1,(0,0,255),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)

            x,y,w,h=cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
    return x+w//2,y+h//2



vid=cv2.VideoCapture(1)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
myPoints=[]
col_var=(255,0,0)
while True:

    success, img = vid.read()
    img = cv2.flip(img, 1)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgContour=img.copy()



    hue_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    lower=np.array([hue_min,sat_min,val_min])
    upper=np.array([hue_max,sat_max,val_max])
    #print(hue_min,hue_max,sat_min,sat_max,val_min,val_max)
    mask=cv2.inRange(img,myColors[::2],myColors[1::2])
    x,y=getContours(mask)
    if x!=0 and y!=0:
        if 0 <= x <= 100 and 0 <= y <= 50:
            col_var = (255, 0, 0)
        if 150 <= x <= 250 and 0 <= y <= 50:
            col_var = (0, 255, 0)
        if 300 <= x <= 400 and 0 <= y <= 50:
            col_var = (0, 0, 255)
        if 450 <= x <= 550 and 0 <= y <= 50:
            col_var = (0, 0, 0)
        if 600 <= x <= 700 and 0 <= y <= 50:
            col_var = (255, 255, 255)
        if 750 <= x <= 850 and 0 <= y <= 50:
            myPoints = []
        myPoints.append([x,y,col_var])



    for point in myPoints:

        cv2.circle(imgContour,(point[0],point[1]),5,point[2],cv2.FILLED)

    #print(col_var)

    cv2.rectangle(imgContour, (0, 0), (100, 50), (255, 0, 0), -1)
    cv2.rectangle(imgContour, (150, 0), (250, 50), (0, 255, 0), -1)
    cv2.rectangle(imgContour, (300, 0), (400, 50), (0, 0, 255), -1)
    cv2.rectangle(imgContour, (450, 0), (550, 50), (0, 0, 0), -1)
    cv2.rectangle(imgContour, (600, 0), (700, 50), (255, 255, 255), -1)
    cv2.rectangle(imgContour, (750, 0), (850, 50), (0, 0, 0), -1)
    cv2.putText(imgContour, "CLEAR", (750, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgContour, "BLUE", (0, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgContour, "GREEN", (150, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgContour, "RED", (300, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgContour, "BLACK", (450, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgContour, "WHITE", (600, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    #cv2.imshow("video", stackImages(0.6, [img, imgHSV,mask,imgContour]))
    cv2.imshow("video",imgContour)


    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
print(myPoints )