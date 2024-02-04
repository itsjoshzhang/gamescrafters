import game25 as g
solns = {}

def solve(post):
    if post in solns:
        return solns[post]
    
    prim = g.primitive_value(post)
    if prim: return prim

    moves = g.generate_moves(post)
    child_posts = [g.do_move(post, m) for m in moves]
    child_solns = [solve(c) for c in child_posts]

    solns[post] = "win" if "lose" in child_solns else "lose"
    return solns[post]
    
[print(f"{p}: {solve(p)}") for p in g.POSTS]