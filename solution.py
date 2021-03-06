
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[index]+cols[index] for index in range(len(rows))], [rows[index]+cols[len(rows)-1-index] for index in range(len(rows))]]

unitlist = row_units + column_units + square_units + diagonal_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def find_naked_twins(values, unit):
    candidates = []
    n_twins = []
    for box in unit:
        if len(values[box]) == 2:
            if values[box] in candidates:
                n_twins.append(values[box])
                candidates.remove(values[box])
            else:
                candidates.append(values[box])
    return n_twins


def naked_twins_eliminate(values, unit, n_twins):
    # print('Values before: ' + str(values))
    digits_to_eliminate = ''.join(n_twins)
    # print('Digits to eliminate: '+digits_to_eliminate)
    for box in unit:
        if values[box] not in n_twins:  # don't change the naked twins
            for digit in digits_to_eliminate:
                values[box] = values[box].replace(digit, '')
    # print('Values after: '+ str(values))
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # raise NotImplementedError

    for unit in unitlist:
        n_twins = find_naked_twins(values, unit)
        values = naked_twins_eliminate(values, unit, n_twins)
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    # raise NotImplementedError

    for box_name in values:
        if len(values[box_name])==1:
            peers_of_box = peers[box_name]
            # print('Box: '+box_name+' Value: '+values[box_name])
            # print(peers_of_box)
            for peer_box_name in peers_of_box:
                old_string = values[peer_box_name]
                new_string = old_string.replace(values[box_name], "")
                values[peer_box_name] = new_string

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    # raise NotImplementedError

    for unit in unitlist:
        for digit in "123456789":
            digit_count = 0
            box_last_seen = ''
            for box in unit:
                if digit in values[box]:
                    digit_count = digit_count + 1
                    box_last_seen = box
            if digit_count == 1:
                values[box_last_seen] = digit

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    # raise NotImplementedError

    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # raise NotImplementedError

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    elif len([box for box in values.keys() if len(values[box]) == 1]) == 81:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    least_digits_box = ''
    for box in values:
        if len(values[box])==1:
            continue
        if len(values[box])==2:
            least_digits_box=box
            break
        if least_digits_box=='':
            least_digits_box=box
            continue
        if len(values[box])<len(values[least_digits_box]):
            least_digits_box=box
    for digit in values[least_digits_box]:
        new_sudoku = values.copy()
        new_sudoku[least_digits_box] = digit
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
