import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

aiMoves = {}
for i in range(1, 4):
    img = cv2.imread(f'Resources/{i}.png', cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    aiMoves[i] = img

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
imgAI = None

while True:
    imgBG = cv2.imread("resources/BG.png")
    success, img = capture.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.8, 0.8)
    imgScaled = imgScaled[:, 40:1000]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_DUPLEX, 4, (255, 0, 255), 10)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    print(fingers)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                    print(playerMove)



                    randomNumber = random.randint(1, 3)
                    imgAI = aiMoves[randomNumber]
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (100, 250))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                        # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
            if stateResult:
                if imgAI.shape[2] == 3:
                    imgAI = cv2.cvtColor(imgAI, cv2.COLOR_BGR2BGRA)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (100, 250))

    imgBG[216:600, 789:1261] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (100, 250))


    cv2.putText(imgBG, str(scores[0]), (330, 140), cv2.FONT_HERSHEY_DUPLEX, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 140), cv2.FONT_HERSHEY_DUPLEX, 4, (255, 255, 255), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

