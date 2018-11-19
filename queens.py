import string


ALPHABET = list(string.ascii_lowercase)


class Board:
    def __init__(self, size):
        """Initiate board object."""

        self.size = size
        self.board = [-1] * size

    def reset_board(self, size):
        """Remove all queens from board."""

        self.board = [-1] * size

    def update_board(self, rank, file):
        """Place queen on specified rank and file."""

        self.board[rank] = file

    def is_valid_move(self, rank, file):
        """Determine if placing queen on specified square is valid.

        This function iterates through ranks of self.board to see if
        the queens on those ranks can capture the new queen. If so,
        return false.
        """

        # Every rank before specified rank should contain queen
        assert all([i != -1 for i in self.board[0: rank]])

        # For every rank before the current rank,
        # Check if queen at current rank interferes
        # with the queen in that rank
        is_valid = True
        test_rank = 0

        while is_valid and test_rank < rank:
            assert rank - test_rank > 0, 'rank - test_rank should always be positive'

            # The file ('x' coordinate) of the queen being tested
            test_file = self.board[test_rank]

            # Tests if new queen is on same rank or diagonal as test queen
            if rank - test_rank == abs(file - test_file) or file == test_file:
                is_valid = False

            test_rank += 1

    @staticmethod
    def valid_moves(board, rank):
        """Yield all legal queen placements at the specified rank."""
        for file in range(len(rank)):
            if Board.is_valid_move(board, rank, file):
                yield file

    @staticmethod
    def render_board(board):
        """Print current state of the board."""

        size = len(board)

        # # Initialize board that will be printed
        # # Will contain lists of rows (rather than files),
        # # like [[a1, a2, a3, ...], [b1, b2, b3, ...], ...]
        # formatted_board = [[' '] * size for _ in range(size)]
        #
        # # Place queen on rank=i and file=board[i]
        # # in the formatted board
        # i = 0
        # while i != -1:
        #     formatted_board[i][board[i]] = 'Q'
        #     i += 1

        # Print top edge of the board
        print('    ┌───' + '┬───' * (size - 1) + '┐')

        # Print body of the board
        # (Loop through ranks in board backwards
        # so rank 0 is displayed at bottom)
        for rank in range(size - 1, -1, -1):
            # Print the rank coordinates
            print(' {} '.format(format(rank+1, '2d')), end='')

            # Print the leading blank squares
            for file in range(0, board[rank]):
                print('│   ', end='')

            # Print the queen if there is one on that rank
            if board[rank] != -1:
                print('│ Q ', end='')

            # Print the trailing blank squares
            for file in range(board[rank]+1, size):
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
            if i != size-1:
                print('   ', end='')
            else:
                print()

    def try_all(self, depth, mode):
        """Recursively try placing queens on the current rank."""

        pass

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
