import tictactoe as g

solns = {}
def solve(post):

    if post in solns: return solns[post]
    prim = g.primitive_value(post)
    if prim:
        solns[post] = prim
        return prim

    moves = g.generate_moves(post)
    child_posts = [g.do_move(post, move) for move in moves]
    child_solns = [solve(child) for child in child_posts]

    if "lose" in child_solns:
        solns[post] = "win"
    elif "tie" in child_solns:
        solns[post] = "tie"
    else:
        solns[post] = "lose"
    return solns[post]

solve(tuple(None for _ in g.BOARD))
win, tie, lose = 0, 0, 0

for value in solns.values():
    match value:
        case "lose": lose += 1
        case "win": win += 1
        case "tie": tie += 1

print(f"lose: {lose} \nwin: {win} \ntie: {tie} \ntotal: {len(solns)}")