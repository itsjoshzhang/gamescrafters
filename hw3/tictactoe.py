import numpy as np

POSTS = (0, 1, 2,   # position = 9 item tuple of X, O
         3, 4, 5,   # empty tiles and not_prim = None
         6, 7, 8)   # move = tuple (POSTS index, X/O)
X, O  = 1, 0
canon = set()

def do_move(post, move):
    if primitive_value(post):
        raise ValueError(f"Position {post} is primitive.")
    
    if move not in generate_moves(post):
        raise ValueError(f"{move} is an illegal move.")
    
    post_l = list(post)
    post_l[move[0]] = move[1]
    return tuple(post_l)

def generate_moves(post):
    if primitive_value(post):
        raise ValueError(f"Position {post} is primitive.")

    # X is next when board is empty or balanced, else O
    next_p = X if post.count(X) == post.count(O) else O

    return [(p, next_p) for p in POSTS if post[p] == None]

def primitive_value(post):
    has_end = lambda l: l.count(X) == 3 or l.count(O) == 3

    nest = [post[:3],   post[3:6],  post[6:],   # rows
            post[0::3], post[1::3], post[2::3], # cols
            post[0::4], post[2:7:2]]            # diag

    if any(has_end(line) for line in nest):
        return "lose"
    elif None not in post:
        return "tie"
    
def canonical(post):
    grid = np.array(post).reshape(3, 3)
    
    transforms = [
        lambda p: p,                         # Identity
        lambda p: np.rot90(p),               # Rotate 90°
        lambda p: np.rot90(p, 2),            # Rotate 180°
        lambda p: np.rot90(p, 3),            # Rotate 270°
        lambda p: np.flipud(p),              # Reflect (x)
        lambda p: np.flipud(np.rot90(p)),    # 90°, reflect
        lambda p: np.flipud(np.rot90(p, 2)), # 180°, reflect
        lambda p: np.flipud(np.rot90(p, 3)), # 270°, reflect
    ]
    for func in transforms:
        t_post = tuple(func(grid).flatten())
        if t_post in canon:
            return t_post
        
    canon.add(post)
    return post