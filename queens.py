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
        """Determine if placing queen on specified square is valid."""

        pass

    def render_board(self):
        """Print current state of the board."""

        pass

    def try_all(self, depth, mode):
        """Recursively try placing queens on the current rank."""

        pass


def get_size():
    """Prompt for and return size of the board."""

    size = input('Enter board size:\n>>> ')

    # Validate input
    is_valid = False
    while not is_valid:
        try:
            # Try to convert size to int
            size = int(size)
        except ValueError:
            # Non-int entered
            size = input('Please enter an integer:\n>>> ')
        else:
            if not 1 <= size <= 26:
                # Size of board out of range
                size = input('Please enter an integer between 1 and 26:\n>>> ')
            elif size in [2, 3]:
                # No solutions for 2x2 or 3x3
                size = input('There are no solutions for a board of size '
                             '2 or 3. Please enter another integer between 1 and '
                             '26:\n>>>')
            else:
                # Size is an int and in range
                is_valid = True

    return size


def get_mode():
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
            # Non-int entered
            mode = input('Please enter 1, 2, 3, or 4:\n>>> ')
        else:
            if mode not in [1, 2, 3, 4]:
                # Invalid mode entered
                mode = input('Please enter 1, 2, 3, or 4:\n>>> ')
            else:
                # Mode is an int and in range
                is_valid = True

    return mode


def main():
    pass


if __name__ == '__main__':
    main()
