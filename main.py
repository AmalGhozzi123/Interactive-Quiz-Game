import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import pyttsx3
import pygame

# Initialisation de la capture vidéo et configuration de la caméra
cap = cv2.VideoCapture(0)  #crée un objet de capture vidéo,argument 0  indique que la caméra par défaut du système doit être utilisée
cap.set(3, 1280)# largeur
cap.set(4, 720)# hauteur
# Initialisation du détecteur de main (HandDetector) avec un seuil de détection
detector = HandDetector(detectionCon=0.8)
# Initialisation du moteur de synthèse vocale (pyttsx3)
engine = pyttsx3.init()# initialise le moteur de synthèse vocale
pygame.init()#initialisation de  la bibliothèque Pygame
# Initialisation des sons corrects et incorrects avec la bibliothèque pygame
correct_sound = pygame.mixer.Sound(r"C:\Users\amalg\Downloads\correct-6033.mp3")
incorrect_sound = pygame.mixer.Sound(r"C:\Users\amalg\Downloads\negative_beeps-6008.mp3")
# Définition de la classe MCQ (Multiple Choice Question)
class MCQ():
    def __init__(self, data):
        # Initialisation avec les données d'une question
        self.question = data[0]
        self.choices = [data[1], data[2], data[3], data[4]]
        self.answer = int(data[5])
        self.userAns = None # indiquant que la réponse de l'utilisateur n'a pas encore été enregistrée.
        self.question_read = False # indiquant que la question n'a pas encore été lue.
        self.choices_read = [False, False, False, False] #Cela initialise la variable choices_read avec une liste de booléens indiquant si chaque choix a été lu ou non.
        self.start_time = None #indiquant que le minuteur n'a pas encore été démarré.
        self.question_timer = 25  # Temps limite pour chaque question en secondes
    # Fonction pour démarrer le minuteur de la question
    def start_timer(self):
        self.start_time = time.time()
    # Fonction pour obtenir le temps écoulé depuis le démarrage du minuteur
    def get_elapsed_time(self):
        return round(time.time() - self.start_time)

    # Fonction pour mettre à jour la question et les choix sur l'écran
    def update(self, img, cursor, bboxs, screen_width):
        global qNo  # Déclarez qNo comme variable globale
            # Draw question if not already read
        if not self.question_read:
            question_size = cv2.getTextSize(self.question, 2, 2, thickness=2)[0]
            question_x = (screen_width - question_size[0]) // 2
            img, _ = cvzone.putTextRect(img, self.question, [question_x, 100], 2, 2, offset=50, border=5,
                colorR=(50, 38, 15))
                # Read question using text-to-speech
            engine.say(self.question)
            engine.runAndWait()
            self.question_read = True
            self.start_timer()

        # Dessiner les choix si ils n'ont pas encore été lus
        for i, choice in enumerate(self.choices):
            # Dessiner la question si elle n'a pas encore été lue
            if not self.choices_read[i]:
                # Calculer la position de la question sur l'écran
                choice_size = cv2.getTextSize(choice, 2, 2, thickness=2)[0]
                choice_x = (screen_width - choice_size[0]) // 2
                y = 250 if i < 2 else 400
                img, bbox = cvzone.putTextRect(img, choice, [choice_x, y], 2, 2, offset=50, border=5, colorR=(50, 38, 15))
                # Lire la question à l'aide de la synthèse vocale
                engine.say(choice)
                engine.runAndWait()
                self.choices_read[i] = True

            x1, y1, x2, y2 = bboxs[i]
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = i + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (50, 38, 15), cv2.FILLED)  # Dark blue (Blue marine)



        if self.start_time:
            elapsed_time = self.get_elapsed_time()
            remaining_time = self.question_timer - elapsed_time
            color = (255, 0, 0) if remaining_time <= 5 else (0, 0, 255)
            cv2.putText(img, f"Time: {remaining_time}s", (100, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2,
                                cv2.LINE_AA)

            if remaining_time <= 0:
                self.userAns = None
                self.start_timer()
                incorrect_sound.play()
                qNo += 1

# Chemin du fichier CSV contenant les questions et les réponses
pathCSV = "Mcqs.csv"
# Lecture des données du fichier CSV
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# Création d'un objet pour chaque question (MCQ)
mcqList = []
for q in dataAll:
    if len(q) >= 6:
        mcqList.append(MCQ(q))
    else:
        print(f"Skipping invalid row: {q}")

print("Total MCQ objects Created:", len(mcqList))
qNo = 0
qTotal = len(mcqList)
score = 0

skip_question = False

try:
    while True:
        # Lecture d'une image depuis la caméra
        success, img = cap.read()
        img = cv2.flip(img, 1)
        # Détection des mains dans l'image
        hands, img = detector.findHands(img, flipType=False)

        if qNo < qTotal:
            mcq = mcqList[qNo]
            # Dessiner la question et les choix sur l'écran
            img, _ = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5, colorR=(50, 38, 15))
            img, bbox1 = cvzone.putTextRect(img, mcq.choices[0], [100, 250], 2, 2, offset=50, border=5, colorR=(50, 38, 15))
            img, bbox2 = cvzone.putTextRect(img, mcq.choices[1], [400, 250], 2, 2, offset=50, border=5, colorR=(50, 38, 15))
            img, bbox3 = cvzone.putTextRect(img, mcq.choices[2], [100, 400], 2, 2, offset=50, border=5, colorR=(50, 38, 15))
            img, bbox4 = cvzone.putTextRect(img, mcq.choices[3], [400, 400], 2, 2, offset=50, border=5, colorR=(50, 38, 15))

            # Dessiner le bouton de saut avec une position et une étiquette ajustées
            cv2.rectangle(img, (1000, 50), (1150, 100), (255, 0, 0), cv2.FILLED)  # Red color for skip button
            cv2.putText(img, "Skip", (1010, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            if hands:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info, img = detector.findDistance((lmList[8][0], lmList[8][1]),
                                                          (lmList[12][0], lmList[12][1]), img,
                                                          color=(255, 0, 255), scale=10)

                if length < 60:
                    mcq.update(img, cursor, [bbox1, bbox2, bbox3, bbox4], img.shape[1])

                    if mcq.userAns is not None:
                        correct_sound.play() if mcq.answer == mcq.userAns else incorrect_sound.play()
                        time.sleep(2) # Introduire une pause après l'affichage de chaque question
                        qNo += 1  # Incrémentez qNo ici

                # Vérifier le clic sur le bouton de saut
                skip_button_rect = [(1000, 50), (1150, 100)]
                if skip_button_rect[0][0] < cursor[0] < skip_button_rect[1][0] and skip_button_rect[0][1] < cursor[1] < skip_button_rect[1][1]:
                    qNo += 1
                    mcq.userAns = None
                    mcq.start_timer() # Redémarrer le minuteur après avoir sauté la question
                    time.sleep(2)  # Introduire une pause après avoir sauté la question

        else:
            score = 0
            for mcq in mcqList:
                if mcq.answer == mcq.userAns:
                    score += 1
            score = round((score / qTotal) * 100, 2)
            img, _ = cvzone.putTextRect(img, "Quiz completed ", [250, 300], 2, 2, offset=50, border=5,
                                        colorR=(50, 38, 15))
            img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5,
                                        colorR=(50, 38, 15))

        barValue = 150 + (950 // qTotal) * qNo
        cv2.rectangle(img, (150, 600), (barValue, 650), (50, 38, 15), cv2.FILLED)  # Dark blue (Blue marine)
        cv2.rectangle(img, (150, 600), (1150, 650), (50, 38, 15), 5)  # Dark blue (Blue marine)
        img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=50, border=5,
                                    colorR=(50, 38, 15))
        # Afficher l'image
        cv2.imshow("Img", img)
        cv2.waitKey(1)  # Ajoutez cette ligne pour éviter le blocage de l'écran
# Gestion de l'interruption du clavier
except KeyboardInterrupt:
    print("Interrupted. Releasing resources.")
    cap.release()
    cv2.destroyAllWindows()
