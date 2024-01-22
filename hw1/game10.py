# 10-to-0-by-1-or-2.py

POSTS = range(0, 11) # all legal positions
MOVES = [1, 2]       # all the legal moves

def is_primitive(post):
    return post == POSTS[0]

# Generates a (number) graph of all positions and their children
    # position: number corresponds to its index in the graph
    # children: list of all positions after legal move taken
GRAPH = [[post-move for move in MOVES if post-move in POSTS] for post in POSTS]
    
def do_move(post, move):
    """
    DoMove(position, move) → new_position
        Function: returns a new position (new_position), the result of making the move from the position
        Requires: position is not a primitive position, and move is a legal move from position.
        Example: DoMove(“9 pennies”, “take one penny”) → “8 pennies”
    """
    if is_primitive(post):
        raise ValueError(f"Position {post} is primitive.")
    if post - move not in GRAPH[post]:
        raise ValueError(f"{move} is an illegal move.")
    return post - move

def generate_moves(post):
    """
    GenerateMoves(position) → set of moves
        Function: returns the set of moves available from the position
        Requires: position is not a primitive position
        Example: GenerateMoves(“9 pennies”) → set of (“take one penny”, “take two pennies”)
        Example: GenerateMoves(“1 penny”) → set of (“take one penny”)
    """
    if is_primitive(post):
        raise ValueError(f"Position {post} is primitive.")
    return [post - child for child in GRAPH[post]]

def primitive_value(post):
    """
    PrimitiveValue(position) → { win, tie, lose, not_primitive } // For the person whose turn it is!
        Function: If the position is primitive, then based on the “to win/lose/tie” conditions, return its value (win, lose, or tie). If the position is not primitive, return not_primitive
        Example: PrimitiveValue(“1 penny”) → not_primitive
        Example: PrimitiveValue(“no pennies”) → lose // If you can't move, you lose
    """
    return "lose" if is_primitive(post) else None

def test_cases():
    print("Printing GRAPH:")
    [print(f"{post}: {GRAPH[post]}") for post in POSTS]

    print("Testing do_move(position, 1):")
    [print(f"{post}: {do_move(post, 1)}") for post in POSTS[1:]]

    print("Testing generate_moves():")
    [print(f"{post}: {generate_moves(post)}")  for post in POSTS[1:]]
    
    print("Testing primitive_value():")
    [print(f"{post}: {primitive_value(post)}") for post in POSTS]
