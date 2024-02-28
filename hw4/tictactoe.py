import numpy as np

M,N,K = 4, 3, 3         # position: len M*N tuple of X, O
POSTS = range(M * N)    # empty tiles and not_prim = None
X, O  = 1, 0            # move = tuple (POSTS index, X/O)
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
    def has_end(line):
        x, o = 0, 0

        for tile in line:
            if tile == X:   x, o = x + 1, 0
            elif tile == O: x, o = 0, o + 1
            else:           x, o = 0, 0
            if x >= K or o >= K:
                return True
        return False
    
    grid = np.array(post).reshape(M, N)

    for i in range(M):          # rows
        if has_end(grid[i, :]):
            return "lose"
    for j in range(N):          # cols
        if has_end(grid[:, j]):
            return "lose"

    for d in range(-M + K, N - K + 1):  # main diagonal
        if has_end(grid.diagonal(d)):
            return "lose"               # anti diagonal
        if has_end(np.fliplr(grid).diagonal(d)):
            return "lose"

    if None not in post:
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