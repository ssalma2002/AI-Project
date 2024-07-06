import cv2
import numpy as np
import os
import os
import numpy as np
import matplotlib.pyplot as plt



save_path = "C:/ASU/ASU/SEM 6/AI/IMG"

def getContours(img, original_img):
    

    corners_dict = {}  # Dictionary to store corner coordinates with names
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for cnt in contours:
        if cv2.contourArea(cnt) > 0:  # Check if contour is valid
            area = cv2.contourArea(cnt)
            if area > 43000:
                cv2.drawContours(original_img, [cnt], -1, (0, 255, 0), 2)
                peri = cv2.arcLength(cnt, True)

                approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
                ax = approx.item(0)
                ay = approx.item(1)

                bx = approx.item(2)
                by = approx.item(3)

                cx = approx.item(4)
                cy = approx.item(5)

                dx = approx.item(6)
                dy = approx.item(7)

                width, height = 300, 300

                pts1 = np.float32([[bx, by], [ax, ay], [cx, cy], [dx, dy]])
                pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                img_prespective = cv2.warpPerspective(original_img, matrix, (width, height))
                img_corners = cv2.cvtColor(img_prespective, cv2.COLOR_BGR2GRAY)

                for x in range(0, 300):
                    for y in range(0, 300):
                        if img_corners[x][y] < 140:
                            img_corners[x][y] = 0
                        else:
                            img_corners[x][y] = 255
                


                cv2.imshow("Corners", img_corners)

                # Draw bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 0, 255), 2)


                for x in range(1, 4):
                    for y in range(1, 4):
                        img = img_corners[x * 100 - 100:x * 100, y * 100 - 100:y * 100]
                        filename = f"square_{x}_{y}.png"
                        cv2.imwrite(os.path.join(save_path, filename), img)

    return corners_dict

