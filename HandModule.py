import cv2
import mediapipe as mp

red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)


class Detector():
    def __init__(self , mode = False , maxHands = 2 ,
                 detectionCon = 0.5  , trackingCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mediapipeHands = mp.solutions.hands
        self.hands = self.mediapipeHands.Hands(self.mode , self.maxHands,
                                            self.detectionCon , self.trackingCon)
        self.Draw = mp.solutions.drawing_utils
        self.Indexes = [4,8,12,16,20]
    def findHands(self , frame , draw = True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.Draw.draw_landmarks(frame,handlandmarks
                                             , self.mediapipeHands.HAND_CONNECTIONS)
        return frame

    def Position(self , frame , handNo = 0 , draw = True):
        self.landmarkList = []
        if self.results.multi_hand_landmarks:
            myHands = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myHands.landmark):
                #print(id , lm)
                h,w,c = frame.shape
                x , y = int(lm.x*w) , int(lm.y*h)
                self.landmarkList.append([id,x,y])
                if draw:
                    cv2.circle(frame , (x,y) , 8 , red , -1)
        return self.landmarkList

    def fing_up(self):
        fingers = []

        for index in range(1, 5):
            if self.landmarkList[self.Indexes[index]][2] < self.landmarkList[self.Indexes[index] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Thumb
        if self.landmarkList[self.Indexes[0]][1] > self.landmarkList[self.Indexes[0] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        return fingers
def main():
    cap = cv2.VideoCapture(0)
    detector = Detector()
    while True:
        _, frame = cap.read()
        frame = detector.findHands(frame)
        landmarkList = detector.Position(frame)
        if len(landmarkList) != 0:
            print(landmarkList[4])

        cv2.imshow('Webcam' , frame)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()