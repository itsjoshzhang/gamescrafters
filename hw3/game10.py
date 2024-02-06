POSTS = range(0, 11) # all legal positions
MOVES = (1, 2)       # all the legal moves
    
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

def canonical(post): return post