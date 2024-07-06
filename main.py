import os
import time

import cv2
import numpy as np
import sys
import pygame
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from Board import *
from OpenCV import *

# Define model and folder paths
model_path = 'C:\\ASU\\ASU\\SEM 6\\AI\\Model\\model_v.22_1.000_0.003.h5'
folder_path = "C:/ASU/ASU/SEM 6/AI/IMG"



def predict_board_state(model_path, folder_path):

    model = load_model(model_path)
    board_state = np.empty((3, 3), dtype=int)
    imgCounter = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(folder_path, filename)
            
            img = load_img(image_path, target_size=(224, 224), color_mode='grayscale')
            img_array = img_to_array(img)
            img_array = img_array.reshape((1,) + img_array.shape)
            img_array = img_array / 255.0
            
            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction)
            i = imgCounter // 3
            j = imgCounter % 3
            board_state[i, j] = predicted_class
            print(f"Image {filename}: {predicted_class} at pos {i},{j}")

            imgCounter += 1
    print("board_state: ", board_state)
    return board_state

def detect_changes(old_state, new_state):
    return np.argwhere(old_state != new_state)





# def notMain():
#     game = Game()
#
#     old_state = np.zeros((3, 3), dtype=int)
#     print("old_state: ", old_state)
#     new_state = predict_board_state(model_path, folder_path)
#     print("new_state: ", new_state)
#     changes = detect_changes(old_state, new_state)
#     print("changes: ", changes)
#     game.update_board_state(new_state)
#     while True:
#         pygame.display.update()
#
#     old_state = new_state
    
def get_subdirectories(folder_path):
    return [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

def main():
    if len(sys.argv) != 2:
        print("Usage: python tictactoe.py [minimax | alpha-beta]")
        sys.exit(1)

    algorithm_choice = sys.argv[1].lower()

    if algorithm_choice not in ["minimax", "alpha-beta"]:
        print("Invalid algorithm choice. Use 'minimax' or 'alpha-beta'.")
        sys.exit(1)

    if algorithm_choice == "minimax":
        game = Game(1)

    else:  # alphabeta
        game = Game(2)

    board = game.board
    ai = game.ai
    ai.print_algorithm()
    # pygame.init()
    # game = Game()
    # board = game.board
    # ai = game.ai

    old_state = np.zeros((3, 3), dtype=int)


    while True:
        pygame.display.update()
        # subdirectories = get_subdirectories(folder_path)
        # for subfolder_path in subdirectories:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #timed Functions
        #getContours()

        cap = cv2.VideoCapture(1)
        cap.set(3, 640)
        cap.set(4, 480)
        while True :
            success, img = cap.read()
            if not success:
                print("Failed to capture frame")
                break
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 3)
            imgCanny = cv2.Canny(imgBlur, 50, 50)
            img_Copy = img.copy()
            getContours(imgCanny, img_Copy)
            cv2.imshow("Result", img_Copy)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



        new_state = predict_board_state(model_path, folder_path)
        changes = detect_changes(old_state, new_state)
        if changes.size > 0:
            if game.running:
                game.update_board_state(new_state)
                if game.isover():
                    game.running = False
                    break

        old_state = new_state

        if game.game_mode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)
            if board.empty_sqr(row, col):
                game.make_move(row, col)

            pygame.display.update()

            if game.isover():
                pygame.display.update()
                game.running = False
                break


        if not game.running:
            # cap.release()
            # cv2.destroyAllWindows()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
                time.sleep(0.1)


    time.sleep(5)







if __name__ == "__main__":
    main()
    print("Game Over!")




