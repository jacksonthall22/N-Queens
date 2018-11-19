import string


ALPHABET = list(string.ascii_lowercase)


class Board:
    def __init__(self, state=None, size=None):
        """Initialize board object.

        The following can all be used to create a board object
                of size 5 and an empty state:
            Board([-1, -1, -1, -1, -1], 5)
            Board([-1, -1, -1, -1, -1])
            Board(5)
        """

        if state is size is None:
            raise ValueError('Board object initialized without state or size kwargs')

        # Makes it possible to enter Board(8) instead of
        # Board(None, 8) to initialize board of length 8
        if type(state) != list and state is not None:
            if type(state) == int:
                size = state
                state = [-1] * size
            else:
                # State is not a list or an int
                raise ValueError('Board object initialized with non-int as its only argument: {}'.format(state))
        elif state is None:
            state = [-1] * size
        elif size is None:
            size = max(len(state), max(state)+1)

            if not 0 < size < 27:
                raise ValueError('Board object initialized with size out of range: {}'.format(size))

            # Add ranks to the state if any value in state is
            # bigger than len(state) to make board a square
            state += [-1] * (size - len(state))

        self.state = state
        self.size = size

    def reset_board(self):
        """Remove all queens from board."""

        self.state = [-1] * self.size

    def update_board(self, rank, file):
        """Place queen on the board at the specified rank and file."""

        self.state[rank] = file

    def find_all(self, mode=1, depth=1) -> list:
        """Recursively find and return list of all board states to render.

        Depending on the mode, self.state will be added to the
        boards list at different stages of the search process so
        they can be displayed accordingly after being returned.

        If there are valid moves when depth==self.size-1, this
        is a solution because a queen has been successfully
        placed on every rank.  There is no need to update the
        board if this is the case.
        """

        # All ranks before current rank should be filled
        assert all([i != -1 if len(self.state[0:depth - 1]) != 0 else True for i in self.state[0:depth - 1]]), \
            'previous state ranks do not contain queen: {}'.format(self.state)

        states = []

        # Depth is 1-indexed, rank should be 0-indexed
        rank = depth - 1

        # For all files on the current rank where it's possible, place a
        # queen there, call try_all() with depth+1, undo queen placement
        possible_moves = Board.valid_moves(self.state, rank)
        for file in possible_moves:
            # Place the queen here so next depths can be searched.
            # If this is the final depth, no need to do this, simply
            # return the state in a list.
            if depth < self.size:
                self.update_board(rank, file)
                states += self.find_all(mode, depth+1)
            else:
                return [self.state]

            self.update_board(rank, -1)

        return states

    @staticmethod
    def is_valid_move(state, rank, file):
        """Determine if placing queen on specified square is valid.

        This function iterates through first 'rank' ranks of self.state
        to see if the queens on those ranks can capture the new queen.
        If so, the move is invalid.
        """

        # Every rank before specified rank should contain queen
        assert all([i != -1 for i in state[0: rank]])

        # For every rank before the current rank, check if queen
        # on that rank interferes with the new queen
        test_rank = 0
        while test_rank < rank:
            # The file ('x' coordinate) whose queen is being tested
            test_file = state[test_rank]

            # Invalid if this queen is on same file or diagonal as the new queen
            if file == test_file or rank - test_rank == abs(file - test_file):
                return False

            test_rank += 1

        # Placement is valid iff no other queen can be attacked from its square
        return True

    @staticmethod
    def valid_moves(state, rank):
        """Yield generator of all legal queen placements at the specified rank."""

        for file in range(len(state)):
            if Board.is_valid_move(state, rank, file):
                yield file

    @staticmethod
    def render_board(state):
        """Print current state of the board."""

        size = len(state)
        assert size <= 26

        # Print top edge of the board
        print('    ┌───' + '┬───' * (size - 1) + '┐')

        # Print body of the board
        # (Loop through ranks in self.state backwards
        # so rank 0 is displayed at bottom)
        for rank in range(size - 1, -1, -1):
            # Print the rank coordinates
            print(' {} '.format(format(rank+1, '2d')), end='')

            # Print the leading blank squares
            for file in range(0, state[rank]):
                print('│   ', end='')

            # Print the queen if there is one on that rank
            if state[rank] != -1:
                print('│ Q ', end='')

            # Print the trailing blank squares
            for file in range(state[rank] + 1, size):
                print('│   ', end='')

            # Print the right edge of board
            print('│')

            # Print lines that separate ranks,
            # unless it is the bottom of the board
            if rank != 0:
                print('    ├───' + '┼───' * (size-1) + '┤')
            else:
                print('    └───' + '┴───' * (size-1) + '┘')

        # Print file coordinates
        print('      ', end='')
        for i in range(0, size):
            print(ALPHABET[i], end='')

            # Print spaces if it's not the last file, else a newline
            if i != size - 1:
                print('   ', end='')
            else:
                print()


def prompt_for_size():
    """Prompt for and return size of the board."""

    size = input('Enter board size:\n>>> ')

    # Validate input while size entered is invalid
    is_valid = False
    while not is_valid:
        try:
            # Try to convert size to int
            size = int(size)
        except ValueError:
            # Non-int was entered
            size = input('Please enter an integer:\n>>> ')
        else:
            if not 1 <= size <= 26:
                # Size of board out of range
                size = input('Please enter an integer between 1 and 26:\n>>> ')
            elif size in [2, 3]:
                # No solutions exist for 2x2 or 3x3 boards
                size = input('There are no solutions for a board of size '
                             '2 or 3. Please enter another integer between 1 and '
                             '26:\n>>>')
            else:
                # Size is an int and in range
                is_valid = True

    return size


def prompt_for_mode():
    """Prompt for and return display mode."""

    print('Choose from a mode below: ')
    print('\t1: Show all solutions immediately')
    print('\t2: Pause at each solution')
    print('\t3: Visual execution - cycle queen placements and '
          'pause at solutions')
    print('\t4: Step-by-step - pause at every queen placement\n')
    mode = input('>>> ')

    # Validate input
    is_valid = False
    while not is_valid:
        try:
            # Try to convert mode to int
            mode = int(mode)
        except ValueError:
            # Non-int was entered
            mode = input('Please enter 1, 2, 3, or 4:\n>>> ')
        else:
            if mode not in [1, 2, 3, 4]:
                # Invalid mode was entered
                mode = input('Please enter 1, 2, 3, or 4:\n>>> ')
            else:
                # Mode is an int and in range
                is_valid = True

    return mode


def main():
    pass


if __name__ == '__main__':
    main()
