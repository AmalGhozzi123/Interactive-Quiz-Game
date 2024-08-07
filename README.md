# 🧠 Interactive Quiz with Gesture Detection ✋

## 🎯 Project Objective

The project involves developing an interactive multiple-choice quiz using gesture detection. The application allows users to answer quiz questions by selecting answers through gestures captured by a camera. Results are displayed in real-time with sound effects for each correct or incorrect answer. A timer is integrated for each question, adding a time challenge, and a "skip" function is available to move to the next question.
## ⚙️ Technologies Used

- **Python**: The programming language used for developing the project. 🐍

### Libraries

- **OpenCV** : Used for video capture and gesture detection. 🎥
- **Cvzone** : Library for facilitating graphical element manipulation on the image. 🖼️
- **Pygame** : Used for sound effects associated with correct and incorrect answers. 🔊
- **Pyttsx3** : Text-to-speech library for reading questions and choices aloud. 🗣️


## 🚀 How the Project Works

1. **Initialization** :
   - Configure the webcam for video capture. 📷
   - Initialize hand detector to track user gestures. ✋
   - Load sound effects for correct and incorrect answers. 🎵
   - Integrate a timer for each question. ⏲️

2. **Loading Questions** :
   - Questions and choices are loaded from a CSV file (`Mcqs.csv`). 📄
   - Create MCQ objects for each set of questions. 📝

3. **Displaying Questions and Choices** :
   - Questions and choices are displayed on the screen with voice reading. 📺🔊
   - Choice selection areas are defined, allowing users to answer through gestures. ✋

4. **Gesture Interaction** :
   - Detect hand position to track the cursor. 🖱️
   - Select choices by positioning the cursor in the respective areas. 📍
   - "Skip" function to move to the next question. ⏭️

5. **Processing Answers** :
   - User responses are processed after each selection. ✔️❌
   - Provide audio feedback and update the score. 📈

6. **Quiz Progression** :
   - A progress bar indicates quiz advancement. 📊
   - Partial results are displayed after each question. 🔢

7. **End of Quiz** :
   - Calculate and display the final score. 🏆
   - Announce the end of the quiz. 🎉
## 🚀 How to Deploy the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AmalGhozzi123/Interactive-Quiz-Game.git
2. **Install Dependencies**
- Make sure you have Python 3.6 or higher installed on your system.
- Install the required libraries using pip :
  `pip install opencv-python-headless cvzone pygame pyttsx3`


3. **Prepare the Data**
- Ensure the Mcqs.csv file is present in the project directory. This file contains the quiz questions and choices.

4. **Configure the Webcam**
- Make sure your webcam is connected and accessible by OpenCV.

5. **Run the Application**
- Execute the script to start the quiz:

## 🧩 Additional Information
Feel free to modify and extend this project to suit your needs. If you encounter any issues or need further assistance, you can contact me at amalghozzi@outlook.com.
