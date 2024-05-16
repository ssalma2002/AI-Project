import copy
import random
import sys
import time
import pygame
import numpy as np
from constants import *

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(bg_color)

# 2D ARRAY REPRESENTING THE BOARD
class Board:
    def __init__(self):
        self.squares = np.zeros((rows,cols))
        # TEST MARK_SQR
        # self.mark_sqr(1,1,2)
        # print(self.squares)
        self.empty_sqrs = copy.deepcopy(self.squares)
        self.marked_sqrs =0
    
    def final_state(self,show_win = False):
        # '''
        #     return 0 if there is no win yet
        #     return 1 if player 1 wins
        #     return 2 if player 2 wins
        # '''
        #vertical wins
        for col in range(cols):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col] !=0:
                if show_win:
                    color= circle_color if self.squares[0][col] ==2 else cross_color
                    initial_position = (col*sq_Size +sq_Size /2,20)
                    final_position = (col*sq_Size+ sq_Size/2,height-20)
                    pygame.draw.line(screen,color,initial_position,final_position,line_width)
                return self.squares[0][col]
        #horizontal wins
        for row in range(rows):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2] !=0:
                if show_win:
                    color= circle_color if self.squares[row][0] ==2 else cross_color
                    initial_position = (20,row*sq_Size+sq_Size/2)
                    final_position = (width-20,row*sq_Size+sq_Size/2)
                    pygame.draw.line(screen,color,initial_position,final_position,line_width)
                return self.squares[row][0]
        #desc win
        if self.squares[0][0]== self.squares[1][1]==self.squares[2][2]!=0:
            if show_win:
                    color= circle_color if self.squares[0][0] ==2 else cross_color
                    initial_position = (20,20)
                    final_position = (width-20,height-20)
                    pygame.draw.line(screen,color,initial_position,final_position,line_width)
            return self.squares[1][1]
        #asc win
        if self.squares[0][2]== self.squares[1][1]==self.squares[2][0]!=0:
            if show_win:
                    color= circle_color if self.squares[0][2] ==2 else cross_color
                    initial_position = (20,height-20)
                    final_position = (width-20,20)
                    pygame.draw.line(screen,color,initial_position,final_position,line_width)
                    
            return self.squares[1][1]
        #IF NOTHING RETURN 0
        return 0
    def get_empty_sqrs(self):
        empty_sqrs =[]
        for row in range(rows):
            for col in range (cols):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs # return row,col
    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0
    # MARK BY PLAYER
    def mark_sqr(self,row,col,player):
        self.squares[row][col]= player
        self.marked_sqrs = self.marked_sqrs + 1
    #IF SQUARE EMPTY RETURN
    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0

class AI:
    def __init__(self, level=1, player=2, algorithm = None):
        self.level = level
        self.player = player
        self.algorithm = algorithm
        self.node_count = 0


    def print_algorithm(self):
        if self.algorithm == 1:
            print("algo is Minimax")
        elif self.algorithm == 2:
            print("algo is Alpha-Beta")
        else:
            print("Invalid algorithm")


    
    def reset_node_count(self):
        self.node_count = 0


    def random_choice(self, board):
        empty_sqrs = board.get_empty_sqrs()
        if board.isfull():
            return
        else:
            idx = random.randrange(0, len(empty_sqrs))
            return empty_sqrs[idx]
        

        
    def minimax(self,board,maximizing):
        self.node_count += 1
        #terminal case 
        case = board.final_state()
        #player 1 wins
        if case == 1:
            return 1,None #eval, move
        elif case == 2:
            return -1,None
        elif board.isfull():
            return 0,None
        
        if maximizing:
            max_eval =-100
            best_move=None
            empty_sqrs = board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval = self.minimax(temp_board,False)[0]
                if eval >max_eval:
                    max_eval = eval
                    best_move =(row,col)
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                #copy so we dont affect the real board
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move =(row,col)
            return min_eval, best_move
    

    def alphabeta(self, board, alpha, beta, maximizing):
        self.node_count += 1
        case = board.final_state()
        if case == 1:
            return 1, None  
        elif case == 2:
            return -1, None  
        elif board.isfull():
            return 0, None  

        if maximizing:
            max_eval = -np.inf
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval, _ = self.alphabeta(temp_board, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = np.inf
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval, _ = self.alphabeta(temp_board, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.random_choice(main_board)
        elif self.algorithm == 1:
            start_time = time.perf_counter()
            self.reset_node_count()
            eval, move = self.minimax(main_board, False)
            exec_time = time.perf_counter() - start_time
        else:
            start_time = time.perf_counter()
            self.reset_node_count()
            eval, move = self.alphabeta(main_board, -np.inf, np.inf, False)
            exec_time = time.perf_counter() - start_time

        
        print(f'AI has chosen to mark the square in position {move} with an eval of {eval}')
        print(f'Nodes evaluated: {self.node_count}')
        print(f'Execution time: {exec_time:.4f} seconds')
        return move


class Game:

    def __init__(self, algorithm_choice):
        self.board=Board()
        self.ai = AI(algorithm=algorithm_choice)
        self.player =1
        self.game_mode ='ai'
        self.running = True
        self.show_lines()

    

    def show_lines(self):
        #vertical
        pygame.draw.line(screen,line_color,(sq_Size,0),(sq_Size,height),line_width)
        pygame.draw.line(screen,line_color,(width - sq_Size,0),(width - sq_Size,height),line_width)
        
        #horizontal
        pygame.draw.line(screen,line_color,(0,sq_Size),(width,sq_Size),line_width)
        pygame.draw.line(screen,line_color,(0,height - sq_Size),(width,height - sq_Size),line_width)
    #MATH EQUATION TO SWITCH BETWEEN PLAYER 1 AND PLAYER 2
    def next_turn(self):
        self.player = self.player %2 + 1
    
    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()
    
    def draw_fig(self,row,col):
        if self.player == 1 :
            #DRAW CROSS
            start_desc =(col* sq_Size +offset,row * sq_Size + offset)
            end_desc =(col*sq_Size + sq_Size - offset,row * sq_Size + sq_Size - offset)
            pygame.draw.line(screen,cross_color,start_desc,end_desc,cross_width)

            start_asc =(col* sq_Size +offset,row * sq_Size + sq_Size - offset)
            end_asc =(col*sq_Size + sq_Size - offset,row*sq_Size + offset)
            pygame.draw.line(screen,cross_color,start_asc,end_asc,cross_width)
        elif self.player ==2:
            center =(col*sq_Size +sq_Size /2,row*sq_Size+sq_Size/2)
            pygame.draw.circle(screen,circle_color,center,radius,circle_width)

    def isover(self):
        return (self.board.final_state(show_win=True) != 0) or (self.board.isfull())

    def update_board_state(self, predicted_state):
        for i in range(3):
            for j in range(3):
                if predicted_state[i][j] != self.board.squares[i][j]:
                    if self.board.empty_sqr(i, j):
                        self.make_move(i, j)
        print(f"predicted_states: {predicted_state}\nUpdated board state:{self.board.squares}\n")



        

