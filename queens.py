import os
import string
import time


ALPHABET = list(string.ascii_lowercase)
# Time in milliseconds to sleep between renders in mode 3
SPEEDS = {'1': 1, '2': 60, '3': 200, '4': 800, '5': 1500}


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

    def find_all(self, mode=1, depth=1, states=None) -> list:
        """Recursively find and return list of all board states to render.

        Depending on the mode, self.state will be added to the
        boards list at different stages of the search process so
        they can be displayed accordingly after being returned.

        If there are valid moves when depth==self.size-1, this
        is a solution because a queen has been successfully
        placed on every rank.  There is no need to update the
        board if this is the case.
        """

        # Initialize states list at first method call
        if states is None:
            states = []

        # All ranks before current rank should be filled
        assert all([i != -1 if len(self.state[0:depth - 1]) != 0 else True for i in self.state[0:depth - 1]]), \
            'previous state ranks do not contain queen: {}'.format(self.state)

        # Depth is 1-indexed, while rank should be 0-indexed
        rank = depth - 1

        # For all files on the current rank where it's possible, place a
        # queen there, call try_all() with depth+1, undo queen placement
        possible_moves = Board.valid_moves(self.state, rank)
        for file in possible_moves:
            # Place the queen here
            self.update_board(rank, file)

            if depth < self.size:
                # Add intermediate states (non-solutions) for modes 3 and 4
                if mode in [3, 4]:
                    states += [self.state.copy()]

                # If this is not the final depth, add results
                # from the next depth to the list
                states += self.find_all(mode, depth+1)
            else:
                # This is a solution, add it to states
                states += [self.state.copy()]

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
    def render_board(state, msg=''):
        """Print current state of the board.

        Optional argument msg is printed to the right of the board
        in line with the top rank (i.e. the first rank printed).
        """

        size = len(state)
        assert size <= 26

        # Print top edge of the board
        print('    ┌───' + '┬───' * (size-1) + '┐')

        # Print body of the board
        # (Loop through ranks in self.state backwards
        # so rank 0 is displayed at bottom)
        for rank in range(size-1, -1, -1):
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
            print('│', end='')

            # Print msg on first printed rank
            if rank == size-1 and msg != '':
                print('    {}'.format(msg))
            else:
                print()

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

    @staticmethod
    def render_mode(states, mode, sleep_time=100, flush=False):
        """Render the boards in states appropriately for the given mode.

        Optional arg sleep_time is milliseconds to sleep between
                renders for mode 3.
        Optional arg flush clears the terminal between renders
                for modes 2, 3, and 4.
        """

        if mode == 1:
            # Print all solutions immediately
            i = 0
            solution = 1
            while i < len(states):
                msg = 'Found solution {}!'.format(solution)
                Board.render_board(states[i], msg)
                print()
                solution += 1
                i += 1
        elif mode == 2:
            # Print only the solutions, pause at each
            i = 0
            solution = 1
            while i < len(states):
                if flush:
                    # Clear the terminal
                    os.system('cls||clear')

                msg = 'Found solution {}! Press enter to continue.'.format(solution)
                Board.render_board(states[i], msg)
                input()
                solution += 1
                i += 1
        elif mode == 3:
            # Print intermediate states, pause at solutions
            i = 0
            solution = 1
            while i < len(states):
                if flush:
                    # Clear the terminal
                    os.system('cls||clear')

                if -1 not in states[i]:
                    # No -1 means states[i] has no empty ranks and is solution
                    msg = 'Found solution {}! Press enter to continue.'.format(solution)
                    Board.render_board(states[i], msg)
                    input()
                    solution += 1
                else:
                    # States[i] is not a solution
                    Board.render_board(states[i])

                i += 1
                time.sleep(millis_to_seconds(sleep_time))
        elif mode == 4:
            # Print and pause at all intermediate states and solutions
            i = 0
            solution = 1
            while i < len(states):
                if flush:
                    # Clear the terminal
                    os.system('cls||clear')

                if -1 not in states[i]:
                    # No -1 means states[i] has no empty ranks and is solution
                    msg = 'Found solution {}! Press enter to continue.'.format(solution)
                    Board.render_board(states[i], msg)
                    input()
                    solution += 1
                else:
                    Board.render_board(states[i])
                    input()

                i += 1
        else:
            raise ValueError('render_mode() called with invalid mode: {}'.format(mode))


def prompt_for_size():
    """Prompt for and return size of the board."""

    size = input('Enter board size:\n>>> ')

    # Validate input while size entered is invalid
    while size not in (str(i) for i in range(26)) or size in ('2', '3'):
        if size in ('2', '3'):
            # No solutions exist for 2x2 or 3x3 boards
            size = input('There are no solutions for a board of size '
                         '2 or 3. Please enter another integer between 1 and '
                         '26:\n>>> ')
        else:
            # Size of board out of range
            size = input('Please enter an integer between 1 and 26:\n>>> ')

    return int(size)


def prompt_for_mode():
    """Prompt for and return display mode."""

    print('Choose from a mode below: ')
    print('\t1: Show all solutions immediately')
    print('\t2: Pause at each solution')
    print('\t3: Visual execution - cycle queen placements and '
          'pause at solutions')
    print('\t4: Step-by-step - pause at every queen placement')
    mode = input('>>> ')

    # Validate input
    while mode not in ('1', '2', '3', '4'):
        mode = input('Please enter 1, 2, 3, or 4:\n>>> ')

    return int(mode)


def prompt_for_sleep_time():
    """Prompt for and return delay between renders in mode 3."""

    print('Choose a speed below: ')
    print('\t1: Lightning')
    print('\t2: Fast')
    print('\t3: Normal')
    print('\t4: Slow')
    print('\t5: Turtle')
    speed = input('>>> ')

    # Validate input
    while speed not in ('1', '2', '3', '4', '5'):
        speed = input('Please enter 1, 2, 3, 4, or 5:\n>>> ')

    return SPEEDS[speed]


def millis_to_seconds(millis):
    """Convert seconds to milliseconds"""

    return millis / 1000


def main():
    size = prompt_for_size()
    print()
    mode = prompt_for_mode()
    print()
    sleep_time = SPEEDS['3']
    if mode == 3:
        sleep_time = prompt_for_sleep_time()
        print()

    # Create the board and find solutions and/or intermediate states
    board = Board(size)
    states = board.find_all(mode)

    Board.render_mode(states, mode, sleep_time, True)
    print('\n\nAll {} solutions were found.'.format(len(states)))


if __name__ == '__main__':
    main()
