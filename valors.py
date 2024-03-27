# Screen
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAY_AGAIN_COLOR = (64, 64, 64)
EXIT_COLOR = (32, 32, 32)

MAIN_DISPLAY = 0
CHOOSE_COLOR_CHAR = 1
GAMEPLAY_PHASE = 2
GAMEPLAY_SECOND_PHASE = 3
GAMEPLAY_REMOVE_PIECE = 4
GAMEPLAY_PLAYER_WON = 5
GAMEPLAY_PLAYER_LOSE = 6
GAMEPLAY_PLAYER_DRAW = 7

GAMEPLAY_SELECT_PIECE_TO_MOVE = 8
GAMEPLAY_SELECT_VALID_POINT = 9
GAMEPLAY_NO_VALID_MOVES = 10

player_one = 1
player_two = 2
curr_player = 0
player_user = 0
piece_clicked = (0, 0)
prev_piece_clicked = (0, 0)
white_piece_clicked = False
black_piece_clicked = False
curr_piece_clicked = False
secondPhase_currPhase = GAMEPLAY_SELECT_PIECE_TO_MOVE

player_pieces = {player_one: 6, player_two: 6}
player_moves = {
    player_one: [],
    player_two: []
}

game_icon1 = "./resources/GameIcon1.png"
game_icon2 = "./resources/GameIcon2.png"
main_cover = "./resources/MainCover.png"
choose_color = "./resources/ChooseColor3.png"
white_piece_img = "./resources/white_piece1.png"
black_piece_img = "./resources/black_piece1.png"
game_bg = "./resources/GameBG1.png"

game_bg3_yourTurn = "./resources/BG3-YourTurn.png"
game_bg4_opponentTurn = "./resources/BG4-OpponentTurn.png"
game_bg5_yourTurn2 = "./resources/BG5-YourTurn2.png"
game_bg5_yourTurn2B = "./resources/BG5-YourTurn2B.png"
game_bg5_yourTurn2C = "./resources/BG5-YourTurn2C.png"
game_bg6_got3piece = "./resources/BG6-Got3Piece.png"
game_bg7_youWon = "./resources/BG7-YouWon.png"
game_bg8_youLose = "./resources/BG8-YouLose.png"
game_bg9_draw = "./resources/BG9-Draw.png"

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
consecutive_points = {
    # horizontals
    ((50, 50), (300, 50), (550, 50)): None,
    ((175, 175), (300, 175), (425, 175)): None,
    ((175, 425), (300, 425), (425, 425)): None,
    ((50, 550), (300, 550), (550, 550)): None,

    # verticals
    ((50, 50), (50, 300), (50, 550)): None,
    ((175, 175), (175, 300), (175, 425)): None,
    ((425, 175), (425, 300), (425, 425)): None,
    ((550, 50), (550, 300), (550, 550)): None
}
point_moves = {
    # row 1 points. outer upper ---
    (50, 50): [(300, 50), (50, 300)],
    (300, 50): [(50, 50), (300, 175), (550, 50)],
    (550, 50): [(300, 50), (550, 300)],

    # row 2 points. inner upper ---
    (175, 175): [(300, 175), (175, 300)],
    (300, 175): [(175, 175), (300, 50), (425, 175)], 
    (425, 175): [(300, 175), (425, 300)],

    # row 3 points. middle points -- --
    (50, 300): [(50, 50), (175, 300), (50, 550)],
    (175, 300): [(50, 300), (175, 175), (175, 425)],
    (425, 300): [(425, 175), (550, 300), (425, 425)],
    (550, 300): [(550, 50), (425, 300), (550, 550)],

    # row 4 points. inner lower ---
    (175, 425): [(175, 300), (300, 425)],
    (300, 425): [(175, 425), (300, 550), (425, 425)],
    (425, 425): [(300, 425), (425, 300)],

    # row 5 points. outer lower ---
    (50, 550): [(50, 300), (300, 550)],
    (300, 550): [(50, 550), (300, 425), (550, 550)],
    (550, 550): [(550, 300), (300, 550)]
}