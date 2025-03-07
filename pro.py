import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,1280)  #width
cap.set(4,720)  #height

# importing all images
imgBackground=cv2.imread("D:\project\Resources\Resources\Background.png")
# IMREAD_UNCHANGED FOR NO BG IMG
imgBall=cv2.imread("D:\project\Resources\Resources\Ball.png",cv2.IMREAD_UNCHANGED)
imgBat1=cv2.imread("D:\project\Resources\Resources\Bat1.png",cv2.IMREAD_UNCHANGED)
imgBat2=cv2.imread("D:\project\Resources\Resources\Bat2.png",cv2.IMREAD_UNCHANGED)
imgGameOver=cv2.imread("D:\project\Resources\Resources\gameOver.png")

#Hand Detector

detector = HandDetector(detectionCon=0.8,maxHands=2) 

#variables 
ballPos=[100,100]
speedX=10
speedY=10
gameOver=False
score=[0,0]
while True:
    _,img=cap.read()

 #image get flipped in horizontal direction

    img=cv2.flip(img,1)

   # Find the hand and its landmarks 
    hands, img= detector.findHands(img,flipType=False)

    img=cv2.addWeighted(img,0.2,imgBackground,0.8,0)
    #overlaying the background image 

# checking for hands 
    if hands:
      for hand in hands:
         x,y,w,h=hand["bbox"] #bounding box key 
         h1,w1,_=imgBat1.shape
         y1=y-h1//2
         y1=np.clip(y1,20,415)
         if hand['type']=="Left":
            img=cvzone.overlayPNG(img,imgBat1,(59,y1))
            if 59<ballPos[0]<59+w1 and y1<ballPos[1]<y1+h1:
                 speedX=-speedX
                 score[0]+=1

               #   ballPos +=30
         if hand['type']=="Right":
            img=cvzone.overlayPNG(img,imgBat2,(1195,y1))
            if 1195-50<ballPos[0]<1195 and y1<ballPos[1]<y1+h1:
               speedX=-speedX
               score[1]+=1
               # ballPos[0] -=30

#checking for gameover 
    if ballPos[0]<40 or ballPos[0]>1200:
      gameOver=True

    if gameOver:
        img=imgGameOver

        cv2.putText(img,str(max(score)).zfill(2),(585,360),cv2.FONT_HERSHEY_COMPLEX,2.5,(200,0,200),5)

   #if game not over we move game
    else:

      # MOVE the ball
     #changing ball direction in y axis 
     #500 and 10 are found using trail and error
      if ballPos[1]>=500 or ballPos[1]<=10:
       speedY=-speedY

      ballPos[0] +=speedX
      ballPos[1] +=speedY
      img=cvzone.overlayPNG(img,imgBall,ballPos)

      cv2.putText(img,str(score[0]),(300,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5,cv2.LINE_AA)
      cv2.putText(img,str(score[1]),(900,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5,cv2.LINE_AA)

      #draw the ball 
      # img=cvzone.overlayPNG(img,imgBall,(100,100))


    cv2.imshow("image",img)
    key=cv2.waitKey(1)  #1 milli sec wai
    if key==ord('R'):
      ballPos=[100,100]
      speedX=10
      speedY=10
      gameOver=False
      score=[0,0]
      imgGameOver=cv2.imread("D:\project\Resources\Resources\gameOver.png")

    # cap.release() 