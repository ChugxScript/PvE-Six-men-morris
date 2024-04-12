# MINIMAAAAX
import valors
curr_phase = None

def get_ai_move(phase, curr_player):
    best_move = None
    best_piece = None
    max_eval = float('-inf')

    opponent_player = valors.player_two if curr_player == valors.player_one else valors.player_one
    
    ai_pieces_onboard = set(valors.player_pieces_onboard[curr_player])
    opponent_pieces_onboard = set(valors.player_pieces_onboard[opponent_player])
    available_moves = ai_checkAvailableMoves(ai_pieces_onboard, opponent_pieces_onboard, 1)
    depth = 3
    global curr_phase 
    curr_phase = phase
    
    if phase == valors.GAMEPLAY_PHASE:
        # get the available point in the board
        # evaluate which point in the board has the best result then return the point

        for move in available_moves:
            new_ai_pieces = set(valors.player_pieces_onboard[curr_player].copy())
            new_ai_pieces.add(move)
            new_ai_pieces_onhold = valors.player_pieces_onhold[curr_player] - 1
            
            eval = minimax(new_ai_pieces, depth,
                        new_ai_pieces_onhold, set(valors.player_pieces_onboard[opponent_player]), 
                        valors.player_pieces_onhold[opponent_player])
            
            # Check if the move blocks opponent's mills
            eval += block_opponent_mill(set(valors.player_pieces_onboard[opponent_player]), move)
            eval += make_mill(set(valors.player_pieces_onboard[curr_player]), move)

            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move
    
    elif phase == valors.GAMEPLAY_SECOND_PHASE:
        # first is get piece from the pieces onboard
        # then get the available moves of that piece
        # evaluate which piece and move has the best result the return the piece and the move

        for piece in valors.player_pieces_onboard[curr_player]:
            for move in ai_checkPieceValidMoves(piece, ai_pieces_onboard, opponent_pieces_onboard):
                new_ai_pieces = ai_pieces_onboard.copy()
                new_ai_pieces.add(move)
                
                eval = minimax(new_ai_pieces, depth, 0, opponent_pieces_onboard, 0)
                eval += block_opponent_mill(opponent_pieces_onboard, move)
                eval += make_mill(ai_pieces_onboard, move)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    best_piece = piece
        return best_piece, best_move

    elif phase == valors.GAMEPLAY_FINAL_PHASE:
        # first is get piece from the pieces onboard
        # then get the available moves of that piece (flying phase)
        # evaluate which piece and move has the best result the return the piece and the move

        for piece in valors.player_pieces_onboard[curr_player]:
            for move in ai_checkAvailableMoves(ai_pieces_onboard, opponent_pieces_onboard, 1):
                new_ai_pieces = set(valors.player_pieces_onboard[curr_player].copy())
                new_ai_pieces.add(move)
                
                eval = minimax(new_ai_pieces, depth, 0, set(valors.player_pieces_onboard[opponent_player]), 0)
                eval += block_opponent_mill(set(valors.player_pieces_onboard[opponent_player]), move)
                eval += make_mill(set(valors.player_pieces_onboard[curr_player]), move)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    best_piece = piece
        return best_piece, best_move
    
    elif phase == valors.GAMEPLAY_REMOVE_PIECE:
        # first is get pieces from opponent
        # evaluate which piece has the best value to remove
        opponent_pieces = set(valors.player_pieces_onboard[opponent_player])
        opponent_mills = set(valors.player_pieces_prev_mills[opponent_player])
        opponent_valid_pieces = opponent_pieces - opponent_mills

        player_pieces = set(valors.player_pieces_onboard[curr_player])

        # Initialize variables to keep track of the best piece to remove and its value
        best_piece = None
        best_value = float('-inf')

        # Evaluate each piece to determine its value for removal
        for piece in opponent_valid_pieces:
            piece_value = remove_piece_value(piece, opponent_valid_pieces, player_pieces)

            # Update the best piece and its value if this piece has higher value
            if piece_value > best_value:
                best_piece = piece
                best_value = piece_value

        # Return the best piece to remove
        return best_piece

def ai_checkAvailableMoves(ai_pieces, opponent_pieces, mode):
    if mode == 1:
        inter_points = set(valors.intersection_points)
        points_occupied = set(ai_pieces | opponent_pieces)
        available_moves = inter_points - points_occupied
        return available_moves
    elif mode == 2:
        your_moves = set()
        opponent_moves = set()

        for piece in ai_pieces:
            your_moves.update(valors.point_moves[piece])

        for piece in opponent_pieces:
            opponent_moves.update(valors.point_moves[piece])
        
        your_valid_moves = your_moves - (opponent_moves | ai_pieces)
        return your_valid_moves

def ai_checkPieceValidMoves(piece_clicked, ai_pieces, opponent_pieces):
    clicked_piece_moves = set(valors.point_moves[piece_clicked])

    clicked_piece_valid_moves = clicked_piece_moves - (ai_pieces | opponent_pieces)
    return clicked_piece_valid_moves

