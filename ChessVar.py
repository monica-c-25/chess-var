# Author: Monica Cao
# GitHub username: monica-c-25
# Date: 12/05/23
# Description: Variant of chess where winner is determined by which player captures all of the opponent's pieces of one
#               type first. Game does not include castling, en passant, or pawn promotion. King is not a special piece.

class ChessVar:
    """
    This class represents a variant of the game chess.
    """

    def __init__(self):
        # game board
        self._board = [
            ['wr', 'wp', '', '', '', '', 'bp', 'br'],
            ['wh', 'wp', '', '', '', '', 'bp', 'bh'],
            ['wb', 'wp', '', '', '', '', 'bp', 'bb'],
            ['wq', 'wp', '', '', '', '', 'bp', 'bq'],
            ['wk', 'wp', '', '', '', '', 'bp', 'bk'],
            ['wb', 'wp', '', '', '', '', 'bp', 'bb'],
            ['wh', 'wp', '', '', '', '', 'bp', 'bh'],
            ['wr', 'wp', '', '', '', '', 'bp', 'br'],
        ]

        # value_dict sets each spot on the board as coordinates for ease of indexing
        self._value_dict = {
            'a1': [0, 0], 'a2': [0, 1], 'a3': [0, 2], 'a4': [0, 3], 'a5': [0, 4], 'a6': [0, 5], 'a7': [0, 6],
            'a8': [0, 7],
            'b1': [1, 0], 'b2': [1, 1], 'b3': [1, 2], 'b4': [1, 3], 'b5': [1, 4], 'b6': [1, 5], 'b7': [1, 6],
            'b8': [1, 7],
            'c1': [2, 0], 'c2': [2, 1], 'c3': [2, 2], 'c4': [2, 3], 'c5': [2, 4], 'c6': [2, 5], 'c7': [2, 6],
            'c8': [2, 7],
            'd1': [3, 0], 'd2': [3, 1], 'd3': [3, 2], 'd4': [3, 3], 'd5': [3, 4], 'd6': [3, 5], 'd7': [3, 6],
            'd8': [3, 7],
            'e1': [4, 0], 'e2': [4, 1], 'e3': [4, 2], 'e4': [4, 3], 'e5': [4, 4], 'e6': [4, 5], 'e7': [4, 6],
            'e8': [4, 7],
            'f1': [5, 0], 'f2': [5, 1], 'f3': [5, 2], 'f4': [5, 3], 'f5': [5, 4], 'f6': [5, 5], 'f7': [5, 6],
            'f8': [5, 7],
            'g1': [6, 0], 'g2': [6, 1], 'g3': [6, 2], 'g4': [6, 3], 'g5': [6, 4], 'g6': [6, 5], 'g7': [6, 6],
            'g8': [6, 7],
            'h1': [7, 0], 'h2': [7, 1], 'h3': [7, 2], 'h4': [7, 3], 'h5': [7, 4], 'h6': [7, 5], 'h7': [7, 6],
            'h8': [7, 7]
        }

        # white_count and black count are initialized to keep track of how many of each piece has been captured
        self._white_count = {'wr': 2, 'wp': 8, 'wh': 2, 'wb': 2, 'wq': 1, 'wk': 1}
        self._black_count = {'br': 2, 'bp': 8, 'bh': 2, 'bb': 2, 'bq': 1, 'bk': 1}

        self._current_turn = 'white'
        self._game_state = 'UNFINISHED'
        self._piece_type = ''

    def get_game_state(self):
        """
        Returns one of the game states: ('UNFINISHED', 'WHITE_WON', 'BLACK_WON')
        """
        return self._game_state

    def make_move(self, start, end):
        """
        Takes a parameter the intended piece to move and destination
        Returns True or False depending on if a player's move is valid
        """
        # check if the starting index or ending index exist
        if start not in self._value_dict or end not in self._value_dict:
            return False

        # search for the coordinates of start and end in value_dict
        start_coord = self._value_dict[start]
        end_coord = self._value_dict[end]

        # retrieve the appropriate strings from the board nested list
        start_piece = self._board[start_coord[0]][start_coord[1]]
        end_piece = self._board[end_coord[0]][end_coord[1]]

        # check the game state, if either has won return False
        if self._game_state == 'WHITE_WON' or self._game_state == 'BLACK_WON':
            return False

        # check if start piece is empty
        elif start_piece == '':
            return False

        # if the start coordinate has a piece, check if the piece belongs to current player and if it does,
        #   continue otherwise return False
        elif start_piece[0] != self._current_turn[0]:
            return False

        # check to make sure starting position is not also end destination
        elif start_coord == end_coord:
            return False

        # check if end piece belongs to other player, if it doesn't return false
        elif end_piece != '' and start_piece[0] == end_piece[0]:
            return False

        else:
            # check type of piece by calling check_type()
            piece = self.check_type(start_piece)

            # check if the move is valid by calling on is_valid()
            check_valid = self.is_valid(start_coord, end_coord, piece)
            if check_valid is True:
                if end_piece == '':
                    self._board[end_coord[0]][end_coord[1]] = start_piece
                    self._board[start_coord[0]][start_coord[1]] = ''
                else:
                    self.capture_piece(end_piece)
                    self._board[end_coord[0]][end_coord[1]] = start_piece
                    self._board[start_coord[0]][start_coord[1]] = ''
                self.check_state()
                if self._current_turn == 'white':
                    self._current_turn = 'black'
                elif self._current_turn == 'black':
                    self._current_turn = 'white'
                return True
            else:
                return False

    def check_type(self, piece):
        """
        Takes as a parameter the piece which is a string
        Checks the type of piece based on the string present. For example 'wr' means white rook.
        Changes self._piece_type to whatever the identified piece is and returns it
        """
        if piece[1] == 'r':
            self._piece_type = 'rook'
            return self._piece_type
        elif piece[1] == 'q':
            self._piece_type = 'queen'
            return self._piece_type
        elif piece[1] == 'k':
            self._piece_type = 'king'
            return self._piece_type
        elif piece[1] == 'h':
            self._piece_type = 'knight'
            return self._piece_type
        elif piece[1] == 'p':
            self._piece_type = 'pawn'
            return self._piece_type
        else:
            self._piece_type = 'bishop'
            return self._piece_type

    def is_valid(self, start, end, piece):
        """
        Takes as a parameter the starting coordinate and ending coordinate, and piece which holds its type
        Checks if a move is valid, including traversing through other pieces which is invalid unless piece is a knight
        """

        # calculates the coordinate change with absolute values taken
        coord_change = [abs(end[0] - start[0]), abs(end[1] - start[1])]
        piece_type = piece
        board = self._board

        if piece_type == 'rook':
            if start[0] == end[0] or start[1] == end[1]: # if either the "x" or "y" coordinate remain the same from start to end
                if start[0] == end[0]:    # if only the "y" coordinate changed
                    if end[1] > start[1]:  # if the end y coordinate is greater than the start y coordinate
                        value = start[1] + 1
                        temp = [start[0], value]
                        while value < end[1]:  # checks values in between
                            if board[temp[0]][temp[1]] != '':  # rooks can't hop over populated spaces
                                return False
                            value += 1     # space is empty so increment the y value to check next spot
                            temp = [start[0], value]
                        return True   # no pieces in between start and end so move is valid return True
                    elif end[1] < start[1]:  # if the end y coordinate is < the start y coordinate
                        value = start[1] - 1
                        temp = [start[0], value]
                        while value > end[1]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value -= 1    # space is empty this time decrement since the end y coord is < start y coord
                            temp = [start[0], value]  # set temp equal to new coordinates
                        return True
                elif start[1] == end[1]:    # if only the "x" coordinate changed
                    if end[0] > start[0]:
                        value = start[0] + 1
                        temp = [value, start[1]]
                        while value < end[0]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value += 1
                            temp = [value, start[1]]
                        return True
                    elif end[0] < start[0]:
                        value = start[0] - 1
                        temp = [value, start[1]]
                        while value > end[0]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value -= 1
                            temp = [value, start[1]]
                        return True
            else:
                return False

        elif piece_type == 'bishop':
            if coord_change[0] == coord_change[1]:      # if the coord change for "x" and "y" are equal
                if end[0] > start[0] and end[1] > start[1]:     # if "x" and "y" both increase
                    value1 = start[0] + 1       # increment x
                    value2 = start[1] + 1       # increment y
                    temp = [value1, value2]
                    while value2 < end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 += 1             # increment x
                        value2 += 1             # increment y
                        temp = [value1, value2]
                    return True

                elif end[0] < start[0] and end[1] < start[1]:       # if "x" and "y" both decrease
                    value1 = start[0] - 1
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    while value2 > end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 -= 1
                        value2 -= 1
                        temp = [value1, value2]
                    return True

                elif end[0] > start[0] and end[1] < start[1]:       # if x increase and y decrease
                    value1 = start[0] + 1
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    while value2 > end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 += 1
                        value2 -= 1
                        temp = [value1, value2]
                    return True

                elif end[0] < start[0] and end[1] > start[1]:          # if x decrease and y increase
                    value1 = start[0] - 1
                    value2 = start[1] + 1
                    temp = [value1, value2]
                    while value2 < end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 -= 1
                        value2 += 1
                        temp = [value1, value2]
                    return True
            else:
                return False

        elif piece_type == 'queen':         # just copy and paste code from rook and bishop since same movements
            if start[0] == end[0] or start[1] == end[1]:
                if start[0] == end[0]:
                    if end[1] > start[1]:
                        value = start[1] + 1
                        temp = [start[0], value]
                        while value < end[1]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value += 1
                            temp = [start[0], value]
                        return True
                    elif end[1] < start[1]:
                        value = start[1] - 1
                        temp = [start[0], value]
                        while value > end[1]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value -= 1
                            temp = [start[0], value]
                        return True
                elif start[1] == end[1]:
                    if end[0] > start[0]:
                        value = start[0] + 1
                        temp = [value, start[1]]
                        while value < end[0]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value += 1
                            temp = [value, start[1]]
                        return True
                    elif end[0] < start[0]:
                        value = start[0] - 1
                        temp = [value, start[1]]
                        while value > end[0]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value -= 1
                            temp = [value, start[1]]
                        return True
            elif coord_change[0] == coord_change[1]:
                if end[0] > start[0] and end[1] > start[1]:
                    value1 = start[0] + 1
                    value2 = start[1] + 1
                    temp = [value1, value2]
                    while value2 < end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 += 1
                        value2 += 1
                        temp = [value1, value2]
                    return True

                elif end[0] < start[0] and end[1] < start[1]:
                    value1 = start[0] - 1
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    while value2 > end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 -= 1
                        value2 -= 1
                        temp = [value1, value2]
                    return True

                elif end[0] > start[0] and end[1] < start[1]:
                    value1 = start[0] + 1
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    while value2 > end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 += 1
                        value2 -= 1
                        temp = [value1, value2]
                    return True

                elif end[0] < start[0] and end[1] > start[1]:
                    value1 = start[0] - 1
                    value2 = start[1] + 1
                    temp = [value1, value2]
                    while value2 < end[1]:
                        if board[temp[0]][temp[1]] != '':
                            return False
                        value1 -= 1
                        value2 += 1
                        temp = [value1, value2]
                    return True
            else:
                return False

        elif piece_type == 'knight':
            if coord_change == [1, 2] or coord_change == [2, 1]:     # coord change will always be [1,2] or [2,1]
                return True         # knights can hop, no need to check in between
            else:
                return False

        elif piece_type == 'king':
            if coord_change == [1, 1] or coord_change == [0, 1] or coord_change == [1, 0]:  # always one of these coords
                return True     # kings only move one space and can capture in any direction, so no in between checks
            else:
                return False

        else:       # these valid checks are for th pawn piece, the last piece not defined yet
            if start[1] == 1 or start[1] == 6:  # for pawns who have not made their first move yet
                if coord_change == [0, 1] or coord_change == [0, 2]:       # for pawns that move forward 1 or 2 spaces
                    if end[0] == start[0] and end[1] < start[1]:
                        value1 = start[0]
                        value2 = start[1] - 1
                        temp = [value1, value2]
                        while value2 >= end[1]:
                            if board[temp[0]][temp[1]] != '':      # since pawns can only diagonal capture, spaces in between must be empty
                                return False
                            value2 -= 1
                            temp = [value1, value2]
                        return True
                    elif end[0] == start[0] and end[1] > start[1]:
                        value1 = start[0]
                        value2 = start[1] + 1
                        temp = [value1, value2]
                        while value2 <= end[1]:
                            if board[temp[0]][temp[1]] != '':
                                return False
                            value2 += 1
                            temp = [value1, value2]
                        return True
                elif coord_change == [1, 1]:        # for pawns that try to move diagonally
                    if end[0] < start[0] and end[1] < start[1]:
                        value1 = start[0] - 1
                        value2 = start[1] - 1
                        temp = [value1, value2]
                        if board[temp[0]][temp[1]] == '':   # spaces must contain opponent's piece since pawns can't move diagonally unless its a capture
                            return False
                        return True
                    elif end[0] > start[0] and end[1] < start[1]:
                        value1 = start[0] + 1
                        value2 = start[1] - 1
                        temp = [value1, value2]
                        if board[temp[0]][temp[1]] == '':
                            return False
                        return True
                    elif end[0] < start[0] and end[1] > start[1]:
                        value1 = start[0] - 1
                        value2 = start[1] + 1
                        temp = [value1, value2]
                        if board[temp[0]][temp[1]] == '':
                            return False
                        return True
                    elif end[0] > start[0] and end[1] > start[1]:
                        value1 = start[0] + 1
                        value2 = start[1] + 1
                        temp = [value1, value2]
                        if board[temp[0]][temp[1]] == '':
                            return False
                        return True
                else:
                    return False
            elif coord_change == [0, 1]:            # for pawns that have already made their first move and want to move forward
                if end[0] == start[0] and end[1] < start[1]:
                    value1 = start[0]
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    if board[temp[0]][temp[1]] != '':
                        return False
                    return True
                elif end[0] == start[0] and end[1] > start[1]:
                    value1 = start[0]
                    value2 = start[1] + 1
                    temp = [value1, value2]
                    if board[temp[0]][temp[1]] != '':
                        return False
                    return True
            elif coord_change == [1, 1]:            # for pawns that have already made their first move and want to mvoe diagonally
                if end[0] < start[0] and end[1] < start[1]:
                    value1 = start[0] - 1
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    if board[temp[0]][temp[1]] == '':
                        return False
                    return True
                elif end[0] > start[0] and end[1] < start[1]:
                    value1 = start[0] + 1
                    value2 = start[1] - 1
                    temp = [value1, value2]
                    if board[temp[0]][temp[1]] == '':
                        return False
                    return True
                elif end[0] < start[0] and end[1] > start[1]:
                    value1 = start[0] - 1
                    value2 = start[1] + 1
                    temp = [value1, value2]
                    if board[temp[0]][temp[1]] == '':
                        return False
                    return True
                elif end[0] > start[0] and end[1] > start[1]:
                    value1 = start[0] + 1
                    value2 = start[1] + 1
                    temp = [value1, value2]
                    if board[temp[0]][temp[1]] == '':
                        return False
                    return True
            else:
                return False

    def capture_piece(self, end_piece):
        """
        Takes as a parameter end_piece which is a string of the end piece
        Remove the piece from the board, decrement the count for that respective piece in the appropriate player's pile
        """
        if end_piece[0] == 'w':
            self._white_count[end_piece] -= 1
        elif end_piece[0] == 'b':
            self._black_count[end_piece] -= 1

    def check_state(self):
        """
        Checks to see if any of either white_count or black_count's types are now 0
        Sets _game_state according to appropriate winner
        """
        for piece in self._white_count.values():
            if piece == 0:
                self._game_state = 'BLACK_WON'

        for piece in self._black_count.values():
            if piece == 0:
                self._game_state = "WHITE_WON"






