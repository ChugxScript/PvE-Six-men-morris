import pygame
import sys
import olors

pygame.init()
current_phase = olors.MAIN_DISPLAY
white_piece_clicked = False
black_piece_clicked = False
player_user = 0

# Set up the screen
screen = pygame.display.set_mode((olors.WIDTH, olors.HEIGHT))
pygame.display.set_caption("Six Men's Morris")

def mainDisplay(mouse_x, mouse_y):
    background_image = pygame.image.load(olors.main_cover)
    background_image = pygame.transform.scale(background_image, (olors.WIDTH, olors.HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define the coordinates and dimensions of the button
    button_width = 300
    button_height = 40
    button_x = (olors.WIDTH - button_width) // 2
    button_y = 510
    
    pygame.draw.rect(screen, (0, 0, 0), (button_x, button_y, button_width, button_height), 2)

    # Check if the mouse click is within the button area
    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        return olors.CHOOSE_COLOR_CHAR

    return olors.MAIN_DISPLAY

def chooseColor(mouse_x, mouse_y):
    global white_piece_clicked, black_piece_clicked, player_user
    background_image = pygame.image.load(olors.choose_color)
    background_image = pygame.transform.scale(background_image, (olors.WIDTH, olors.HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define button dimensions
    button_width = 300
    button_height = 400
    white_button_x = 600
    black_button_x = 100
    button_y = 125

    start_button_width = 300
    start_button_height = 40
    start_button_x = (olors.WIDTH - start_button_width) // 2
    start_button_y = 530

    # Draw white and black pieces as buttons
    white_piece = pygame.image.load(olors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (button_width, button_height))
    black_piece = pygame.image.load(olors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (button_width, button_height))

    # draw a rect_point for start button as red
    pygame.draw.rect(screen, (255, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)

    # Check if mouse is over the white piece button
    if white_button_x <= mouse_x <= white_button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        # if white piece is already clicked and then clicked again
        if white_piece_clicked:
            white_piece_clicked = False

        # if black piece is selected, change the current selected piece to white
        elif black_piece_clicked: 
            black_piece_clicked = False
            white_piece_clicked = True

        else:
            white_piece_clicked = True

    # Check if mouse is over the black piece button
    if black_button_x <= mouse_x <= black_button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        # if black piece is already clicked and then clicked again
        if black_piece_clicked:
            black_piece_clicked = False

        # if white piece is selected, change the current selected piece to black
        elif white_piece_clicked: 
            white_piece_clicked = False
            black_piece_clicked = True

        else:
            black_piece_clicked = True
        
    # transform the pieces
    if white_piece_clicked:
        screen.blit(pygame.transform.scale(white_piece, (button_width + 40, button_height + 40)), (white_button_x - 10, button_y - 10))
    elif not white_piece_clicked:
        screen.blit(white_piece, (white_button_x, button_y))

    if black_piece_clicked:
        screen.blit(pygame.transform.scale(black_piece, (button_width + 40, button_height + 40)), (black_button_x - 10, button_y - 10))
    elif not black_piece_clicked:
        screen.blit(black_piece, (black_button_x, button_y))

    # check if there is selected piece
    if white_piece_clicked or black_piece_clicked:
        # draw a rect_point for start button as green
        pygame.draw.rect(screen, (0, 255, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)
        if start_button_x <= mouse_x <= start_button_x + start_button_width and start_button_y <= mouse_y <= start_button_y + start_button_height:
            if white_piece_clicked:
                player_user = olors.player_one
                return olors.GAMEPLAY_PHASE, olors.player_one
            elif black_piece_clicked:
                player_user = olors.player_two
                return olors.GAMEPLAY_PHASE, olors.player_two
    else:
        # draw a rect_point for start button as red
        pygame.draw.rect(screen, (255, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)
    return olors.CHOOSE_COLOR_CHAR, 0

def startGame(mouse_x, mouse_y, curr_player, current_phase):
    drawBoard(current_phase, curr_player)
    drawCurrentBoard()
    drawPieces()
    
    if olors.player_pieces[curr_player] > 0:
        available_moves = checkAvailableMoves()
        for point in olors.intersection_points:
            distance = ((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2) ** 0.5
            if distance <= olors.POINT_RADIUS:
                if point in available_moves:
                    drawBoard(current_phase, curr_player)
                    drawCurrentBoard()
                    placePieceOnBoard(curr_player, point)
                    drawPieces()

                    # check if curr_player place a 3 consecutive pieces
                    if isConsecutivePoints(olors.player_moves[curr_player]):
                        return olors.GAMEPLAY_REMOVE_PIECE, curr_player

                    # check if curr_player already won
                    winner = isCurrentPlayerWon(curr_player)
                    if winner != 0:
                        if winner == player_user:
                            return olors.GAMEPLAY_PLAYER_WON, winner
                        else:
                            return olors.GAMEPLAY_PLAYER_LOSE, curr_player
                    
                    # check if the game is draw
                    if isGameDraw(curr_player):
                        return olors.GAMEPLAY_PLAYER_DRAW, curr_player
                    
                    # change current player
                    curr_player = olors.player_two if curr_player == olors.player_one else olors.player_one
                    drawBoard(current_phase, curr_player)
                    drawCurrentBoard()
                    drawPieces()
                    return olors.GAMEPLAY_PHASE, curr_player
                else:
                    print(f"[Error] Invalid Move. point: {point}")
                    drawCurrentBoard()
                    drawPieces()
                    return olors.GAMEPLAY_PHASE, curr_player
        return olors.GAMEPLAY_PHASE, curr_player
    else:
        return olors.GAMEPLAY_SECOND_PHASE, curr_player

def secondPhaseGame(mouse_x, mouse_y, curr_player, current_phase):
    drawBoard(current_phase, curr_player)
    drawPieces()
    
    # the flow will be like choosing colors
    # if player click a piece it will expand the size then show the valid moves
    #   the valid moves will turn the dot into green colors
    # if piece has no valid moves change the background to 'piece has no valid moves'
    # if the player click again the clicked piece it will turn back to normal size
    #   the valid moves also disappear
    curr_player_pieces = set(olors.player_moves[curr_player])
    for piece in curr_player_pieces:
        piece_distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
        if piece_distance <= olors.POINT_RADIUS:
            curr_player_available_moves = olors.point_moves[piece]
            for curr_player_move in olors.intersection_points:
                player_move_distance = ((mouse_x - curr_player_move[0]) ** 2 + (mouse_y - curr_player_move[1]) ** 2) ** 0.5
                if player_move_distance <= olors.POINT_RADIUS:
                    if curr_player_move in curr_player_available_moves:
                        drawBoard(current_phase, curr_player)
                        drawCurrentBoard()
                        placePieceOnBoard(curr_player, player_move_distance)
                        drawPieces()

                        # check if curr_player place a 3 consecutive pieces
                        if isConsecutivePoints(olors.player_moves[curr_player]):
                            return olors.GAMEPLAY_REMOVE_PIECE, curr_player

                        # check if curr_player already won
                        winner = isCurrentPlayerWon(curr_player)
                        if winner != 0:
                            if winner == player_user:
                                return olors.GAMEPLAY_PLAYER_WON, winner
                            else:
                                return olors.GAMEPLAY_PLAYER_LOSE, curr_player
                        
                        # check if the game is draw
                        if isGameDraw(curr_player):
                            return olors.GAMEPLAY_PLAYER_DRAW, curr_player
                        
                        # change current player
                        curr_player = olors.player_two if curr_player == olors.player_one else olors.player_one
                        return olors.GAMEPLAY_SECOND_PHASE, curr_player
                    else:
                        print(f"[Error] Invalid Move. player_move_distance: {player_move_distance}")
                        drawCurrentBoard()
                        drawPieces()
                        return olors.GAMEPLAY_SECOND_PHASE, curr_player
    return olors.GAMEPLAY_SECOND_PHASE, curr_player

def drawBoard(curr_phase, curr_user):
    if curr_phase == olors.GAMEPLAY_PHASE and curr_user == player_user:
        background_image = pygame.image.load(olors.game_bg3_yourTurn)
    elif curr_phase == olors.GAMEPLAY_PHASE and curr_user != player_user:
        background_image = pygame.image.load(olors.game_bg4_opponentTurn)
    elif curr_phase == olors.GAMEPLAY_SECOND_PHASE and curr_user == player_user:
        background_image = pygame.image.load(olors.game_bg5_yourTurn2)
    elif curr_phase == olors.GAMEPLAY_SECOND_PHASE and curr_user != player_user:
        background_image = pygame.image.load(olors.game_bg4_opponentTurn)
    elif curr_phase == olors.GAMEPLAY_REMOVE_PIECE and curr_user == player_user:
        background_image = pygame.image.load(olors.game_bg6_got3piece)
    elif curr_phase == olors.GAMEPLAY_REMOVE_PIECE and curr_user != player_user:
        background_image = pygame.image.load(olors.game_bg4_opponentTurn)
    elif curr_phase == olors.GAMEPLAY_PLAYER_WON and curr_user == player_user:
        background_image = pygame.image.load(olors.game_bg7_youWon)
    elif curr_phase == olors.GAMEPLAY_PLAYER_LOSE and curr_user != player_user:
        background_image = pygame.image.load(olors.game_bg8_youLose)
    elif curr_phase == olors.GAMEPLAY_PLAYER_DRAW:
        background_image = pygame.image.load(olors.game_bg9_draw)
    else:
        background_image = pygame.image.load(olors.game_bg)
        print(f"[Error] Invalid curr_phase: {curr_phase} or curr_user: {curr_user}")

    background_image = pygame.transform.scale(background_image, (olors.WIDTH, olors.HEIGHT))
    screen.blit(background_image, (0, 0))
    
    # Outer square
    pygame.draw.line(screen, olors.BLACK, (50, 50), (550, 50), olors.LINE_WIDTH) # upper ---
    pygame.draw.line(screen, olors.BLACK, (50, 50), (50, 550), olors.LINE_WIDTH) # left |
    pygame.draw.line(screen, olors.BLACK, (550, 50), (550, 550), olors.LINE_WIDTH) # right |
    pygame.draw.line(screen, olors.BLACK, (50, 550), (550, 550), olors.LINE_WIDTH) # lower ---

    # edges connecting the outer and inner squares
    pygame.draw.line(screen, olors.BLACK, (300, 50), (300, 175), olors.LINE_WIDTH) # upper |
    pygame.draw.line(screen, olors.BLACK, (50, 300), (175, 300), olors.LINE_WIDTH) # left ---
    pygame.draw.line(screen, olors.BLACK, (425, 300), (550, 300), olors.LINE_WIDTH) # right ---
    pygame.draw.line(screen, olors.BLACK, (300, 425), (300, 550), olors.LINE_WIDTH) # lower |
    
    # Inner square
    pygame.draw.line(screen, olors.BLACK, (175, 175), (425, 175), olors.LINE_WIDTH) # upper ---
    pygame.draw.line(screen, olors.BLACK, (175, 175), (175, 425), olors.LINE_WIDTH) # left |
    pygame.draw.line(screen, olors.BLACK, (425, 175), (425, 425), olors.LINE_WIDTH) # right |
    pygame.draw.line(screen, olors.BLACK, (175, 425), (425, 425), olors.LINE_WIDTH) # lower ---
    
    # Draw little circles at each intersection point
    for point in olors.intersection_points:
        pygame.draw.circle(screen, olors.BLACK, point, 10) 

def drawPieces():
    # pieces dimensions
    piece_width = 100
    piece_height = 100
    piece_x = 600
    white_piece_y = 50
    black_piece_y = olors.HEIGHT - 150

    white_piece = pygame.image.load(olors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(olors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))

    # Draw white pieces
    for i in range(olors.player_pieces[olors.player_one]):
        screen.blit(white_piece, (piece_x + i * 50, white_piece_y))

    # Draw black pieces
    for i in range(olors.player_pieces[olors.player_two]):
        screen.blit(black_piece, (piece_x + i * 50, black_piece_y))

def drawCurrentBoard():
    # pieces dimensions
    piece_width = 100
    piece_height = 100

    white_piece = pygame.image.load(olors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(olors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))

    for point in olors.player_moves[olors.player_one]:
        screen.blit(white_piece, (point[0] - white_piece.get_width() // 2, point[1] - white_piece.get_height() // 2))
    
    for point in olors.player_moves[olors.player_two]:
        screen.blit(black_piece, (point[0] - black_piece.get_width() // 2, point[1] - black_piece.get_height() // 2))

# first phase
def checkAvailableMoves():
    inter_points = set(olors.intersection_points)
    points_occupied = set(olors.player_moves[olors.player_one] + olors.player_moves[olors.player_two])
    available_moves = inter_points - points_occupied
    return available_moves

# second phase
def checkAvailableMovesSecondPhase(curr_player, opponent_player):
    curr_player_pieces = set(olors.player_moves[curr_player])
    opponent_player_pieces = set(olors.player_moves[opponent_player])

    curr_player_moves = set()
    opponent_player_moves = set()

    for piece in curr_player_pieces:
        curr_player_moves.update(olors.point_moves[piece])

    for piece in opponent_player_pieces:
        opponent_player_moves.update(olors.point_moves[piece])

    curr_player_valid_moves = curr_player_moves - (opponent_player_pieces | curr_player_pieces)

    return curr_player_valid_moves

def placePieceOnBoard(curr_player, point):
    # pieces dimensions
    piece_width = 100
    piece_height = 100

    white_piece = pygame.image.load(olors.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(olors.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))

    if curr_player == olors.player_one:
        screen.blit(white_piece, (point[0] - white_piece.get_width() // 2, point[1] - white_piece.get_height() // 2))
        olors.player_moves[curr_player].append(point)
        olors.player_pieces[curr_player] -= 1
    elif curr_player == olors.player_two:
        screen.blit(black_piece, (point[0] - black_piece.get_width() // 2, point[1] - black_piece.get_height() // 2))
        olors.player_moves[curr_player].append(point)
        olors.player_pieces[curr_player] -= 1
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

def isConsecutivePoints(curr_player_moves):
    for group in olors.consecutive_points:
        count = 0
        for point in group:
            if point in curr_player_moves:
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
    return False

def removeOpponentPiece(mouse_x, mouse_y, curr_player, current_phase):
    drawBoard(current_phase, curr_player)
    drawCurrentBoard()
    drawPieces()

    if curr_player == olors.player_one:
        for opponent_piece in olors.player_moves[olors.player_two]:
            distance = ((mouse_x - opponent_piece[0]) ** 2 + (mouse_y - opponent_piece[1]) ** 2) ** 0.5
            if distance <= olors.POINT_RADIUS:
                olors.player_moves[olors.player_two].remove(opponent_piece)
                
                # check if curr_player already won
                winner = isCurrentPlayerWon(curr_player)
                if winner != 0:
                    if winner == player_user:
                        return olors.GAMEPLAY_PLAYER_WON, curr_player
                    else:
                        return olors.GAMEPLAY_PLAYER_LOSE, curr_player
                
                curr_player = olors.player_two if curr_player == olors.player_one else olors.player_one
                drawBoard(current_phase, curr_player)
                drawCurrentBoard()
                drawPieces()
                return olors.GAMEPLAY_PHASE, curr_player
    elif curr_player == olors.player_two:
        for opponent_piece in olors.player_moves[olors.player_one]:
            distance = ((mouse_x - opponent_piece[0]) ** 2 + (mouse_y - opponent_piece[1]) ** 2) ** 0.5
            if distance <= olors.POINT_RADIUS:
                olors.player_moves[olors.player_one].remove(opponent_piece)

                # check if curr_player already won
                winner = isCurrentPlayerWon(curr_player)
                if winner != 0:
                    if winner == player_user:
                        return olors.GAMEPLAY_PLAYER_WON, curr_player
                    else:
                        return olors.GAMEPLAY_PLAYER_LOSE, curr_player
                
                curr_player = olors.player_two if curr_player == olors.player_one else olors.player_one
                drawBoard(olors.GAMEPLAY_PHASE, curr_player)
                drawCurrentBoard()
                drawPieces()
                return olors.GAMEPLAY_PHASE, curr_player
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")
    
    return olors.GAMEPLAY_REMOVE_PIECE, curr_player

def isCurrentPlayerWon(curr_player):
    if curr_player == olors.player_one:
        opponent_player = olors.player_two
    elif curr_player == olors.player_two:
        opponent_player = olors.player_one
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

    if olors.player_pieces[curr_player] == 0:
        # check pieces
        curr_player_pieces = set(olors.player_moves[curr_player])
        if len(curr_player_pieces) <= 2:
            return opponent_player

        # check moves
        curr_player_valid_moves = checkAvailableMovesSecondPhase(curr_player, opponent_player)
        if not curr_player_valid_moves:
            return opponent_player
    
    if olors.player_pieces[opponent_player] == 0:
        # check pieces
        opponent_player_pieces = set(olors.player_moves[opponent_player])
        if len(opponent_player_pieces) <= 2:
            return curr_player

        # check moves
        opponent_player_valid_moves = checkAvailableMovesSecondPhase(opponent_player, curr_player)
        if not opponent_player_valid_moves:
            return curr_player
    
    return 0

def isGameDraw(curr_player):
    if curr_player == olors.player_one:
        opponent_player = olors.player_two
    elif curr_player == olors.player_two:
        opponent_player = olors.player_one
    else:
        print(f"[Error] Invalid curr_player. curr_player: {curr_player}")

    if olors.player_pieces[curr_player] == 0 and olors.player_pieces[opponent_player] == 0:
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
    play_again_btn_width = 200
    play_again_btn_height = 40
    play_again_btn_x = 50
    play_again_btn_y = 50
    pygame.draw.rect(screen, olors.GREEN, (play_again_btn_x, play_again_btn_y, play_again_btn_width, play_again_btn_height), 5)

    # exit button
    exit_btn_width = 200
    exit_btn_height = 40
    exit_btn_x = 50
    exit_btn_y = 100
    pygame.draw.rect(screen, olors.RED, (exit_btn_x, exit_btn_y, exit_btn_width, exit_btn_height), 5)

    # check if play again or exit
    if play_again_btn_x <= mouse_x <= play_again_btn_x + play_again_btn_width and play_again_btn_y <= mouse_y <= play_again_btn_y + play_again_btn_height:
        return olors.MAIN_DISPLAY, 0
    
    if exit_btn_x <= mouse_x <= exit_btn_x + exit_btn_width and exit_btn_y <= mouse_y <= exit_btn_y + exit_btn_height:
        pygame.quit()
        sys.exit()
    
    return current_phase, curr_player

if __name__ == "__main__":
    prev_phase = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if current_phase == olors.MAIN_DISPLAY:
                    current_phase = mainDisplay(mouse_x, mouse_y)
                elif current_phase == olors.CHOOSE_COLOR_CHAR:
                    prev_phase = current_phase
                    current_phase, player_user = chooseColor(mouse_x, mouse_y)
                    if player_user == 1:
                        curr_player = player_user
                    else:
                        curr_player = 2 # AI palitan nalang kase di ko pa na-declare
                elif current_phase == olors.GAMEPLAY_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = startGame(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == olors.GAMEPLAY_SECOND_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = secondPhaseGame(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == olors.GAMEPLAY_REMOVE_PIECE:
                    prev_phase = current_phase
                    current_phase, curr_player = removeOpponentPiece(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == olors.GAMEPLAY_PLAYER_WON or current_phase == olors.GAMEPLAY_PLAYER_LOSE or current_phase == olors.GAMEPLAY_PLAYER_DRAW:
                    prev_phase = current_phase
                    current_phase, curr_player = gamePlayResult(mouse_x, mouse_y, curr_player, current_phase)
                else:
                    print(f"[Error] Invalid current_phase. current_phase: {current_phase}")
                    pygame.quit()
                    sys.exit()
        
        if current_phase == olors.MAIN_DISPLAY:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            temp = mainDisplay(mouse_x, mouse_y)

        if prev_phase != current_phase and prev_phase != olors.GAMEPLAY_REMOVE_PIECE:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1, 1)}))

        # Update the display
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()
