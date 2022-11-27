import cv2
import cvzone

from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

#imgBackground = cv2.imread("assets/backgrounds/nightbackgroundwithmoon.png")
imgBackground = cv2.imread("Resources/soccerfield.png")

#imgBackground = cv2.imread("Resources/Background.png")

#imgGameOver = cv2.imread("Resources/noonbackground.png")
imgWinGirl = cv2.imread("Resources/girlWon.png")
imgWinBoy = cv2.imread("Resources/boyWon.png")

imgBall = cv2.imread("Resources/ball21.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/girl1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/boy1.png", cv2.IMREAD_UNCHANGED)
#imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
#imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
detector = HandDetector(detectionCon=0.8, maxHands=2)
#Player HP
imgHeart = cv2.imread("Resources/heart.png", cv2.IMREAD_UNCHANGED)


# Variables
defaultBallPos = [600, 310]
ballPos = defaultBallPos
speedX = 25
speedY = 25
gameOver = False
score = [0, 0]

girlHP = 3
boyHP = 3

tmp = 1
rand = random.randint(0, 1)
if rand == 0:
    tmp = -1
else:
    tmp = 1


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    #Find the hands
    hands, img = detector.findHands(img, flipType=False)
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0.0)
    
    # Check for hands
    if hands:
        for hand in hands:
            x,y,w,h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 70 < ballPos[0] < 70 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 100
                    score[0] += 1
                    imgBat1 = cv2.imread("Resources/girljump.png", cv2.IMREAD_UNCHANGED)

                else:
                    imgBat1 = cv2.imread("Resources/girl1.png", cv2.IMREAD_UNCHANGED)

            if hand['type'] == "Right":
                #img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                img = cvzone.overlayPNG(img, imgBat2, (1100, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 50
                    score[1] += 1
                    imgBat2 = cv2.imread("Resources/boyjump.png", cv2.IMREAD_UNCHANGED)
                else:
                    imgBat2 = cv2.imread("Resources/boy1.png", cv2.IMREAD_UNCHANGED)

    #Game over
    # if ballPos[0] < 40 or ballPos[0] > 1200:
    #     gameOver = True
    # if gameOver:
    #     img = imgGameOver
    #     cv2.putText(img, str(score[1] + score[0]), (585, 368), cv2.FONT_HERSHEY_COMPLEX, 2.5, (153, 0, 0), 5)
    #
    #print(ballPos)

    if ballPos[0] < 80 and girlHP > 0:
        girlHP -= 1
        #ballPos = defaultBallPos
        ballPos[0] = 500
        rand = random.randint(0, 1)
        if rand == 0:
            tmp = -1
        else:
            tmp = 1
        print(f"Girl {girlHP}")
        # gameOver = True
    if ballPos[0] > 1140 and boyHP > 0:
        boyHP -= 1 
        ballPos[0] = 500
        rand = random.randint(0, 1)
        if rand == 0:
            tmp = -1
        else:
            tmp = 1
        print(f"Boy {boyHP}")
        # gameOver = True


    # if gameOver:
    #     #print(ballPos)
    #     #ballPos[0] = 500
    #     speedX = 25
    #     speedY = 25
    #     gameOver = False
    #       # Girl Won
        
    #     continue
        #continue 
        # Girl Won
        # if boyHP == 0:
        #     img = imgWinGirl
        #     cv2.putText(img, str(score[0]), (585, 368), cv2.FONT_HERSHEY_COMPLEX, 2.5, (153, 0, 0), 5)
        # # Boy Won
        # elif girlHP == 0:
        #     img = imgWinBoy
        #     cv2.putText(img, str(score[1]), (585, 368), cv2.FONT_HERSHEY_COMPLEX, 2.5, (153, 0, 0), 5)
    else:
      
        #Move the ball
        if ballPos[1] >= 560 or ballPos[1] <= 10:
            speedY = -speedY

        
        ballPos[0] += speedX * tmp 
        ballPos[1] += speedY * tmp
            
        

        #Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)
    
        ballPos = defaultBallPos
        
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        #Draw the HP 
        #Girl's HP
        for i in range(1, girlHP + 1):
            img = cvzone.overlayPNG(img, imgHeart,(100 + (50 * i), 20))
        #Boy's HP
        for i in range(1, boyHP + 1):
            img = cvzone.overlayPNG(img, imgHeart, (1180 - (50 * i), 20))

        #Girl Won
        if boyHP == 0 or girlHP == 0:
            if score[0] > score[1]:
                gameOver = True
                img = imgWinGirl
                cv2.putText(img, str(score[0]), (585, 368), cv2.FONT_HERSHEY_COMPLEX, 2.5, (153, 0, 0), 5)
            #Boy Won
            else:
                gameOver = True
                img = imgWinBoy
                cv2.putText(img, str(score[1]), (585, 368), cv2.FONT_HERSHEY_COMPLEX, 2.5, (153, 0, 0), 5)
                
            

        cv2.imshow('Game', img)
        if gameOver:
            gameOver = False
            time.sleep(1)
        key = cv2.waitKey(1)
        if key == ord('r'):
            ballPos = defaultBallPos
            speedX = 25
            speedY = 25
            gameOver = False
            girlHP = 3
            boyHP = 3
            score[0] = 0
            score[1] = 0
    #     #score = [0, 0]
    #     #imgGameOver = cv2.imread("Resources/gameOver.png")
        