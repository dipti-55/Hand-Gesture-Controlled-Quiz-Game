import cv2
import csv
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=2)

class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

# Import CSV file data
pathCSV = "Mcqs.csv"
with open(pathCSV, newline="\n") as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# Create Object for each MCQ
mcqList = [MCQ(q) for q in dataAll]
print("Total MCQ Objects Created:", len(mcqList))

qNo = 0
qTotal = len(dataAll)
start_time = time.time()
time_per_question = 15  # seconds
quiz_completed = False  # Flag to indicate if the quiz is completed

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if qNo < qTotal and not quiz_completed:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

        if hands:
            lmList = hands[0]["lmList"]
            cursor = lmList[8]
            length, info, img = detector.findDistance((lmList[8][0], lmList[8][1]), (lmList[12][0], lmList[12][1]), img)
            if length < 60:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo += 1
                    start_time = time.time()

        # Countdown Timer
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_per_question - elapsed_time)
        img, _ = cvzone.putTextRect(img, f'Time Left: {int(remaining_time)}s', [1000, 50], 2, 2, offset=20, border=5)
        if remaining_time <= 0:
            qNo += 1
            start_time = time.time()

        # Draw Progress Bar
        barValue = 150 + (950 // qTotal) * qNo
        cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
        img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

    else:
        if not quiz_completed:
            score = sum(1 for mcq in mcqList if mcq.answer == mcq.userAns)
            score_percentage = round((score / qTotal) * 100, 2)
            img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
            img, _ = cvzone.putTextRect(img, f'Your Score: {score_percentage}%', [700, 300], 2, 2, offset=50, border=5)

            # Save score history
            with open("score_history.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), score_percentage])

            # Review incorrect answers
            for idx, mcq in enumerate(mcqList):
                if mcq.answer != mcq.userAns:
                    img, _ = cvzone.putTextRect(img, f'Q{idx + 1}: {mcq.question}', [100, 400 + idx * 50], 2, 2, offset=20, border=5)
                    img, _ = cvzone.putTextRect(img, f'Correct Answer: {mcq.answer}', [700, 400 + idx * 50], 2, 2, offset=20, border=5)

            quiz_completed = True  # Set the flag to indicate the quiz is completed

        else:
            img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
            img, _ = cvzone.putTextRect(img, f'Your Score: {score_percentage}%', [700, 300], 2, 2, offset=50, border=5)

            # Review incorrect answers
            for idx, mcq in enumerate(mcqList):
                if mcq.answer != mcq.userAns:
                    img, _ = cvzone.putTextRect(img, f'Q{idx + 1}: {mcq.question}', [100, 400 + idx * 50], 2, 2, offset=20, border=5)
                    img, _ = cvzone.putTextRect(img, f'Correct Answer: {mcq.answer}', [700, 400 + idx * 50], 2, 2, offset=20, border=5)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
