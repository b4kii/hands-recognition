import cv2
import mediapipe as mp
import HandTrackingModule as htm

def tracker():
    CAM_W, CAM_H = 640, 480

    camera = cv2.VideoCapture(0)
    camera.set(3, CAM_W)
    camera.set(4, CAM_H)

    if not camera.isOpened():
        print("Cannot open camera!")
        exit()

    detector = htm.handDetector(detectionCon=0.75)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode = False,
                            model_complexity = 1,
                            min_detection_confidence = 0.75, 
                            min_tracking_confidence = 0.75,
                            max_num_hands = 2)

    while True:
        ret, frame = camera.read()

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        frame = detector.findHands(frame)

        finger_count = 0

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                handLabel = results.multi_handedness[handIndex].classification[0].label

                if len(results.multi_handedness) == 2:
                    cv2.putText(frame, "Both hands", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                else:
                    if handLabel == "Left":
                        cv2.putText(frame, f"{handLabel} Hand", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                    if handLabel == "Right":
                        cv2.putText(frame, f"{handLabel} Hand", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                handLandmarks = []

                for landmarks in hand_landmarks.landmark:
                    handLandmarks.append([landmarks.x, landmarks.y])

                if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                    finger_count = finger_count+1
                elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                    finger_count = finger_count+1

                if handLandmarks[8][1] < handLandmarks[6][1]:
                    finger_count = finger_count+1
                if handLandmarks[12][1] < handLandmarks[10][1]:
                    finger_count = finger_count+1
                if handLandmarks[16][1] < handLandmarks[14][1]:
                    finger_count = finger_count+1
                if handLandmarks[20][1] < handLandmarks[18][1]:
                    finger_count = finger_count+1

            cv2.putText(frame, f"{finger_count}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 1)

        cv2.putText(frame, "Press 'q' to quit!", (10, 460), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        cv2.imshow("Camera", frame)

        if not ret:
            print("Cannot receive frame!")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()