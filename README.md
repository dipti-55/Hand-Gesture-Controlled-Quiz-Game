
# Hand-Gesture Controlled Quiz Game

### Navigate through a quiz using just hand gestures! This project uses computer vision to provide an interactive and touch-free quiz experience.

## 🚀 Features

- **Hand Gesture Detection**: Uses a webcam to detect hand gestures for selecting quiz answers.
- **Multiple Choice Questions (MCQs)**: Displays questions and options in a user-friendly interface.
- **Interactive Visual Feedback**: Highlights the selected answer dynamically using green boxes.
- **Real-Time Countdown Timer**: Ensures each question is answered within a specified time.
- **Progress Bar**: Visually tracks quiz completion.
- **Scoring System**: Automatically calculates and displays the score at the end of the quiz.
- **Score History**: Saves quiz scores along with timestsamps in a CSV file.
- **Review Incorrect Answers**: Highlights incorrectly answered questions with correct answers for post-quiz review.

---

## 🛠️ Tech Stack

- **Programming Language**: Python
- **Libraries Used**:
  - [OpenCV](https://opencv.org/) for computer vision tasks
  - [cvzone](https://github.com/cvzone/cvzone) for UI components
  - [HandDetector Module](https://github.com/cvzone/cvzone) for hand gesture recognition
  - [csv](https://docs.python.org/3/library/csv.html) for managing score history

---

## 🎯 How It Works

1. **Start Quiz**:
   - The application captures video input using your webcam.
   - It displays a question with four options on the screen.

2. **Hand Gesture Selection**:
   - Move your hand to position the cursor (index finger tip) over an option.
   - Pinch your fingers (index and middle finger) to select the option.

3. **Dynamic Feedback**:
   - Selected options are highlighted with a green rectangle.

4. **Time Management**:
   - A countdown timer ensures you answer each question within the allotted time.

5. **Quiz Completion**:
   - At the end of the quiz, the application displays your score as a percentage.
   - Incorrect answers and their correct answers are shown for review.
   - Your score is saved in a `score_history.csv` file for future reference.


## 📂 File Structure

```
├── main.py               # Main application file
├── Mcqs.csv              # File containing quiz questions and answers
├── score_history.csv     # File to store score history with timestamp
└── README.md             # Project documentation
```

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dipti-55/Hand-Gesture-Controlled-Quiz-Game.git
   cd Hand-Gesture-Controlled-Quiz-Game
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your quiz data in the `Mcqs.csv` file.

---

## 🖥️ Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The webcam feed will open, displaying the quiz interface.

3. Use your hand to interact:
   - Point to an option using your index finger.
   - Pinch your index and middle fingers to select the answer.

4. Complete the quiz and review your results!

---

## 🧩 Example of `Mcqs.csv`

```csv
Question,Option1,Option2,Option3,Option4,Answer
What is the capital of France?,Paris,London,Berlin,Madrid,1
What is 2+2?,3,4,5,6,2
Which planet is known as the Red Planet?,Venus,Earth,Mars,Jupiter,3
```

---

## 🔥 Highlights

- **Touch-Free Interface**: A unique approach to conducting quizzes without any physical interaction.
- **Interactive Feedback**: Provides immediate visual cues for selections, progress bar and timer.
- **Customizable**: Easily modify the quiz questions by editing the `Mcqs.csv` file.

