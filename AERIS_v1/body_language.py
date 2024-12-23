import pandas as pd
import pickle
import cv2
import mediapipe as mp
from queue import Queue
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


def emotion_detection(emotion_queue, chatbot_status):
    # print("Waiting for chatbot to start...")
    chatbot_status.wait() # wait until the chatbot is running
    print("emotion_detection function is running...")
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic 
    with open('../body_language_rf.pkl', mode='rb') as f:
        emotion_detection_model = pickle.load(f)

    cap = cv2.VideoCapture(0)
    if not emotion_queue.empty():
        emotion_context = emotion_queue.get()

    with mp_holistic.Holistic(min_detection_confidence = 0.5, 
                              min_tracking_confidence = 0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = holistic.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 1. Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                    mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                    mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                    )
            
            # 2. Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                    )

            # 3. Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                    )

            # 4. Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )
            
            try:
                # Extract Pose landmarks
                pose = results.pose_landmarks.landmark
                pose_row = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in pose]).flatten())
                
                # Extract Face landmarks
                face = results.face_landmarks.landmark
                face_row = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in face]).flatten())
                
                # Concate rows
                row = pose_row+face_row

                # Make Detections
                X = pd.DataFrame([row])
                body_language_class = emotion_detection_model.predict(X)[0]
                body_language_prob = emotion_detection_model.predict_proba(X)[0]
                #print(body_language_class, body_language_prob)
                emotion_context += body_language_class
                emotion_queue.put(emotion_context)
                
            except:
                print('excepting')
                pass

            cv2.imshow('Raw Webcam Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                emotion_queue.put('exit') # replacing all the previous contexts, only exit is left
                break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return body_language_class