import game25 as g
solns = {}

def solve(post):
    if post in solns:
        return solns[post]
    
    prim = g.primitive_value(post)
    if prim: return prim

    moves = g.generate_moves(post)
    c_posts = [g.do_move(post, m) for m in moves]
    c_solns = [solve(p) for p in c_posts]

    solns[post] = "win" if "lose" in c_solns else "lose"
    return solns[post]
    
[print(f"{p}: {solve(p)}") for p in g.POSTS]