import numpy as np

POSTS = (0, 1, 2,   # position = 9-item list of X & O
         3, 4, 5,   # empty tiles and not_prim = None
         6, 7, 8)   # move = tuple (BOARD_index, X/O)
X, O  = 1, 0
canon = []

def do_move(post, move):
    if primitive_value(post):
        raise ValueError(f"Position {post} is primitive.")
    
    if move not in generate_moves(post):
        raise ValueError(f"{move} is an illegal move.")
    
    post_l = list(post)
    post_l[move[0]] = move[1]
    return tuple(post_l)

def generate_moves(post):
    # X is next when board is empty or balanced, else O
    next_p = X if post.count(X) == post.count(O) else O

    if primitive_value(post):
        raise ValueError(f"Position {post} is primitive.")
    return [(p, next_p) for p in POSTS if post[p] == None]

def primitive_value(post):
    def has_ending(group):
        
        for list in group:
            if list.count(X) == 3 or list.count(O) == 3:
                return True
        return False

    nest = [[post[:3],   post[3:6],  post[6:]],     # rows
            [post[0::3], post[1::3], post[2::3]],   # cols
            [post[0::4], post[2:7:2]]]              # diag

    if any(has_ending(group) for group in nest):
        return "lose"
    elif None not in post:
        return "tie"
    
def canonical(post):
    grid = np.array(post).reshape(3, 3)
    
    transforms = [
        lambda x: x,                         # Identity
        lambda x: np.rot90(x),               # Rotate 90°
        lambda x: np.rot90(x, 2),            # Rotate 180°
        lambda x: np.rot90(x, 3),            # Rotate 270°
        lambda x: np.flipud(x),              # Reflect (x)
        lambda x: np.flipud(np.rot90(x)),    # 90°, reflect
        lambda x: np.flipud(np.rot90(x, 2)), # 180°, reflect
        lambda x: np.flipud(np.rot90(x, 3)), # 270°, reflect
    ]
    for func in transforms:
        t_post = tuple(func(grid).flatten())
        if t_post in canon:
            return t_post
        
    canon.append(post)
    return post