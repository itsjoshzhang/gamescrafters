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
    child_posts = [g.do_move(post, m) for m in moves]
    child_solns = [solve(c) for c in child_posts]

    if "lose" in child_solns:
        solns[post] = "win"
    elif "tie" in child_solns:
        solns[post] = "tie"
    else:
        solns[post] = "lose"
    return solns[post]

solve(tuple(None for _ in g.POSTS))
win, tie, lose = 0, 0, 0

for value in solns.values():
    match value:
        case "lose": lose += 1
        case "win": win += 1
        case "tie": tie += 1

print(f"lose: {lose} \nwin: {win} \ntie: {tie} \ntotal: {len(solns)}")