import cv2
import numpy as np
import mediapipe as mp


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )

    window_name = "Screen Annotation Tracker"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    canvas = None
    prev_x, prev_y = None, None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        if canvas is None:
            canvas = np.zeros_like(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        draw_mode = False
        pause_mode = False
        clear_mode = False

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            lm = hand_landmarks.landmark
            index_tip = lm[8]
            index_dip = lm[7]
            middle_tip = lm[12]
            middle_dip = lm[11]
            ring_tip = lm[16]
            ring_dip = lm[15]
            thumb_tip = lm[4]
            thumb_ip = lm[3]

            index_up = index_tip.y < index_dip.y
            middle_up = middle_tip.y < middle_dip.y
            ring_up = ring_tip.y < ring_dip.y
            thumb_up = thumb_tip.x < thumb_ip.x if index_tip.x < thumb_tip.x else thumb_tip.x > thumb_ip.x

            x, y = int(index_tip.x * w), int(index_tip.y * h)

            if index_up and not middle_up:
                draw_mode = True
            elif index_up and middle_up and not ring_up:
                pause_mode = True
            elif index_up and middle_up and ring_up and thumb_up:
                clear_mode = True

            if clear_mode:
                canvas = np.zeros_like(frame)
                prev_x, prev_y = None, None
            elif draw_mode:
                if prev_x is None or prev_y is None:
                    prev_x, prev_y = x, y
                cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 255, 0), 6, cv2.LINE_AA)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.circle(frame, (x, y), 8, (0, 255, 255), cv2.FILLED)

        overlay = cv2.addWeighted(frame, 0.6, canvas, 0.4, 0)

        instructions = [
            "Index finger up: draw",
            "Index + middle finger up: pause",
            "All fingers up: clear",
            "Press Q or ESC to quit",
        ]
        for i, text in enumerate(instructions, start=1):
            cv2.putText(overlay, text, (20, 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        if draw_mode:
            status = "Drawing"
            color = (0, 255, 0)
        elif pause_mode:
            status = "Paused"
            color = (0, 255, 255)
        elif clear_mode:
            status = "Cleared"
            color = (0, 0, 255)
        else:
            status = "Show index finger to draw"
            color = (255, 255, 255)

        cv2.putText(overlay, f"Status: {status}", (20, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3, cv2.LINE_AA)

        cv2.imshow(window_name, overlay)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
