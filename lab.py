"""6.009 Lab 5 -- Mines"""

def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]]})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    """
    lines = ["dimensions: {}".format(game["dimensions"]),
             "board: {}".format("\n       ".join(map(str, game["board"]))),
             "mask:  {}".format("\n       ".join(map(str, game["mask"])))]
    print("\n".join(lines))

def get_neighbors(board, loc):
    """Return list of valid neighbors

    Args:
        board (list): 2D array that contains all the bombs as "."
        loc (tuple): the coordinates of the current location

    Returns:
        list of valid neighbors

    >>> get_neighbors([['.', 0]], (0,1))
    [(0, 0)]
    """
    rows = len(board)
    cols = len(board[0])

    r = loc[0]
    c = loc[1]
    adjacent = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]
    neighbors = []

    for l in adjacent:
        if l[0] >= 0 and l[0] < rows and l[1] >= 0 and l[1] < cols:
            neighbors.append(l)

    return neighbors



def count_bombs(board, loc):
    """Return number of bombs around a specific location

    Args:
        board (list): 2D array that contains all the bombs as "."
        loc (tuple): the coordinates of the current location

    Returns:
        int of how many bombs are next to the location

    >>> count_bombs([['.', 1]], (0,1))
    1

    """

    count = 0

    for l in get_neighbors(board, loc):
        if board[l[0]][l[1]] == ".":
            count += 1
    return count

def new_game(num_rows, num_cols, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.

    Args:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]
    """
    dimensions = [num_rows, num_cols]

    mask = []
    for i in range(num_rows):
        temp = []
        for j in range(num_cols):
            temp.append(False)
        mask.append(temp)

    board = [ [ 0 for j in range(num_cols)] for i in range(num_rows)] 
    for bomb in bombs:
        board[bomb[0]][bomb[1]] = "."
    for i in range(num_rows):
        for j in range(num_cols):
            loc = (i,j)
            if board[i][j] != ".":
                board[i][j] = count_bombs(board, loc)

    return {'dimensions': dimensions, 'mask': mask, 'board': board}


def nd_get_neighbors(dims, loc):
    """Gets all valid neighbors of a location

    Args: 
        dims (list)
        loc (n-length tuple)

    Returns:
        list of neighbors

    >>> nd_get_neighbors([1,2], (0,1))
    [(0, 1), (0, 0)]
    """
    if len(loc) == 1:
        neighbors = []
        if loc[0] < dims[0] and loc[0] >= 0:
            neighbors.append((loc[0],))
        if loc[0]-1 < dims[0] and loc[0]-1 >= 0:
            neighbors.append((loc[0]-1,))
        if loc[0]+1 < dims[0] and loc[0]+1 >= 0:
            neighbors.append((loc[0]+1,))
    else:
        temp = nd_get_neighbors(dims[1:], loc[1:])
        neighbors = []
        if loc[0] < dims[0] and loc[0] >= 0:
            neighbors.extend([(loc[0],) + n for n in temp])
        if loc[0]-1 < dims[0] and loc[0]-1 >= 0:
            neighbors.extend([(loc[0]-1,) + n for n in temp])
        if loc[0]+1 < dims[0] and loc[0]+1 >= 0:
            neighbors.extend([(loc[0]+1,) + n for n in temp])
    return neighbors



def get_all_locs(dims):
    """Gets all location coordinates of a board

    Args: 
        dims (list of ints)

    Returns:
        list of locations (list of tuples)

    >>> get_all_locs([1,2])
    [(0, 0), (0, 1)]
    """
    if len(dims) == 1:
        return [(i,) for i in range(dims[0])]
    else:
        temp = get_all_locs(dims[1:])
        all = []
        for i in range(dims[0]):
            all.extend([(i,) + n for n in temp])
        return all


def set_value(board, loc, val):
    """Sets a value recursively to one location

    Args: 
        board (n-dimensional array) 
        loc (n-length tuple)
        val (char)

    Returns:
        copy of board with the val in the right spot and other values unchanged

    >>> set_value([['.', 0]], (0,1), 1)
    [['.', 1]]
    """
    result = board[:]
    if len(loc) == 1:
        result[loc[0]] = val
    else:
        i = loc[0]

        result[i] = set_value(board[i], loc[1:], val)
    return result

