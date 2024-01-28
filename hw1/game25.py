POSTS = range(0, 26) # all legal positions
MOVES = (1, 3, 4)    # all the legal moves
    
def do_move(post, move):
    if primitive_value(post):
        raise ValueError(f"Position {post} is primitive.")
    
    if move not in generate_moves(post):
        raise ValueError(f"{move} is an illegal move.")
    return post - move

def generate_moves(post):
    if primitive_value(post):
        raise ValueError(f"Position {post} is primitive.")
    return [m for m in MOVES if post - m in POSTS]

def primitive_value(post):
    return "lose" if post == POSTS[0] else None

def test_cases():
    print("Testing do_move(position, 1):")
    [print(f"{post}: {do_move(post, 1)}") for post in POSTS[1:]]

    print("Testing generate_moves():")
    [print(f"{post}: {generate_moves(post)}")  for post in POSTS[1:]]
    
    print("Testing primitive_value():")
    [print(f"{post}: {primitive_value(post)}") for post in POSTS]