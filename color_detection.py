import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    colors = {

        "RED": [
            (np.array([0,120,70]), np.array([10,255,255])),
            (np.array([170,120,70]), np.array([180,255,255]))
        ],

        "GREEN": [
            (np.array([40,40,40]), np.array([80,255,255]))
        ],

        "BLUE": [
            (np.array([100,150,0]), np.array([140,255,255]))
        ]
    }

    for color_name, ranges in colors.items():

        mask = None

        for lower, upper in ranges:

            current = cv2.inRange(hsv, lower, upper)

            if mask is None:
                mask = current
            else:
                mask += current

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:

            area = cv2.contourArea(contour)

            if area > 1000:

                x, y, w, h = cv2.boundingRect(contour)

                if color_name == "RED":
                    color = (0,0,255)
                elif color_name == "GREEN":
                    color = (0,255,0)
                else:
                    color = (255,0,0)

                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)

                cv2.putText(frame,color_name,(x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,color,2)

    cv2.imshow("Color Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()