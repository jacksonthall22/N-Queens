class Board:
    def __init__(self, size):
        self.size = size

    def get_size(self):
        """Prompt for and return size of the board."""

        size = input('Enter board size:\n>>> ')

        # Validate input
        is_valid = False
        while not is_valid:
            try:
                # Try to convert size to int
                size = int(size)

            except ValueError:
                size = input('Please enter an integer:\n>>> ')

            else:
                if not 1 <= size <= 26:
                    # Size of board out of range
                    size = input('Please enter an integer between 1 and 26:\n'
                                 '>>> ')
                elif size in [2, 3]:
                    # No solutions for 2x2 or 3x3
                    size = input('There are no solutions for a board of size '
                                 '2 or 3. Please enter another integer between 1 and '
                                 '26:\n>>>')
                else:
                    is_valid = True


def main():
    pass


main()
