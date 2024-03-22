import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# first phase
BUTTON_COLOR = (100, 100, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X, BUTTON_Y = (WIDTH - BUTTON_WIDTH) // 2, (HEIGHT - BUTTON_HEIGHT) // 2

MAIN_DISPLAY = 0
CHOOSE_COLOR_CHAR = 1
GAMEPLAY_PHASE = 2
current_phase = MAIN_DISPLAY

player_one = 1
player_two = 2
player_user = 0
curr_player = 0

white_piece_clicked = False
black_piece_clicked = False

main_cover = "./resources/MainCover.png"
choose_color = "./resources/ChooseColor3.png"
white_piece_img = "./resources/white_piece1.png"
black_piece_img = "./resources/black_piece1.png"
game_bg = "./resources/GameBG1.png"

# Initialize player pieces
player_pieces = {player_one: 6, player_two: 6}

# board
BLACK = (0, 0, 0)
LINE_WIDTH = 5
POINT_RADIUS = 20

# board intersection points
intersection_points = [
    (50, 50), (300, 50), (550, 50),                       # +---+---+      the intersection (corners)
    (175, 175), (300, 175), (425, 175),                   # | +-+-+ |      will look something like this
    (50, 300), (175, 300), (425, 300), (550, 300),        # + +   + +
    (175, 425), (300, 425), (425, 425),                   # | +-+-+ |
    (50, 550), (300, 550), (550, 550)                     # +---+---+
]

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Six Men's Morris")

def mainDisplay(mouse_x, mouse_y):
    background_image = pygame.image.load(main_cover)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define the coordinates and dimensions of the button
    button_width = 300
    button_height = 40
    button_x = (WIDTH - button_width) // 2
    button_y = 510
    
    pygame.draw.rect(screen, (0, 0, 0), (button_x, button_y, button_width, button_height), 2)

    # Check if the mouse click is within the button area
    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        return CHOOSE_COLOR_CHAR

    return MAIN_DISPLAY

def chooseColor(mouse_x, mouse_y):
    global white_piece_clicked, black_piece_clicked
    background_image = pygame.image.load(choose_color)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define button dimensions
    button_width = 300
    button_height = 400
    white_button_x = 600
    black_button_x = 100
    button_y = 125

    start_button_width = 300
    start_button_height = 40
    start_button_x = (WIDTH - start_button_width) // 2
    start_button_y = 530

    # Draw white and black pieces as buttons
    white_piece = pygame.image.load(white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (button_width, button_height))
    black_piece = pygame.image.load(black_piece_img)
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
                return GAMEPLAY_PHASE, 1
            elif black_piece_clicked:
                return GAMEPLAY_PHASE, 2
    else:
        # draw a rect_point for start button as red
        pygame.draw.rect(screen, (255, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 5)
    return CHOOSE_COLOR_CHAR

def startGame(mouse_x, mouse_y, curr_player):
    # print board
    # print the pieces

    # if curr_player pieces_onHold is not 0
    #     available_moves = check_available_moves(curr_player)
    #     if curr_player move is in available_moves 
    #         place piece to the intersection_point
    #         store intersection_point to curr_player.piece_coord
    #         curr_player pieces_onHold -= 1

    #         if curr_player == 1
    #             if player two pieces_onHold == 0 
    #                 opponent_moves = check_available_moves(player two)
    #                 if player two available moves == 0 or player two current_pieces <= 2
    #                     return curr_player wins , RESULT_PHASE
    #             curr_player = 2
    #         elif curr_player == 2
    #             if player one pieces_onHold == 0 
    #                 opponent_moves = check_available_moves(player one)
    #                 if player one available moves == 0 or player one current_pieces <= 2
    #                     return curr_player wins , RESULT_PHASE
    #             curr_player = 1
    #     else
    #         try again
    # else 
    #     return SECOND_PHASE_GAME
    pass
    
def draw_board():
    # Clear the screen
    screen.fill(WHITE)
    
    # Outer square
    pygame.draw.line(screen, BLACK, (50, 50), (550, 50), LINE_WIDTH) # upper ---
    pygame.draw.line(screen, BLACK, (50, 50), (50, 550), LINE_WIDTH) # left |
    pygame.draw.line(screen, BLACK, (550, 50), (550, 550), LINE_WIDTH) # right |
    pygame.draw.line(screen, BLACK, (50, 550), (550, 550), LINE_WIDTH) # lower ---

    # edges connecting the outer and inner squares
    pygame.draw.line(screen, BLACK, (300, 50), (300, 175), LINE_WIDTH) # upper |
    pygame.draw.line(screen, BLACK, (50, 300), (175, 300), LINE_WIDTH) # left ---
    pygame.draw.line(screen, BLACK, (425, 300), (550, 300), LINE_WIDTH) # right ---
    pygame.draw.line(screen, BLACK, (300, 425), (300, 550), LINE_WIDTH) # lower |
    
    # Inner square
    pygame.draw.line(screen, BLACK, (175, 175), (425, 175), LINE_WIDTH) # upper ---
    pygame.draw.line(screen, BLACK, (175, 175), (175, 425), LINE_WIDTH) # left |
    pygame.draw.line(screen, BLACK, (425, 175), (425, 425), LINE_WIDTH) # right |
    pygame.draw.line(screen, BLACK, (175, 425), (425, 425), LINE_WIDTH) # lower ---
    
    # Draw little circles at each intersection point
    for point in intersection_points:
        pygame.draw.circle(screen, BLACK, point, 10) 

def draw_pieces():
    # Draw player one's pieces
    for i in range(player_pieces[player_one]):
        pygame.draw.circle(screen, GRAY, (600 + i * 50, 50), 20)

    # Draw player two's pieces
    for i in range(player_pieces[player_two]):
        pygame.draw.circle(screen, BLACK, (600 + i * 50, HEIGHT - 50), 20)

def handle_gameplay_phase(mouse_x, mouse_y):
    global curr_player

    print(f"curr_player: {curr_player}")
    # Check if the current player has pieces left to place on the board
    if player_pieces[curr_player] > 0:
        for point in intersection_points:
            distance = ((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2) ** 0.5
            if distance <= POINT_RADIUS:
                # Player places a piece on the board
                player_pieces[curr_player] -= 1
                # Implement logic for handling the piece placement
                print(f"Player {curr_player} placed a piece at {point}")
                # Switch to the next player
                curr_player = player_two if curr_player == player_one else player_one

if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if current_phase == MAIN_DISPLAY:
                    current_phase = mainDisplay(mouse_x, mouse_y)
                elif current_phase == CHOOSE_COLOR_CHAR:
                    current_phase, player_user = chooseColor(mouse_x, mouse_y)
                    if player_user == 1:
                        curr_player = player_user
                    else:
                        curr_player = 2 # AI palitan nalang kase di ko pa na-declare
                elif current_phase == GAMEPLAY_PHASE:
                    startGame(mouse_x, mouse_y, curr_player)
                else:
                    print(f"[Error] Invalid current_phase. current_phase: {current_phase}")
                    pygame.quit()
                    sys.exit()
        
        if current_phase == MAIN_DISPLAY:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            current_phase = mainDisplay(mouse_x, mouse_y)

        # Update the display
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()