def minimax(ai_pieces, depth, ai_pieces_onhold, opponent_pieces, opponent_pieces_onhold):
    if curr_phase == valors.GAMEPLAY_PHASE:
        if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
            return evaluate(ai_pieces, opponent_pieces)

        max_eval = float('-inf')
        for move in ai_checkAvailableMoves(ai_pieces, opponent_pieces, 1):
            new_ai_pieces = set(ai_pieces.copy())
            new_ai_pieces.add(move)
            new_ai_pieces_onhold = ai_pieces_onhold - 1
            eval = minimax(new_ai_pieces, depth - 1, new_ai_pieces_onhold, opponent_pieces, opponent_pieces_onhold)
            max_eval = max(max_eval, eval)
        return max_eval
    
    elif curr_phase == valors.GAMEPLAY_SECOND_PHASE:
        if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
            return evaluate(ai_pieces, opponent_pieces)

        max_eval = float('-inf')
        for piece in ai_pieces:
            for move in ai_checkPieceValidMoves(piece, ai_pieces, opponent_pieces):
                new_ai_pieces = set(ai_pieces.copy())
                new_ai_pieces.add(move)
                eval = minimax(new_ai_pieces, depth - 1, 0, opponent_pieces, 0)
                max_eval = max(max_eval, eval)
        return max_eval
        
    elif curr_phase == valors.GAMEPLAY_FINAL_PHASE:
        if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
            return evaluate(ai_pieces, opponent_pieces)

        max_eval = float('-inf')
        for piece in ai_pieces:
            for move in ai_checkAvailableMoves(ai_pieces, opponent_pieces, 1):
                new_ai_pieces = set(ai_pieces.copy())
                new_ai_pieces.add(move)
                eval = minimax(new_ai_pieces, depth - 1, 0, opponent_pieces, 0)
                max_eval = max(max_eval, eval)
        return max_eval
    

def ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
    if opponent_pieces_onhold == 0:
        # Check pieces
        if len(opponent_pieces) <= 2:
            return True

        # Check moves
        if not ai_checkAvailableMoves(opponent_pieces, ai_pieces, 2):
            return True
    
    return False

def evaluate(ai_pieces, opponent_pieces):
    # Assign weights to different factors
    if curr_phase == valors.GAMEPLAY_PHASE:
        piece_count_weight = 2
        mill_count_weight = 10
        mobility_weight = 2
        mode = 1

    elif curr_phase == valors.GAMEPLAY_SECOND_PHASE:
        piece_count_weight = 7
        mill_count_weight = 10
        mobility_weight = 8
        mode = 2

    elif curr_phase == valors.GAMEPLAY_FINAL_PHASE:
        piece_count_weight = 4
        mill_count_weight = 10
        mobility_weight = 8
        mode = 1

    ai_piece_count = len(ai_pieces)
    ai_mills = count_mills(ai_pieces, 1)
    ai_mobility = len(ai_checkAvailableMoves(ai_pieces, opponent_pieces, mode))
    
    # Calculate the overall score
    ai_score = (piece_count_weight * ai_piece_count) + (mill_count_weight * ai_mills) + (mobility_weight * ai_mobility)
    return ai_score

def count_mills(pieces, cmode):
    if cmode == 1:
        mill_count = 0
        for group in valors.consecutive_points:
            count = 0
            for point in group:
                if point in pieces:
                    count += 1
                    if count == 3:
                        mill_count += 1
                else:
                    count = 0
        return mill_count
    
    if cmode == 2:
        mill_count = set()
        for group in valors.consecutive_points:
            count = 0
            for point in group:
                if point in pieces:
                    count += 1
                    if count == 2:
                        mill_count.add(point)
                else:
                    count = 0
        return mill_count

    if cmode == 3:
        mill_count = set()
        for group in valors.consecutive_points:
            count = 0
            for point in group:
                if point in pieces:
                    count += 1
                    if count == 2:
                        mill_count.add(group)
                else:
                    count = 0
        return mill_count

def remove_piece_value(piece, opponent_pieces, player_pieces):
    value = 0
    # mobility
    value += len(ai_checkPieceValidMoves(piece, player_pieces, opponent_pieces))

    # potential mill formation
    mill_pieces = count_mills(opponent_pieces, 2)
    if piece in mill_pieces:
        value += 1
    
    # if out piece is getting block by opponent piece
    mill_group = count_mills(player_pieces, 3)
    for gpiece in mill_group:
        if piece in gpiece:
            value += 1
    
    return value

def block_opponent_mill(opponent_pieces, ai_move):
    for group in valors.consecutive_points:
        if ai_move in group:
            # Check if adding AI's move completes a potential mill for the opponent
            count = 0
            for point in group:
                if point in opponent_pieces:
                    count += 1
            if count == 2:
                return 100  # Block opponent's mill
    return 0

def make_mill(ai_pieces, ai_move):
    for group in valors.consecutive_points:
        if ai_move in group:
            # Check if adding AI's move completes a mill
            count = 0
            for point in group:
                if point in ai_pieces:
                    count += 1
            if count == 2:
                return 200  # AI makes a mill
    return 0