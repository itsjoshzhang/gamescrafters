import numpy as np

M,N,K = 3, 3, 3         # position = 9-item tuple of X, O
POSTS = range(M * N)    # empty tiles and not_prim = None
X, O  = 1, 0            # move = tuple (BOARD_index, X/O)
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

    rows = [post[i * N: (i + 1) * N] for i in range(M)]
    cols = [post[i::N] for i in range(N)]
    
    diags = []
    for d in range(-(M - 1), N):

        # Main diagonal from top left to bottom right
        main  = range(max(0, -d), min(M, N - d))
        diag1 = [post[i * N + (i + d)] for i in main]
        
        # Anti diagonal from top right to bottom left
        anti = range(max(0, d), min(M, M + d))
        diag2 = [post[i*N + (N-1-i-d)] for i in anti]

        if len(diag1) >= K:
            diags.append(diag1)
        if len(diag2) >= K:
            diags.append(diag2)

    group = rows + cols + diags
    if any(has_end(line) for line in group):
        return "lose"
    elif None not in post:
        return "tie"
    
def canonical(post):
    grid = np.array(post).reshape(M, N)
    
    transforms = [
        lambda p: p,                        # Identity
        lambda p: np.rot90(p, 2),           # Rotate 180°
        lambda p: np.flipud(p),             # Reflect (x)
        lambda p: np.flipud(np.rot90(p, 2)) # 180°, reflect
    ]
    if M == N:
        transforms += [
            lambda p: np.rot90(p),              # Rotate 90°
            lambda p: np.rot90(p, 3),           # Rotate 270°
            lambda p: np.flipud(np.rot90(p)),   # 90°, reflect
            lambda p: np.flipud(np.rot90(p, 3)) # 270°, reflect
        ]
    for func in transforms:
        t_post = tuple(func(grid).flatten())
        if t_post in canon:
            return t_post
        
    canon.add(post)
    return post