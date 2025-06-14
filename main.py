import cv2
import csv
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize hand detector with detection confidence and max hands
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Define color used for UI (dark blue in BGR)
DARK_BLUE = (139, 0, 0)

# ---------- COUNTDOWN BEFORE QUIZ START ----------
countdown_start = True
countdown_done = False
countdown_start_time = None
countdown_duration = 5  # seconds

# Class to represent each MCQ
class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None  # Initially unanswered

    # Update answer based on finger position
    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)  # Highlight selection

# Load questions from CSV file
pathCSV = "Mcqs.csv"
with open(pathCSV, newline="\n") as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]  # Skip header

# Create a list of MCQ objects
mcqList = [MCQ(q) for q in dataAll]
print("Total MCQ Objects Created:", len(mcqList))

# Quiz control variables
qNo = 0
qTotal = len(dataAll)
start_time = None
time_per_question = 15  # seconds
quiz_completed = False
waiting_for_next = False
answer_time = None

# ---------- MAIN LOOP ----------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror view
    hands, img = detector.findHands(img, flipType=False)

    # ---------- SHOW COUNTDOWN BEFORE QUIZ ----------
    if countdown_start and not countdown_done:
        if countdown_start_time is None:
            countdown_start_time = time.time()
        elapsed = int(time.time() - countdown_start_time)
        countdown_val = countdown_duration - elapsed
        if countdown_val > 0:
            img, _ = cvzone.putTextRect(img, f'Starting in {countdown_val}', [500, 300], 4, 4, offset=30, border=8, colorR=(0, 0, 255))
        else:
            countdown_done = True
            countdown_start = False
            start_time = time.time()  # Start the quiz timer

        cv2.imshow("Img", img)
        cv2.waitKey(1)
        continue

    # ---------- MAIN QUIZ INTERFACE ----------
    if qNo < qTotal and not quiz_completed:
        mcq = mcqList[qNo]

        # Display current question and its choices
        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5, colorR=DARK_BLUE)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5, colorR=DARK_BLUE)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5, colorR=DARK_BLUE)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5, colorR=DARK_BLUE)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5, colorR=DARK_BLUE)

        # Detect hand gesture and check if fingers are pinched
        if hands and not waiting_for_next:
            lmList = hands[0]["lmList"]
            cursor = lmList[8]  # Index fingertip
            length, info, img = detector.findDistance((lmList[8][0], lmList[8][1]),
                                                      (lmList[12][0], lmList[12][1]), img)
            if length < 60:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    waiting_for_next = True
                    answer_time = time.time()

        # Display countdown timer for each question
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_per_question - elapsed_time)
        img, _ = cvzone.putTextRect(img, f'Time Left: {int(remaining_time)}s', [1000, 50], 2, 2, offset=20, border=5, colorR=DARK_BLUE)

        # Move to next question if time is up
        if remaining_time <= 0 and not waiting_for_next:
            qNo += 1
            start_time = time.time()

        # Move to next question after 3 seconds of answering
        if waiting_for_next and (time.time() - answer_time >= 3):
            qNo += 1
            start_time = time.time()
            waiting_for_next = False

        # Indicate loading next question
        if waiting_for_next:
            img, _ = cvzone.putTextRect(img, "Next question loading...", [450, 550], 2, 2, offset=10, border=4, colorR=DARK_BLUE)

        # Draw progress bar at bottom
        barValue = 150 + (950 // qTotal) * qNo
        cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (150, 600), (1100, 650), DARK_BLUE, 5)
        img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16, colorR=DARK_BLUE)

    # ---------- QUIZ COMPLETED ----------
    else:
        if not quiz_completed:
            score = sum(1 for mcq in mcqList if mcq.answer == mcq.userAns)
            score_percentage = round((score / qTotal) * 100, 2)

            # Display final score
            img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5, colorR=DARK_BLUE)
            img, _ = cvzone.putTextRect(img, f'Your Score: {score_percentage}%', [700, 300], 2, 2, offset=50, border=5, colorR=DARK_BLUE)

            # Save score in a CSV file
            with open("score_history.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), score_percentage])

            # Display incorrect answers
            for idx, mcq in enumerate(mcqList):
                if mcq.answer != mcq.userAns:
                    img, _ = cvzone.putTextRect(img, f'Q{idx + 1}: {mcq.question}', [100, 400 + idx * 50], 2, 2, offset=20, border=5, colorR=DARK_BLUE)
                    img, _ = cvzone.putTextRect(img, f'Correct Answer: {mcq.answer}', [700, 400 + idx * 50], 2, 2, offset=20, border=5, colorR=DARK_BLUE)

            quiz_completed = True
        else:
            # Show quiz summary screen
            img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5, colorR=DARK_BLUE)
            img, _ = cvzone.putTextRect(img, f'Your Score: {score_percentage}%', [700, 300], 2, 2, offset=50, border=5, colorR=DARK_BLUE)

            # Repeat incorrect answers
            for idx, mcq in enumerate(mcqList):
                if mcq.answer != mcq.userAns:
                    img, _ = cvzone.putTextRect(img, f'Q{idx + 1}: {mcq.question}', [100, 400 + idx * 50], 2, 2, offset=20, border=5, colorR=DARK_BLUE)
                    img, _ = cvzone.putTextRect(img, f'Correct Answer: {mcq.answer}', [700, 400 + idx * 50], 2, 2, offset=20, border=5, colorR=DARK_BLUE)

    # Show webcam feed with overlays
    cv2.imshow("Img", img)
    cv2.waitKey(1)
