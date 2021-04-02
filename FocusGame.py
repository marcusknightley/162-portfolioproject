# Author: Marcus Knightley
# Date: 11/22/2020
# Description: This programme is a simulation of the board game Focus.
# It allows players to move stacks of pieces on the board to capture the opponent's pieces.
# The player that captures 6 pieces, wins the game.


class Player:
    """creates the player objects"""

    def __init__(self, player):
        """initialises the players of the game and returns the player and their colour in a tuple """
        self._player_name = player[0]  # assigning the player name
        self._player_colour = player[1]  # assigning the player colour

        self._captured = 0  # creating the storage for captured pieces
        self._reserve = 0  # creating the storage for reserved pieces


    def get_player_name(self):
        """returns player name"""
        return self._player_name

    def get_colour(self):
        """returns player colour"""
        return self._player_colour

    def amend_reserve(self,val):
        """adds and subtracts 1 piece from reserves"""
        self._reserve += val

    def get_reserve(self):
        """returns the reserves"""
        return self._reserve

    def amend_captured(self,val):
        """adds or subtracts 1 piece from the captured pieces"""
        self._captured += val

    def get_captured(self):
        """returns the number of captured pieces"""
        return self._captured


class FocusGame():
    """this class creates the board, takes the player objects """

    def __init__(self, player_1, player_2):
        """takes two tuples of the player objects and initialises the board with the pieces in their starting position"""

        the_board = []
        self._player_1 = Player(player_1)  # initialising the player_1 by turning the tuple into a Player class object to be able to utilise its methods
        self._player_2 = Player(player_2)  # # initialising the player_2 by turning the tuple into a Player class object to be able to utilise its methods
        colour_1 = self._player_1.get_colour()
        colour_2 = self._player_2.get_colour()

        self._last_player = None  # initialising the recorder of the last player

        #   a for loop to initiate the a list of lists with starting at (0,0) and ending at (5,5) with pieces placed at the starting position
        for i in range(0,6):
            if i % 2 == 0:
                i = [[colour_1],[colour_1],[colour_2],[colour_2],[colour_1],[colour_1]]
                the_board.append(i)
            else:
                i = [[colour_2],[colour_2],[colour_1],[colour_1],[colour_2],[colour_2]]
                the_board.append(i)

        self._board = the_board  # assigning the created board



    def move_piece(self, player_name, tuple_start, tuple_end, stack_count,):
        """moves the stack as many square as the pieces in the stack"""

        if self._last_player is not None:    # if it's not the player's turn by matching the player's name with the last_player variable's value.
            if self._last_player.lower() == player_name.lower():
                return False

        current_player = None  # determining which player is playing to call for the correct object from the Player class
        if player_name.lower() == self._player_1.get_player_name().lower():
            current_player = self._player_1
        else:
            current_player = self._player_2

        # checking the coordinates of the requested moves to make sure the move is legal
        if self.check_the_board(current_player,tuple_start,tuple_end,stack_count):
            if self.valid_piece_count(tuple_start,stack_count):  # to check if the # of pieces to be moved is legal
                self.make_move(current_player, tuple_start, tuple_end,stack_count)  # if all the moves and # of pieces to be moved are legal, makes the move
            else:
                return False
        else:
            return False
        if current_player.get_captured() == 6:  # checks to see if the player won the game after the move
            return str(current_player.get_player_name()) + " Wins"
        self._last_player = current_player.get_player_name()  # if there's not a winner, it records the player as the last player to play
        return "successfully moved"



    def check_the_board(self,current_player, tuple_start, tuple_end,stack_count):
        """check if the locations are on the board,"""
        source_row = tuple_start[0]
        source_col = tuple_start[1]
        dest_row = tuple_end[0]
        dest_col = tuple_end[1]

        # checks if both source and destination coordinates are on the board
        if -1 < source_row < 6 and -1 < source_col < 6:
            if -1 < dest_row < 6 and -1 < dest_col < 6:
                if self._board[source_row][source_col] == []:  # checks if source list is empty
                    return False
                elif abs(source_row - dest_row) == stack_count:  # checks if the pieces to be moved are equal to the # of rows to move
                    if abs(source_col - dest_col) != 0:  # if yes, checks if the columns are equal to prevent any diagonal move
                        return False
                elif abs(source_col - dest_col) == stack_count:  # checks if the pieces to be moved are equal to the # of columns to move
                    if abs(source_row - dest_row) != 0:  # if yes, checks if the rows are equal to prevent any diagonal move
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

        source_stack = self._board[source_row][source_col]
        if source_stack[-1] == current_player.get_colour():  # checks the top piece belongs to the player who is playing
            return True
        else:
            return False



    def valid_piece_count(self, tuple_start, stack_count):
        """takes the tuple of the starting position and the number of pieces to be moved to check if the move is legal"""

        the_stack = self._board[tuple_start[0]][tuple_start[1]]

        if len(the_stack) > 5:  # checks if the # of pieces to be moved and the existing stack are equal to the allowed number
            return False
        elif stack_count > 5:
            return False
        elif stack_count > len(the_stack):  # checks if pieces to be moved are greater than the existing pieces
            return False
        return True



    def make_move(self,current_player,tuple_start, tuple_end, stack_count):
        """ Places the stack on the destionation point"""

        the_colour_stack = self._board[tuple_start[0]][tuple_start[1]]

        new_stack = the_colour_stack[(len(the_colour_stack) - stack_count):]

        # append the list of stack to the existing stack on the destination location
        for i in new_stack:
            self._board[tuple_end[0]][tuple_end[1]].append(i)

        del the_colour_stack[(len(the_colour_stack)-stack_count):]


         # if the new stack is greater than the allowed number, it removes the bottom piece to either reserve or captured depending on the colour
        dest_stack = self._board[tuple_end[0]][tuple_end[1]]
        if len(dest_stack) > 5:
            while len(dest_stack) > 5:
                bottom = dest_stack[0]
                if bottom == current_player.get_colour():
                    current_player.amend_reserve(1)
                else:
                    current_player.amend_captured(1)
                del dest_stack[0]



    def show_pieces(self, pos_tuple):
        """takes a position on the board as parameter and returns a list of the pieces on that location"""
        if -1 < pos_tuple[0] < 6 and -1 < pos_tuple[1] < 6:

            the_stack = self._board[pos_tuple[0]][pos_tuple[1]]
            return the_stack
        else:
            return False



    def show_reserve(self, player_name):
        """takes the name of player as a parameter and returns the count of pieces in the reserve list for the player
        if there's not a piece in the reserve returns 0"""
        if player_name.lower() == self._player_1.get_player_name().lower():
            if self._player_1.get_reserve() == 0:
                return 0
            else:
                return self._player_1.get_reserve()
        elif player_name.lower() == self._player_2.get_player_name().lower():
            if self._player_2.get_reserve() == 0:
                return 0
            else:
                return self._player_2.get_reserve()
        else:
            return False



    def show_captured(self, player_name):
        """takes the name of player as a parameter and returns the count of pieces in the captured list for the player
                if there's not a piece in the reserve returns 0"""
        if player_name.lower() == self._player_1.get_player_name().lower():
            if self._player_1.get_captured() == 0:
                return 0
            else:
                return self._player_1.get_captured()
        elif player_name.lower() == self._player_2.get_player_name().lower():
            if self._player_2.get_captured() == 0:
                return 0
            else:
                return self._player_2.get_captured()
        else:
            return False



    def reserved_move(self, player_name, loc_tuple):
        """takes player name and a location on the board,
        then places one piece from the reserve on that spot and reduces the # of reserves by one"""

        if player_name.lower() == self._player_1.get_player_name().lower():
            current_player = self._player_1
        elif player_name.lower() == self._player_2.get_player_name().lower():
            current_player = self._player_2
        else:
            return False

        # if player's reserve storage isn't empty, moves a pieces to the desired location
        if current_player.get_reserve() != 0:
            dest_stack = self._board[loc_tuple[0]][loc_tuple[1]]
            player_piece = current_player.get_colour()
            dest_stack.append(player_piece)

            # if the location now has more than 5 pieces, it stores the bottom piece either in the reserve or in the captured depending on the colour of the piece
            if len(dest_stack) > 5:
                while len(dest_stack) > 5:
                    if dest_stack[0] == current_player.get_colour():
                        current_player.amend_reserve(1)
                    else:
                        current_player.amend_captured(1)
                    del dest_stack[0]  # deletes the piece after it is stored

            self._board[loc_tuple[0]][loc_tuple[1]] = dest_stack
        else:
            return False








#game = FocusGame(("Player_1", "R"), ("Player_2", "G"))
#game.move_piece("Player_1",(0,0),(0,1),1)
#game.show_pieces((0,1))
#game.show_captured("Player_1")
#game.reserved_move("Player_1",(0,0))
#game.move_piece("Player_2",(0,2),(0,1),1)
#game.move_piece("Player_1",(1,2),(1,1),1)
#game.move_piece("Player_2",(0,1),(0,4),3)
#game.move_piece("Player_1",(1,1),(1,0),1)
#game.move_piece("Player_2",(0,4),(4,4),4)
#game.move_piece("Player_1",(1,0),(2,0),1)
#game.move_piece("Player_2",(4,4),(1,4),3)
#game.move_piece("Player_1",(4,4),(4,2),2)
#game.move_piece("Player_2",(1,4),(3,4),2)
#game.move_piece("Player_1",(4,2),(4,5),3)
#game.move_piece("Player_2",(1,0),(1,1),1)
#game.move_piece("Player_1",(4,5),(0,5),4)
#game.show_pieces((0,5))
#game.move_piece("Player_2",(1,1),(1,3),2)
#game.move_piece("Player_1",(0,5),(5,5),5)
#game.show_pieces((0,1))


