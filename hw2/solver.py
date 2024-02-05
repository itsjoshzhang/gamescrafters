import tictactoe as g

solns = {}

def solve(post):
    if post in solns:
        return solns[post]
    
    value = g.primitive_value(post)
    if value:
        solns[post] = value
        return value

    moves = g.generate_moves(post)
    c_posts = [g.do_move(post, m) for m in moves]
    c_solns = [solve(p) for p in c_posts]

    if "lose" in c_solns:
        solns[post] = "win"
    elif "tie" in c_solns:
        solns[post] = "tie"
    else:
        solns[post] = "lose"
    return solns[post]

solve(tuple(None for _ in g.POSTS))
v = list(solns.values())

print(f"lose: {v.count("lose")} \nwin: {v.count("win")}")
print(f"tie: {v.count("tie")} \ntotal: {len(solns)}")