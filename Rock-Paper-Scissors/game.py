import cv2
import random
import hand_tracker as htm
from config import *

#! Global Variables
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (255,0,0)
RED = (0,0,255)
GREEN = (0,255,0)
CAM_WIDTH = 1440
CAM_HEIGHT = 1080

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

detector = htm.HandDetector()
font = cv2.FONT_HERSHEY_SIMPLEX
option = 0
text = ""
cc = CHOOSE_COUNTDOWN
wc = WAIT_COUNTDOWN
player_pts = 0
computer_pts = 0
flag = True
pos = 1200

while True:
    success, img = cap.read()
    if FLIP:
        img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        fingers = detector.fingersUp()
        s = sum(fingers)

        if flag:
            if s==0:
                text = "ROCK"
                option = 1
            elif fingers[1]==1 and fingers[2]==1 and s==2:
                text = "SCISSORS"
                option = 2
            elif s==5:
                text = "PAPER"
                option = 3
            else:
                text = "ERROR"
                option = 4

            cv2.putText(img, str(cc), (620,50), font, 1, BLUE, 3)
        cv2.putText(img, text, (20,50), font, 1, BLUE, 3)

        cc -= 1
        if cc<0:
            cv2.putText(img, str(wc), (620,50), font, 1, BLUE, 3)
            if flag:
                r = random.randint(1,3)
                if option==4:
                    cc = CHOOSE_COUNTDOWN
                    continue
                elif option==1:
                    if r==2:
                        player_pts += 1
                    elif r==3:
                        computer_pts += 1
                elif option==2:
                    if r==1:
                        computer_pts += 1
                    elif r==3:
                        player_pts += 1
                else:
                    if r==1:
                        player_pts += 1
                    elif r==2:
                        computer_pts += 1

                pos = 1200 - (len(str(computer_pts))-1)*20
                flag = False

            wc -= 1
            if r==1:
                cv2.putText(img, "ROCK", (CAM_WIDTH-285,50), font, 1, BLUE, 3)
            elif r==2:
                cv2.putText(img, "SCISSORS", (CAM_WIDTH-350,50), font, 1, BLUE, 3)
            else:
                cv2.putText(img, "PAPER", (CAM_WIDTH-300,50), font, 1, BLUE, 3)
            
            if wc<0:
                flag = True
                cc = CHOOSE_COUNTDOWN
                wc = WAIT_COUNTDOWN
    
    total = player_pts + computer_pts
    cv2.rectangle(img, (50,CAM_HEIGHT-450), (1230, CAM_HEIGHT-400), RED, cv2.FILLED)
    if (total == 0):
        cv2.rectangle(img, (50,CAM_HEIGHT-450), (640,CAM_HEIGHT-400), GREEN, cv2.FILLED)
    else:
        l = 1180*player_pts/total
        cv2.rectangle(img, (50,CAM_HEIGHT-450), (50+int(l),CAM_HEIGHT-400), GREEN, cv2.FILLED)

    cv2.putText(img, "COMPUTER", (1060,CAM_HEIGHT-460), font, 1, RED, 3)
    cv2.putText(img, str(computer_pts), (pos,CAM_HEIGHT-415), font, 1, WHITE, 3)
    cv2.putText(img, NAME, (50,CAM_HEIGHT-460), font, 1, GREEN, 3)
    cv2.putText(img, str(player_pts), (60,CAM_HEIGHT-415), font, 1, BLACK, 3)

    cv2.imshow(f'Rock Paper Scissors v{VERSION} by Adit Jain', img)
    cv2.waitKey(1)