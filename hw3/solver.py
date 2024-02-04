import game10 as g

solns = {} # Dictionary. Keys: position <post>
# Values: Tuple (string <value>, int <remote>)

def solve(post):
    def remote(children, value):
        term, func = None, None
        
        match value:
            case "lose":
                term, func = "win", max
            case "win":
                term, func = "lose", min
            case "tie":
                term, func = "tie", min

        filter = [c for c in children if c[0] == term]
        return 1 + func(filter, key = lambda c: c[1])[1]

    if post in solns:
        return solns[post]
    
    value = g.primitive_value(post)
    if value:
        solns[post] = (value, 0)
        return (value, 0)

    moves = g.generate_moves(post)
    child_posts = [g.do_move(post, m) for m in moves]
    child_solns = [solve(c) for c in child_posts]
    c = child_solns

    if "lose" in c:
        solns[post] = ("win", remote(c, "lose"))
    elif "tie" in c:
        solns[post] = ("tie", remote(c, "tie"))
    else:
        solns[post] = ("lose", remote(c, "win"))
    return solns[post]

solve(10)
win, tie, lose = [0, 0], [0, 0], [0, 0]

for value in solns.values():
    match value[0]:
        case "lose":
            lose[0] += 1
            lose[1] += value[1]
        case "win":
            win[0] += 1
            win[1] += value[1]
        case "tie":
            tie[0] += 1
            tie[1] += value[1]

print(f"lose: {lose[0]} \nwin: {win[0]} \ntie: {tie[0]} \ntotal: {len(solns)}")