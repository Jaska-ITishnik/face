import os

import cv2
import numpy as np
from PIL import Image

from root.settings import BASE_DIR

detector = cv2.CascadeClassifier(BASE_DIR + '/apps/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()


class FaceRecognition:

    def faceDetect(self, Entry1):
        face_id = Entry1
        cam = cv2.VideoCapture(0)

        count = 0

        while (True):

            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                cv2.imwrite(BASE_DIR + '/apps/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg",
                            gray[y:y + h, x:x + w])

                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            elif count >= 30:
                break

        cam.release()
        cv2.destroyAllWindows()

    def trainFace(self):

        path = BASE_DIR + '/apps/dataset'

        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])
                print("face_id", face_id)
                faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(face_id)

            return faceSamples, ids

        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        recognizer.save(
            BASE_DIR + '/apps/trainer/trainer.yml')

        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    def recognizeFace(self):
        recognizer.read(BASE_DIR + '/apps/trainer/trainer.yml')

        faceCascade = cv2.CascadeClassifier(BASE_DIR + '/apps/haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)

        matched_face_id = None
        best_confidence = 999

        while True:
            ret, img = cam.read()

            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80),
            )

            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]

                face_id, confidence = recognizer.predict(face_roi)

                print("Predicted:", face_id, "Confidence:", confidence)

                if confidence < best_confidence:
                    best_confidence = confidence
                    matched_face_id = face_id

                if confidence < 45:
                    cam.release()
                    cv2.destroyAllWindows()
                    return face_id

            cv2.imshow('Detect Face', img)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()

        return None