def get_value(board, loc):
    """Gets a value recursively of one location

    Args: 
        board (n-dimensional array) 
        loc (n-length tuple)

    Returns:
        value of the board at one location (char)

    >>> get_value([['.', 0]], (0,1))
    0
    """
    if len(loc) == 1:
        return board[loc[0]]
    else:
        i = loc[0]
        return get_value(board[i], loc[1:])
        
    
def nd_new_game(dims, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.  This is an N-dimensional version of new_game().

    Args:
       dims (list): Dimensions of the board
       bombs (list): bomb locations as a list of tuples, each an N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> dump(nd_new_game([2, 4, 2], [(0, 0, 1), (1, 0, 0), (1, 1, 1)]))
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, False], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    
    mask_temp = dims[::-1]

    n = mask_temp.pop()
    mask = [False] * n
    board = [0] * n
    while len(mask_temp) != 0:
        num = mask_temp.pop()
        mask = [mask] * num
        board = [board] * num

    for bomb in bombs:
        board = set_value(board, bomb, ".")
        for n in nd_get_neighbors(dims, bomb):
            if get_value(board, n) != ".":
                current = int(get_value(board, n))
                board = set_value(board, n, current+1)

    return {'dimensions': dims, 'board': board, 'mask': mask}



def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent to
    a bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    Args:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       Tuple[str,int]: A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 3)
    ('victory', 4)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 0)
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    """
    if game['mask'][row][col] == True:
        count = 0
    else:
        game['mask'][row][col] = True
        count = 1

    if game['board'][row][col] == 0:
        for loc in get_neighbors(game['board'], (row, col)):
            if game['mask'][loc[0]][loc[1]] == False:
                count += dig(game, loc[0], loc[1])[1]

    elif game['board'][row][col] == ".":
        return ("defeat", count)


    num_rows = game['dimensions'][0]
    num_cols = game['dimensions'][1]
    for i in range(num_rows):
        for j in range(num_cols):
            if game['board'][i][j] != "." and game['mask'][i][j] == False:
                return ("ongoing", count)

    return ("victory", count)



def nd_dig(game, coords):
    """Recursively dig up square at coords and neighboring squares.

    Update game["mask"] to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    This is an N-dimensional version of dig().

    Args:
       game (dict): Game state
       coords (tuple): Where to start digging

    Returns:
       A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 3, 0))
    ('ongoing', 8)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, True], [True, True], [True, True]]
           [[False, False], [False, False], [True, True], [True, True]]

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 0, 1))
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, True], [False, True], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    mask = game['mask']
    board = game['board']

    if get_value(mask, coords) == True:
        count = 0
    else:
        game['mask'] = set_value(mask, coords, True)
        count = 1

    if get_value(board, coords) == 0:
        for loc in nd_get_neighbors(game['dimensions'], coords):
            if get_value(mask, loc) == False:
                count += nd_dig(game, loc)[1]

    elif get_value(board, coords) == ".":
        return ("defeat", count)


    for loc in get_all_locs(game['dimensions']):
            if get_value(board, loc) != "." and get_value(mask, loc) == False:
                return ("ongoing", count)

    return ("victory", count)
            
                

def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'],
     ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '],
     ['.', '.', '1', ' ']]
    """
    mask = game['mask']
    board = game['board']
    num_rows = game['dimensions'][0]
    num_cols = game['dimensions'][1]
    render = [ [ 0 for j in range(num_cols)] for i in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_cols):

            if mask[i][j] == True or xray == True:
                if board[i][j] == 0:
                    render[i][j] = " "
                else:
                    render[i][j] = str(board[i][j])
            else:
                render[i][j] = "_"

    return render



def nd_render(game, xray=False):
    """Prepare a game for display.

    Returns an N-dimensional array (nested lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    This is an N-dimensional version of render().

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       An n-dimensional array (nested lists)

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
    ...                     [[False, False], [False, False], [True, True], [True, True]]]},
    ...           False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                     [[False, False], [False, False], [False, False], [False, False]]]},
    ...           True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    mask = game['mask']
    board = game['board']
    dims = game['dimensions']

    render = board[:]
    
    for loc in get_all_locs(dims):
        if get_value(mask, loc) == True or xray == True:
            if get_value(board, loc) == 0:
                render = set_value(render, loc, " ")
            else:
                render = set_value(render, loc, str(get_value(board, loc)))
        else:
            render = set_value(render, loc, "_")

    return render



def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    template = render(game, xray)
    answer = ""
    for row in template:
        line = ""
        for char in row:
            line += char
        line += "\n"
        answer += line

    return answer[:len(answer)-1]

    

