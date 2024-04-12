import pygame
import sys
import valors # va for variables and lors for olors HAHAHAHAHAHA
from aiolors import get_ai_move

pygame.init()
current_phase = valors.MAIN_DISPLAY

# Set up the screen
screen = pygame.display.set_mode((valors.WIDTH, valors.HEIGHT))
pygame.display.set_caption("Six Men Morris")
icon = pygame.image.load(valors.game_icon1)
pygame.display.set_icon(icon)
font = pygame.font.Font(None, 36)

def mainDisplay(mouse_x, mouse_y):
    background_image = pygame.image.load(valors.main_cover)
    background_image = pygame.transform.scale(background_image, (valors.WIDTH, valors.HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define the coordinates and dimensions of the button
    button_width = 300
    button_height = 40
    button_x = (valors.WIDTH - button_width) // 2
    button_y = 510
    
    pygame.draw.rect(screen, (0, 0, 0), (button_x, button_y, button_width, button_height), 2)

    # Check if the mouse click is within the button area
    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        return valors.CHOOSE_COLOR_CHAR

    return valors.MAIN_DISPLAY

def chooseColor(mouse_x, mouse_y):
    background_image = pygame.image.load(valors.choose_color)
    background_image = pygame.transform.scale(background_image, (valors.WIDTH, valors.HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define button dimensions
    button_width = 300
    button_height = 400
    white_button_x = 600
    black_button_x = 100
    button_y = 125

    start_button_width = 300
    start_button_height = 40
    start_button_x = (valors.WIDTH - start_button_width) // 2
    start_button_y = 530

    # Draw white and black pieces as buttons
    white_piece = pygame.image.load(valors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (button_width, button_height))
    black_piece = pygame.image.load(valors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (button_width, button_height))

    # draw a rect_point for start button as red
    pygame.draw.rect(screen, (255, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)

    # Check if mouse is over the white piece button
    if white_button_x <= mouse_x <= white_button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        # if white piece is already clicked and then clicked again
        if valors.white_piece_clicked:
            valors.white_piece_clicked = False

        # if black piece is selected, change the current selected piece to white
        elif valors.black_piece_clicked: 
            valors.black_piece_clicked = False
            valors.white_piece_clicked = True

        else:
            valors.white_piece_clicked = True

    # Check if mouse is over the black piece button
    if black_button_x <= mouse_x <= black_button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        # if black piece is already clicked and then clicked again
        if valors.black_piece_clicked:
            valors.black_piece_clicked = False

        # if white piece is selected, change the current selected piece to black
        elif valors.white_piece_clicked: 
            valors.white_piece_clicked = False
            valors.black_piece_clicked = True

        else:
            valors.black_piece_clicked = True
        
    # transform the pieces
    if valors.white_piece_clicked:
        screen.blit(pygame.transform.scale(white_piece, (button_width + 40, button_height + 40)), (white_button_x - 10, button_y - 10))
    elif not valors.white_piece_clicked:
        screen.blit(white_piece, (white_button_x, button_y))

    if valors.black_piece_clicked:
        screen.blit(pygame.transform.scale(black_piece, (button_width + 40, button_height + 40)), (black_button_x - 10, button_y - 10))
    elif not valors.black_piece_clicked:
        screen.blit(black_piece, (black_button_x, button_y))

    # check if there is selected piece
    if valors.white_piece_clicked or valors.black_piece_clicked:
        # draw a rect_point for start button as green
        pygame.draw.rect(screen, (0, 255, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)
        if start_button_x <= mouse_x <= start_button_x + start_button_width and start_button_y <= mouse_y <= start_button_y + start_button_height:
            if valors.white_piece_clicked:
                valors.player_user = valors.player_one
                return valors.GAMEPLAY_PHASE, valors.player_one
            elif valors.black_piece_clicked:
                valors.player_user = valors.player_two
                return valors.GAMEPLAY_PHASE, valors.player_two
    else:
        # draw a rect_point for start button as red
        pygame.draw.rect(screen, (255, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)
    return valors.CHOOSE_COLOR_CHAR, 0

def startGame(mouse_x, mouse_y, curr_player, current_phase):
    drawBoard(current_phase, curr_player)
    drawCurrentBoard()
    drawPieces()
    
    if valors.player_pieces_onhold[curr_player] > 0:
        if curr_player == valors.player_user:
            available_moves = checkAvailableMoves()
            drawAvailableMoves()

            for point in valors.intersection_points:
                distance = ((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2) ** 0.5
                if distance <= valors.POINT_RADIUS:
                    if point in available_moves:
                        drawBoard(current_phase, curr_player)
                        drawCurrentBoard()
                        placePieceOnBoard(curr_player, point)
                        drawPieces()

                        # check if curr_player place a 3 consecutive pieces
                        if isConsecutivePoints(curr_player):
                            
                            if isPiecesAlreadyMills(curr_player):
                                valors.piece_clicked = (0, 0)
                                valors.prev_piece_clicked = (0, 0)
                                valors.curr_piece_clicked = False
                                return valors.GAMEPLAY_REMOVE_PIECE, curr_player
                        else:
                            valors.player_pieces_mills[curr_player] = []
                            valors.player_pieces_prev_mills[curr_player] = []
                                

                        # check if curr_player already won
                        winner = isCurrentPlayerWon(curr_player)
                        if winner != 0:
                            if winner == valors.player_user:
                                return valors.GAMEPLAY_PLAYER_WON, winner
                            else:
                                return valors.GAMEPLAY_PLAYER_LOSE, curr_player
                        
                        # check if the game is draw
                        if isGameDraw(curr_player):
                            return valors.GAMEPLAY_PLAYER_DRAW, curr_player
                        
                        # change current player
                        curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                        drawBoard(current_phase, curr_player)
                        drawCurrentBoard()
                        drawPieces()
                        drawAvailableMoves()

                        if valors.player_pieces_onhold[valors.player_one] > 0 or valors.player_pieces_onhold[valors.player_two] > 0:
                            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                            return valors.GAMEPLAY_PHASE, curr_player
                        else:
                            displayFeedback("SECOND PHASE.", (650, 185))
                            pygame.time.wait(1000)
                            drawBoard(valors.secondPhase_currPhase, curr_player)
                            drawCurrentBoard()
                            return valors.GAMEPLAY_SECOND_PHASE, curr_player
                    else:
                        print(f"[Error] Invalid Move. point: {point}")
                        displayFeedback("POINT IS ALREADY OCCUPIED.", (600, 185))
                        pygame.time.wait(1000)
                        drawBoard(current_phase, curr_player)
                        drawCurrentBoard()
                        drawPieces()
                        drawAvailableMoves()
                        return valors.GAMEPLAY_PHASE, curr_player
        else:
            # get ai move 
            # get a point from ai
            # placePieceOnBoard(curr_player, point)

            return_value = get_ai_move(valors.GAMEPLAY_PHASE, curr_player)
            placePieceOnBoard(curr_player, return_value)
            drawPieces()

            # check if curr_player place a 3 consecutive pieces
            if isConsecutivePoints(curr_player):
                
                if isPiecesAlreadyMills(curr_player):
                    valors.piece_clicked = (0, 0)
                    valors.prev_piece_clicked = (0, 0)
                    valors.curr_piece_clicked = False
                    return valors.GAMEPLAY_REMOVE_PIECE, curr_player
            else:
                valors.player_pieces_mills[curr_player] = []
                valors.player_pieces_prev_mills[curr_player] = []
                    

            # check if curr_player already won
            winner = isCurrentPlayerWon(curr_player)
            if winner != 0:
                if winner == valors.player_user:
                    return valors.GAMEPLAY_PLAYER_WON, winner
                else:
                    return valors.GAMEPLAY_PLAYER_LOSE, curr_player
            
            # check if the game is draw
            if isGameDraw(curr_player):
                return valors.GAMEPLAY_PLAYER_DRAW, curr_player
            
            # change current player
            curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
            drawBoard(current_phase, curr_player)
            drawCurrentBoard()
            drawPieces()
            drawAvailableMoves()

            if valors.player_pieces_onhold[valors.player_one] > 0 or valors.player_pieces_onhold[valors.player_two] > 0:
                return valors.GAMEPLAY_PHASE, curr_player
            else:
                displayFeedback("SECOND PHASE.", (650, 185))
                pygame.time.wait(1000)
                drawBoard(valors.secondPhase_currPhase, curr_player)
                drawCurrentBoard()
                return valors.GAMEPLAY_SECOND_PHASE, curr_player

        return valors.GAMEPLAY_PHASE, curr_player
    else:
        displayFeedback("SECOND PHASE.", (650, 185))
        pygame.time.wait(1000)
        drawBoard(valors.secondPhase_currPhase, curr_player)
        drawCurrentBoard()
        return valors.GAMEPLAY_SECOND_PHASE, curr_player

def secondPhaseGame(mouse_x, mouse_y, curr_player):
    drawBoard(valors.secondPhase_currPhase, curr_player)
    drawPieces()

    print()
    print("------------- SECOND PHASE -------------")
    print()

    if curr_player == valors.player_one:
        opponent_player = valors.player_two
    elif curr_player == valors.player_two:
        opponent_player = valors.player_one
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")
    
    print(f"len(valors.player_pieces_onboard[curr_player]): {len(valors.player_pieces_onboard[curr_player])}")
    print(f"len(valors.player_pieces_onboard[opponent_player]): {len(valors.player_pieces_onboard[opponent_player])}")
          

    if len(valors.player_pieces_onboard[curr_player]) == 3 and len(valors.player_pieces_onboard[opponent_player]) == 3:
        displayFeedback("FINAL PHASE.", (650, 185))
        pygame.time.wait(1000)
        drawBoard(valors.secondPhase_currPhase, curr_player)
        drawCurrentBoard()
        drawAvailableMoves()
        return valors.GAMEPLAY_FINAL_PHASE, curr_player
    
    else:
        if curr_player == valors.player_user:
            curr_player_pieces = set(valors.player_pieces_onboard[curr_player])
            for piece in curr_player_pieces:
                piece_distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
                if piece_distance <= valors.POINT_RADIUS:
                    valors.piece_clicked = piece

                    # if piece is already clicked
                    if valors.prev_piece_clicked == valors.piece_clicked:
                        valors.prev_piece_clicked = (0, 0)
                        valors.curr_piece_clicked = False
                    
                    # if piece is clicked then click another piece
                    elif valors.curr_piece_clicked and valors.prev_piece_clicked != valors.piece_clicked:
                        valors.prev_piece_clicked = valors.piece_clicked
                        valors.curr_piece_clicked = True
                    
                    else:
                        valors.prev_piece_clicked = valors.piece_clicked
                        valors.curr_piece_clicked = True

            if not valors.curr_piece_clicked:
                valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
                drawBoard(valors.secondPhase_currPhase, curr_player)    
                drawCurrentBoard()

            if valors.curr_piece_clicked:
                curr_player_valid_moves = checkPieceValidMoves(valors.piece_clicked, curr_player, opponent_player)
                if curr_player_valid_moves:
                    valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_VALID_POINT
                    drawBoard(valors.secondPhase_currPhase, curr_player)

                    # make green point to the valid moves of the piece
                    for point in curr_player_valid_moves:
                        pygame.draw.circle(screen, valors.GREEN, point, 15, width=5) 

                    for curr_player_move in curr_player_valid_moves:
                        player_move_distance = ((mouse_x - curr_player_move[0]) ** 2 + (mouse_y - curr_player_move[1]) ** 2) ** 0.5
                        if player_move_distance <= valors.POINT_RADIUS:
                            # replace the piece's coord to valid point
                            valors.player_pieces_onboard[curr_player][valors.player_pieces_onboard[curr_player].index(valors.piece_clicked)] = curr_player_move
                            drawBoard(valors.secondPhase_currPhase, curr_player)
                            drawCurrentBoard()

                            # check if curr_player place a 3 consecutive pieces
                            if isConsecutivePoints(curr_player):
                                # store the 3 pieces so that if next move 
                                # that 3 pieces are not valid as a mill
                                # unless it moved

                                if isPiecesAlreadyMills(curr_player):
                                    valors.piece_clicked = (0, 0)
                                    valors.prev_piece_clicked = (0, 0)
                                    valors.curr_piece_clicked = False
                                    return valors.GAMEPLAY_REMOVE_PIECE, curr_player
                            else:
                                valors.player_pieces_mills[curr_player] = []
                                valors.player_pieces_prev_mills[curr_player] = []

                            # check if curr_player already won
                            winner = isCurrentPlayerWon(curr_player)
                            if winner != 0:
                                if winner == valors.player_user:
                                    return valors.GAMEPLAY_PLAYER_WON, winner
                                else:
                                    return valors.GAMEPLAY_PLAYER_LOSE, curr_player
                            
                            # check if the game is draw
                            if isGameDraw(curr_player):
                                return valors.GAMEPLAY_PLAYER_DRAW, curr_player
                            
                            print(f"--->len(valors.player_pieces_onboard[curr_player]): {len(valors.player_pieces_onboard[curr_player])}")
                            print(f"--->len(valors.player_pieces_onboard[opponent_player]): {len(valors.player_pieces_onboard[opponent_player])}")
        
                            if len(valors.player_pieces_onboard[curr_player]) == 3 and len(valors.player_pieces_onboard[opponent_player]) == 3:
                                displayFeedback("FINAL PHASE.", (650, 185))
                                pygame.time.wait(1000)  

                                # change current player
                                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                                curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                                valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
                                valors.piece_clicked = (0, 0)
                                valors.prev_piece_clicked = (0, 0)
                                valors.curr_piece_clicked = False

                                drawBoard(valors.secondPhase_currPhase, curr_player)
                                drawCurrentBoard()
                                return valors.GAMEPLAY_FINAL_PHASE, curr_player
                            else:
                                # change current player
                                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                                curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                                valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
                                valors.piece_clicked = (0, 0)
                                valors.prev_piece_clicked = (0, 0)
                                valors.curr_piece_clicked = False
                                
                                drawBoard(valors.secondPhase_currPhase, curr_player)
                                drawCurrentBoard()
                                return valors.GAMEPLAY_SECOND_PHASE, curr_player
                else:
                    valors.secondPhase_currPhase = valors.GAMEPLAY_NO_VALID_MOVES
                    drawBoard(valors.secondPhase_currPhase, curr_player)
        else:
            return_piece, return_move = get_ai_move(valors.GAMEPLAY_SECOND_PHASE, curr_player)
            valors.player_pieces_onboard[curr_player][valors.player_pieces_onboard[curr_player].index(return_piece)] = return_move
            drawBoard(valors.secondPhase_currPhase, curr_player)
            drawCurrentBoard()

            # check if curr_player place a 3 consecutive pieces
            if isConsecutivePoints(curr_player):
                # store the 3 pieces so that if next move 
                # that 3 pieces are not valid as a mill
                # unless it moved

                if isPiecesAlreadyMills(curr_player):
                    valors.piece_clicked = (0, 0)
                    valors.prev_piece_clicked = (0, 0)
                    valors.curr_piece_clicked = False
                    return valors.GAMEPLAY_REMOVE_PIECE, curr_player
            else:
                valors.player_pieces_mills[curr_player] = []
                valors.player_pieces_prev_mills[curr_player] = []

            # check if curr_player already won
            winner = isCurrentPlayerWon(curr_player)
            if winner != 0:
                if winner == valors.player_user:
                    return valors.GAMEPLAY_PLAYER_WON, winner
                else:
                    return valors.GAMEPLAY_PLAYER_LOSE, curr_player
            
            # check if the game is draw
            if isGameDraw(curr_player):
                return valors.GAMEPLAY_PLAYER_DRAW, curr_player
            
            print(f"--->len(valors.player_pieces_onboard[curr_player]): {len(valors.player_pieces_onboard[curr_player])}")
            print(f"--->len(valors.player_pieces_onboard[opponent_player]): {len(valors.player_pieces_onboard[opponent_player])}")

            if len(valors.player_pieces_onboard[curr_player]) == 3 and len(valors.player_pieces_onboard[opponent_player]) == 3:
                displayFeedback("FINAL PHASE.", (650, 185))
                pygame.time.wait(1000)  

                # change current player
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
                valors.piece_clicked = (0, 0)
                valors.prev_piece_clicked = (0, 0)
                valors.curr_piece_clicked = False

                drawBoard(valors.secondPhase_currPhase, curr_player)
                drawCurrentBoard()
                return valors.GAMEPLAY_FINAL_PHASE, curr_player
            else:
                # change current player
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
                valors.piece_clicked = (0, 0)
                valors.prev_piece_clicked = (0, 0)
                valors.curr_piece_clicked = False
                
                drawBoard(valors.secondPhase_currPhase, curr_player)
                drawCurrentBoard()
                return valors.GAMEPLAY_SECOND_PHASE, curr_player

        drawCurrentBoard()
        return valors.GAMEPLAY_SECOND_PHASE, curr_player
        
    
def finalPhaseGame(mouse_x, mouse_y, curr_player):
    drawBoard(valors.secondPhase_currPhase, curr_player)
    drawPieces()

    print()
    print("------------- FINAL PHASE -------------")
    print()

    if curr_player == valors.player_one:
        opponent_player = valors.player_two
    elif curr_player == valors.player_two:
        opponent_player = valors.player_one
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

    if curr_player == valors.player_user:
        curr_player_pieces = set(valors.player_pieces_onboard[curr_player])
        for piece in curr_player_pieces:
            piece_distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
            if piece_distance <= valors.POINT_RADIUS:
                valors.piece_clicked = piece

                # if piece is already clicked
                if valors.prev_piece_clicked == valors.piece_clicked:
                    valors.prev_piece_clicked = (0, 0)
                    valors.curr_piece_clicked = False
                
                # if piece is clicked then click another piece
                elif valors.curr_piece_clicked and valors.prev_piece_clicked != valors.piece_clicked:
                    valors.prev_piece_clicked = valors.piece_clicked
                    valors.curr_piece_clicked = True
                
                else:
                    valors.prev_piece_clicked = valors.piece_clicked
                    valors.curr_piece_clicked = True

        if not valors.curr_piece_clicked:
            valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
            drawBoard(valors.secondPhase_currPhase, curr_player)    
            drawCurrentBoard()

        if valors.curr_piece_clicked:
            curr_player_valid_moves = checkAvailableMoves()
            if curr_player_valid_moves:
                valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_VALID_POINT
                drawBoard(valors.secondPhase_currPhase, curr_player)

                # make green point to the valid moves of the piece
                for point in curr_player_valid_moves:
                    pygame.draw.circle(screen, valors.GREEN, point, 15, width=5) 

                for curr_player_move in curr_player_valid_moves:
                    player_move_distance = ((mouse_x - curr_player_move[0]) ** 2 + (mouse_y - curr_player_move[1]) ** 2) ** 0.5
                    if player_move_distance <= valors.POINT_RADIUS:
                        # replace the piece's coord to valid point
                        valors.player_pieces_onboard[curr_player][valors.player_pieces_onboard[curr_player].index(valors.piece_clicked)] = curr_player_move
                        drawBoard(valors.secondPhase_currPhase, curr_player)
                        drawCurrentBoard()

                        # check if curr_player place a 3 consecutive pieces
                        if isConsecutivePoints(curr_player):
                            # store the 3 pieces so that if next move 
                            # that 3 pieces are not valid as a mill
                            # unless it moved
                            
                            if isPiecesAlreadyMills(curr_player):
                                valors.piece_clicked = (0, 0)
                                valors.prev_piece_clicked = (0, 0)
                                valors.curr_piece_clicked = False
                                return valors.GAMEPLAY_REMOVE_PIECE, curr_player
                        else:
                            valors.player_pieces_mills[curr_player] = []
                            valors.player_pieces_prev_mills[curr_player] = []

                        # check if curr_player already won
                        winner = isCurrentPlayerWon(curr_player)
                        if winner != 0:
                            if winner == valors.player_user:
                                return valors.GAMEPLAY_PLAYER_WON, winner
                            else:
                                return valors.GAMEPLAY_PLAYER_LOSE, curr_player
                        
                        # check if the game is draw
                        if isGameDraw(curr_player):
                            return valors.GAMEPLAY_PLAYER_DRAW, curr_player
                        
                        # change current player
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                        curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                        valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
                        valors.piece_clicked = (0, 0)
                        valors.prev_piece_clicked = (0, 0)
                        valors.curr_piece_clicked = False
                        drawBoard(valors.secondPhase_currPhase, curr_player)
                        drawCurrentBoard()
                        return valors.GAMEPLAY_FINAL_PHASE, curr_player
            else:
                valors.secondPhase_currPhase = valors.GAMEPLAY_NO_VALID_MOVES
                drawBoard(valors.secondPhase_currPhase, curr_player)
    else:
        # get ai move
        # the flow is 
        #   get a piece from the board then choose which point it will go
        # valors.player_pieces_onboard[curr_player][valors.player_pieces_onboard[curr_player].index(valors.piece_clicked)] = curr_player_move

        return_piece, return_move = get_ai_move(valors.GAMEPLAY_FINAL_PHASE, curr_player)
        valors.player_pieces_onboard[curr_player][valors.player_pieces_onboard[curr_player].index(return_piece)] = return_move
        drawBoard(valors.secondPhase_currPhase, curr_player)
        drawCurrentBoard()

        # check if curr_player place a 3 consecutive pieces
        if isConsecutivePoints(curr_player):
            # store the 3 pieces so that if next move 
            # that 3 pieces are not valid as a mill
            # unless it moved
            
            if isPiecesAlreadyMills(curr_player):
                valors.piece_clicked = (0, 0)
                valors.prev_piece_clicked = (0, 0)
                valors.curr_piece_clicked = False
                return valors.GAMEPLAY_REMOVE_PIECE, curr_player
        else:
            valors.player_pieces_mills[curr_player] = []
            valors.player_pieces_prev_mills[curr_player] = []

        # check if curr_player already won
        winner = isCurrentPlayerWon(curr_player)
        if winner != 0:
            if winner == valors.player_user:
                return valors.GAMEPLAY_PLAYER_WON, winner
            else:
                return valors.GAMEPLAY_PLAYER_LOSE, curr_player
        
        # check if the game is draw
        if isGameDraw(curr_player):
            return valors.GAMEPLAY_PLAYER_DRAW, curr_player
        
        # change current player
        curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
        valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE
        valors.piece_clicked = (0, 0)
        valors.prev_piece_clicked = (0, 0)
        valors.curr_piece_clicked = False
        drawBoard(valors.secondPhase_currPhase, curr_player)
        drawCurrentBoard()
        return valors.GAMEPLAY_FINAL_PHASE, curr_player
        
    drawCurrentBoard()
    return valors.GAMEPLAY_FINAL_PHASE, curr_player

def drawBoard(curr_phase, curr_user):
    if curr_phase == valors.GAMEPLAY_PHASE and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg3_yourTurn)
    elif curr_phase == valors.GAMEPLAY_SECOND_PHASE and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg5_yourTurn2)
    elif curr_phase == valors.GAMEPLAY_SELECT_PIECE_TO_MOVE and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg5_yourTurn2)
    elif curr_phase == valors.GAMEPLAY_SELECT_VALID_POINT and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg5_yourTurn2B)
    elif curr_phase == valors.GAMEPLAY_NO_VALID_MOVES and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg5_yourTurn2C)
    elif curr_phase == valors.GAMEPLAY_REMOVE_PIECE and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg6_got3piece)
    elif curr_phase == valors.GAMEPLAY_PLAYER_WON and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg7_youWon)
    elif curr_phase == valors.GAMEPLAY_PLAYER_LOSE and curr_user == valors.player_user:
        background_image = pygame.image.load(valors.game_bg8_youLose)
    elif curr_phase == valors.GAMEPLAY_PLAYER_LOSE and curr_user != valors.player_user:
        background_image = pygame.image.load(valors.game_bg8_youLose)
    elif curr_phase == valors.GAMEPLAY_PLAYER_DRAW:
        background_image = pygame.image.load(valors.game_bg9_draw)
    elif curr_user != valors.player_user:
        background_image = pygame.image.load(valors.game_bg4_opponentTurn)
    else:
        background_image = pygame.image.load(valors.game_bg)
        print(f"[Error] Invalid curr_phase: {curr_phase} or curr_user: {curr_user}")

    background_image = pygame.transform.scale(background_image, (valors.WIDTH, valors.HEIGHT))
    screen.blit(background_image, (0, 0))
    
    # Outer square
    pygame.draw.line(screen, valors.BLACK, (50, 50), (550, 50), valors.LINE_WIDTH) # upper ---
    pygame.draw.line(screen, valors.BLACK, (50, 50), (50, 550), valors.LINE_WIDTH) # left |
    pygame.draw.line(screen, valors.BLACK, (550, 50), (550, 550), valors.LINE_WIDTH) # right |
    pygame.draw.line(screen, valors.BLACK, (50, 550), (550, 550), valors.LINE_WIDTH) # lower ---

    # edges connecting the outer and inner squares
    pygame.draw.line(screen, valors.BLACK, (300, 50), (300, 175), valors.LINE_WIDTH) # upper |
    pygame.draw.line(screen, valors.BLACK, (50, 300), (175, 300), valors.LINE_WIDTH) # left ---
    pygame.draw.line(screen, valors.BLACK, (425, 300), (550, 300), valors.LINE_WIDTH) # right ---
    pygame.draw.line(screen, valors.BLACK, (300, 425), (300, 550), valors.LINE_WIDTH) # lower |
    
    # Inner square
    pygame.draw.line(screen, valors.BLACK, (175, 175), (425, 175), valors.LINE_WIDTH) # upper ---
    pygame.draw.line(screen, valors.BLACK, (175, 175), (175, 425), valors.LINE_WIDTH) # left |
    pygame.draw.line(screen, valors.BLACK, (425, 175), (425, 425), valors.LINE_WIDTH) # right |
    pygame.draw.line(screen, valors.BLACK, (175, 425), (425, 425), valors.LINE_WIDTH) # lower ---
    
    # Draw little circles at each intersection point
    for point in valors.intersection_points:
        pygame.draw.circle(screen, valors.BLACK, point, 10) 

def drawPieces():
    # pieces dimensions
    piece_width = 100
    piece_height = 100
    piece_x = 600
    white_piece_y = 50
    black_piece_y = valors.HEIGHT - 150

    white_piece = pygame.image.load(valors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(valors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))

    # Draw white pieces
    for i in range(valors.player_pieces_onhold[valors.player_one]):
        screen.blit(white_piece, (piece_x + i * 50, white_piece_y))

    # Draw black pieces
    for i in range(valors.player_pieces_onhold[valors.player_two]):
        screen.blit(black_piece, (piece_x + i * 50, black_piece_y))

def drawCurrentBoard():
    # pieces dimensions
    piece_width = 100
    piece_height = 100
    clicked_piece_width = 120
    clicked_piece_height = 120

    white_piece = pygame.image.load(valors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(valors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))

    for point in valors.player_pieces_onboard[valors.player_one]:
        if point == valors.prev_piece_clicked:
            screen.blit(
                pygame.transform.scale(white_piece, (clicked_piece_width, clicked_piece_height)), 
                (point[0] - white_piece.get_width() // 2, point[1] - white_piece.get_height() // 2)
            )
        else:
            screen.blit(white_piece, (point[0] - white_piece.get_width() // 2, point[1] - white_piece.get_height() // 2))
    
    for point in valors.player_pieces_onboard[valors.player_two]:
        if point == valors.prev_piece_clicked:
            screen.blit(
                pygame.transform.scale(black_piece, (clicked_piece_width, clicked_piece_height)), 
                (point[0] - black_piece.get_width() // 2, point[1] - black_piece.get_height() // 2)
            )
        else:
            screen.blit(black_piece, (point[0] - black_piece.get_width() // 2, point[1] - black_piece.get_height() // 2))

# first phase
def checkAvailableMoves():
    inter_points = set(valors.intersection_points)
    points_occupied = set(valors.player_pieces_onboard[valors.player_one] + valors.player_pieces_onboard[valors.player_two])
    available_moves = inter_points - points_occupied
    return available_moves

def drawAvailableMoves():
    available_moves = checkAvailableMoves()
    for vpoint in available_moves:
        pygame.draw.circle(screen, valors.GREEN, vpoint, 15, width=5) 

# second phase
def checkAvailableMovesSecondPhase(curr_player, opponent_player):
    curr_player_pieces = set(valors.player_pieces_onboard[curr_player])
    opponent_player_pieces = set(valors.player_pieces_onboard[opponent_player])

    curr_player_moves = set()
    opponent_player_moves = set()

    for piece in curr_player_pieces:
        curr_player_moves.update(valors.point_moves[piece])

    for piece in opponent_player_pieces:
        opponent_player_moves.update(valors.point_moves[piece])

    curr_player_valid_moves = curr_player_moves - (opponent_player_pieces | curr_player_pieces)

    return curr_player_valid_moves

def checkPieceValidMoves(piece_clicked, curr_player, opponent_player):
    curr_player_pieces = set(valors.player_pieces_onboard[curr_player])
    opponent_player_pieces = set(valors.player_pieces_onboard[opponent_player])
    clicked_piece_moves = set(valors.point_moves[piece_clicked])

    clicked_piece_valid_moves = clicked_piece_moves - (curr_player_pieces | opponent_player_pieces)
    return clicked_piece_valid_moves

def placePieceOnBoard(curr_player, point):
    # pieces dimensions
    piece_width = 100
    piece_height = 100

    white_piece = pygame.image.load(valors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(valors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))
    
    if curr_player == valors.player_one:
        screen.blit(white_piece, (point[0] - white_piece.get_width() // 2, point[1] - white_piece.get_height() // 2))
        valors.player_pieces_onboard[curr_player].append(point)
        valors.player_pieces_onhold[curr_player] -= 1
    elif curr_player == valors.player_two:
        screen.blit(black_piece, (point[0] - black_piece.get_width() // 2, point[1] - black_piece.get_height() // 2))
        valors.player_pieces_onboard[curr_player].append(point)
        valors.player_pieces_onhold[curr_player] -= 1
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

def isConsecutivePoints(curr_player):
    return_value = False
    valors.player_pieces_mills[curr_player] = []

    for group in valors.consecutive_points:
        count = 0
        for point in group:
            if point in valors.player_pieces_onboard[curr_player]:
                count += 1
                if count == 3:
                    for gpoint in group:
                        valors.player_pieces_mills[curr_player].append(gpoint)
                    count = 0
                    return_value = True
            else:
                count = 0
    return return_value

def isPiecesAlreadyMills(curr_player):
    print(f"player_pieces_mills: {valors.player_pieces_mills[curr_player]}")
    print(f"player_pieces_prev_mills: {valors.player_pieces_prev_mills[curr_player]}")
    # if valors.player_pieces_mills[curr_player] == valors.player_pieces_prev_mills[curr_player] or valors.player_pieces_mills[curr_player] in valors.player_pieces_prev_mills[curr_player]:
    #     return False
    # else:
    #     valors.player_pieces_prev_mills[curr_player] = valors.player_pieces_mills[curr_player]
    #     return True
    current_mills = set(valors.player_pieces_mills[curr_player])
    previous_mills = set(valors.player_pieces_prev_mills[curr_player])

    # Check if current mills are either equal to or a subset of previous mills
    if current_mills == previous_mills or current_mills.issubset(previous_mills):
        valors.player_pieces_prev_mills[curr_player] = valors.player_pieces_mills[curr_player]
        return False
    else:
        valors.player_pieces_prev_mills[curr_player] = valors.player_pieces_mills[curr_player]
        return True


def removeOpponentPiece(mouse_x, mouse_y, curr_player, current_phase):
    drawBoard(current_phase, curr_player)
    drawCurrentBoard()
    drawPieces()

    if curr_player == valors.player_one:
        opponent_player = valors.player_two
        opponent_piece = set(valors.player_pieces_onboard[valors.player_two])
        opponent_piece_mills = set(valors.player_pieces_prev_mills[valors.player_two])
        valid_pieces_toRemove = opponent_piece - opponent_piece_mills
        
    elif curr_player == valors.player_two:
        opponent_player = valors.player_one
        opponent_piece = set(valors.player_pieces_onboard[valors.player_one])
        opponent_piece_mills = set(valors.player_pieces_prev_mills[valors.player_one])
        valid_pieces_toRemove = opponent_piece - opponent_piece_mills

    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

    if curr_player == valors.player_user:
        # make green point to the valid moves of the piece
        for vpoint in valid_pieces_toRemove:
            pygame.draw.circle(screen, valors.GREEN, vpoint, 20, width=5) 

        for piece in valid_pieces_toRemove:
            distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
            if distance <= valors.POINT_RADIUS:
                if piece in valid_pieces_toRemove:
                    valors.player_pieces_onboard[opponent_player].remove(piece)
                    
                    # check if curr_player already won
                    winner = isCurrentPlayerWon(curr_player)
                    if winner != 0:
                        if winner == valors.player_user:
                            return valors.GAMEPLAY_PLAYER_WON, curr_player
                        else:
                            return valors.GAMEPLAY_PLAYER_LOSE, curr_player
                    
                    if valors.player_pieces_onhold[curr_player] > 0:
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                        curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                        drawBoard(valors.GAMEPLAY_PHASE, curr_player)
                        drawCurrentBoard()
                        drawPieces()
                        drawAvailableMoves()
                        return valors.GAMEPLAY_PHASE, curr_player
                    elif len(valors.player_pieces_onboard[curr_player]) == 3 and len(valors.player_pieces_onboard[opponent_player]) == 3:
                        if not valors.isFinal_phase:
                            displayFeedback("FINAL PHASE.", (650, 185))
                            pygame.time.wait(1000)
                            valors.isFinal_phase = True
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                        curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                        drawBoard(valors.GAMEPLAY_SECOND_PHASE, curr_player)
                        drawCurrentBoard()
                        return valors.GAMEPLAY_FINAL_PHASE, curr_player
                    else:
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                        curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
                        drawBoard(valors.GAMEPLAY_SECOND_PHASE, curr_player)
                        drawCurrentBoard()
                        return valors.GAMEPLAY_SECOND_PHASE, curr_player
                else:
                    displayFeedback("CANNOT REMOVE OPPONENT'S MILL", (600, 185))
                    pygame.time.wait(1000)
                    drawBoard(current_phase, curr_player)
                    drawCurrentBoard()
                    drawPieces()
    else:
        return_value = get_ai_move(valors.GAMEPLAY_REMOVE_PIECE, curr_player)
        valors.player_pieces_onboard[opponent_player].remove(return_value)
                    
        # check if curr_player already won
        winner = isCurrentPlayerWon(curr_player)
        if winner != 0:
            if winner == valors.player_user:
                return valors.GAMEPLAY_PLAYER_WON, curr_player
            else:
                return valors.GAMEPLAY_PLAYER_LOSE, curr_player
        
        if valors.player_pieces_onhold[curr_player] > 0:
            curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
            drawBoard(valors.GAMEPLAY_PHASE, curr_player)
            drawCurrentBoard()
            drawPieces()
            drawAvailableMoves()
            return valors.GAMEPLAY_PHASE, curr_player
        elif len(valors.player_pieces_onboard[curr_player]) == 3 and len(valors.player_pieces_onboard[opponent_player]) == 3:
            if not valors.isFinal_phase:
                displayFeedback("FINAL PHASE.", (650, 185))
                pygame.time.wait(1000)
                valors.isFinal_phase = True
            curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
            drawBoard(valors.GAMEPLAY_SECOND_PHASE, curr_player)
            drawCurrentBoard()
            return valors.GAMEPLAY_FINAL_PHASE, curr_player
        else:
            curr_player = valors.player_two if curr_player == valors.player_one else valors.player_one
            drawBoard(valors.GAMEPLAY_SECOND_PHASE, curr_player)
            drawCurrentBoard()
            return valors.GAMEPLAY_SECOND_PHASE, curr_player

    return valors.GAMEPLAY_REMOVE_PIECE, curr_player

def displayFeedback(text, position):
    text_surface = font.render(text, True, valors.RED)
    text_rect = text_surface.get_rect(topleft = position)
    screen.blit(text_surface, text_rect)
    pygame.display.flip() 

def isCurrentPlayerWon(curr_player):
    if curr_player == valors.player_one:
        opponent_player = valors.player_two
    elif curr_player == valors.player_two:
        opponent_player = valors.player_one
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

    if valors.player_pieces_onhold[curr_player] == 0:
        # check pieces
        curr_player_pieces = set(valors.player_pieces_onboard[curr_player])
        if len(curr_player_pieces) <= 2:
            return opponent_player

        # check moves
        curr_player_valid_moves = checkAvailableMovesSecondPhase(curr_player, opponent_player)
        if not curr_player_valid_moves:
            return opponent_player
    
    if valors.player_pieces_onhold[opponent_player] == 0:
        # check pieces
        opponent_player_pieces = set(valors.player_pieces_onboard[opponent_player])
        if len(opponent_player_pieces) <= 2:
            return curr_player

        # check moves
        opponent_player_valid_moves = checkAvailableMovesSecondPhase(opponent_player, curr_player)
        if not opponent_player_valid_moves:
            return curr_player
    
    return 0

def isGameDraw(curr_player):
    if curr_player == valors.player_one:
        opponent_player = valors.player_two
    elif curr_player == valors.player_two:
        opponent_player = valors.player_one
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

    if valors.player_pieces_onhold[curr_player] == 0 and valors.player_pieces_onhold[opponent_player] == 0:
        curr_player_moves = checkAvailableMovesSecondPhase(curr_player, opponent_player)
        opponent_moves = checkAvailableMovesSecondPhase(opponent_player, curr_player)
        if not curr_player_moves and not opponent_moves:
            return True
    return False

def gamePlayResult(mouse_x, mouse_y, curr_player, current_phase):
    drawBoard(current_phase, curr_player)
    drawCurrentBoard()
    drawPieces()

    # play again button
    play_again_btn_width = 214
    play_again_btn_height = 65
    play_again_btn_x = 573
    play_again_btn_y = 325
    pygame.draw.rect(screen, valors.PLAY_AGAIN_COLOR, (play_again_btn_x, play_again_btn_y, play_again_btn_width, play_again_btn_height), 5)

    # exit button
    exit_btn_width = play_again_btn_width
    exit_btn_height = play_again_btn_height
    exit_btn_x = play_again_btn_x + play_again_btn_width
    exit_btn_y = play_again_btn_y
    pygame.draw.rect(screen, valors.EXIT_COLOR, (exit_btn_x, exit_btn_y, exit_btn_width, exit_btn_height), 5)

    # check if play again or exit
    if play_again_btn_x <= mouse_x <= play_again_btn_x + play_again_btn_width and play_again_btn_y <= mouse_y <= play_again_btn_y + play_again_btn_height:
        playAgain()
        return valors.MAIN_DISPLAY, 0
    
    if exit_btn_x <= mouse_x <= exit_btn_x + exit_btn_width and exit_btn_y <= mouse_y <= exit_btn_y + exit_btn_height:
        pygame.quit()
        sys.exit()
    
    return current_phase, curr_player

def playAgain():
    valors.curr_player = 0
    valors.player_user = 0
    valors.piece_clicked = (0, 0)
    valors.prev_piece_clicked = (0, 0)
    valors.white_piece_clicked = False
    valors.black_piece_clicked = False
    valors.curr_piece_clicked = False
    valors.secondPhase_currPhase = valors.GAMEPLAY_SELECT_PIECE_TO_MOVE

    valors.player_pieces_onhold = {valors.player_one: 6, valors.player_two: 6}
    valors.player_pieces_onboard = {
        valors.player_one: [],
        valors.player_two: []
    }

if __name__ == "__main__":
    prev_phase = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if current_phase == valors.MAIN_DISPLAY:
                    current_phase = mainDisplay(mouse_x, mouse_y)
                elif current_phase == valors.CHOOSE_COLOR_CHAR:
                    prev_phase = current_phase
                    current_phase, valors.player_user = chooseColor(mouse_x, mouse_y)
                    if valors.player_user == 1:
                        curr_player = valors.player_user
                    else:
                        curr_player = 2 # AI palitan nalang kase di ko pa na-declare
                elif current_phase == valors.GAMEPLAY_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = startGame(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == valors.GAMEPLAY_SECOND_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = secondPhaseGame(mouse_x, mouse_y, curr_player)
                elif current_phase == valors.GAMEPLAY_FINAL_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = finalPhaseGame(mouse_x, mouse_y, curr_player)
                elif current_phase == valors.GAMEPLAY_REMOVE_PIECE:
                    prev_phase = current_phase
                    current_phase, curr_player = removeOpponentPiece(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == valors.GAMEPLAY_PLAYER_WON or current_phase == valors.GAMEPLAY_PLAYER_LOSE or current_phase == valors.GAMEPLAY_PLAYER_DRAW:
                    prev_phase = current_phase
                    current_phase, curr_player = gamePlayResult(mouse_x, mouse_y, curr_player, current_phase)
                else:
                    print(f"[Error] Invalid current_phase. current_phase: {current_phase}")
                    pygame.quit()
                    sys.exit()
        
        if current_phase == valors.MAIN_DISPLAY:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            temp = mainDisplay(mouse_x, mouse_y)

        if prev_phase != current_phase and prev_phase != valors.GAMEPLAY_REMOVE_PIECE and prev_phase != valors.GAMEPLAY_PLAYER_WON and prev_phase != valors.GAMEPLAY_PLAYER_LOSE and prev_phase != valors.GAMEPLAY_PLAYER_DRAW:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1, 1)}))
        
        
        # Update the display
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()
