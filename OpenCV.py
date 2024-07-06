import cv2
import numpy as np
import os
import os
import numpy as np
import matplotlib.pyplot as plt
# from tensorflow.keras.models import load_model
# from keras.preprocessing.image import img_to_array, load_img


save_path = "C:/ASU/ASU/SEM 6/AI/IMG"
# folder_path = 'C:\ASU\ASU\SEM 6\AI\IMG'
# model_path = 'C:\ASU\ASU\SEM 6\AI\Model\model_v.22_1.000_0.003.h5'

# def predict_images_in_folder(model_path, folder_path):
#     model = load_model(model_path)
#     predictions_list = []
#
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
#             image_path = os.path.join(folder_path, filename)
#
#             img = load_img(image_path, target_size=(224, 224), color_mode='grayscale')
#             img_array = img_to_array(img)
#             img_array = img_array.reshape((1,) + img_array.shape)
#             img_array = img_array / 255.0
#
#             prediction = model.predict(img_array)
#             predicted_class = np.argmax(prediction)
#             predictions_list.append((filename, predicted_class))
#
#     print(len(predictions_list))
#     return predictions_list

# def reorder(myPoints):
#     myPoints = myPoints.reshape((-1, 2))
#     if len(myPoints) > 4:
#         myPoints = myPoints[:4]  # Take only the first four points
#     myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
#     add = myPoints.sum(1)
#     myPointsNew[0] = myPoints[np.argmin(add)]
#     myPointsNew[3] = myPoints[np.argmax(add)]
#     diff = np.diff(myPoints, axis=1)
#     myPointsNew[1] = myPoints[np.argmin(diff)]
#     myPointsNew[2] = myPoints[np.argmax(diff)]
#     return myPointsNew


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


# def capture_and_process_frame():
#     cap = cv2.VideoCapture(1)
#     cap.set(3, 640)
#     cap.set(4, 480)
#
#     # Define the time interval (in seconds) for capturing frames
#     capture_interval = 10
#     # Initialize a variable to keep track of the time
#     start_time = 0
#
#     while True:
#         # Capture current time
#         current_time = cv2.getTickCount()
#
#         # Calculate the time elapsed since the last frame capture
#         time_elapsed = (current_time - start_time) / cv2.getTickFrequency()
#
#         # Read a frame from the video capture
#         success, img = cap.read()
#         if not success:
#             print("Failed to capture frame")
#             break
#
#         imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 3)
#         imgCanny = cv2.Canny(imgBlur, 50, 50)
#         img_Copy = img.copy()
#
#         cv2.imshow("Result", img_Copy)
#
#         # Check if it's time to capture a frame
#         if time_elapsed >= capture_interval:
#             # Pass the current frame to getContours function
#             getContours(imgCanny, img_Copy)
#
#             predicted_classes = predict_images_in_folder(model_path, folder_path)
#
#
#             category = {0: 'Blank', 1: 'X', 2: 'O'}
#
#             for filename, predicted_class in predicted_classes:
#
#                 print(f"Image {filename}: {category[predicted_class]}")
#
#             # Update the start time for the next capture
#             start_time = current_time
#
#         # if cv2.waitKey(1) & 0xFF == ord('q'):
#         #     break
#
#     cap.release()
#     cv2.destroyAllWindows()


# Call the function to start capturing and processing frames
# capture_and_process_frame()
