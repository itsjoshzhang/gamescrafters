import tictactoe as g

REMOVE_SYM = True
solns = {} # Dictionary. Keys: position <post>
# Values: Tuple (string <value>, int <remote>)

def solve(post):
    def remote(c_solns, value):
        
        match value:
            case "lose": func = min
            case "win": func = max
            case "tie": func = min

        filter = [c for c in c_solns if c[0] == value]
        return 1 + func(filter, key = lambda c: c[1])[1]
    
    if REMOVE_SYM:
        post = g.canonical(post)
    if post in solns:
        return solns[post]
    
    value = g.primitive_value(post)
    if value:
        solns[post] = (value, 0)
        return solns[post]

    moves = g.generate_moves(post)
    c_posts = [g.do_move(post, m) for m in moves]

    c_solns = [solve(p) for p in c_posts]
    c_value = [s[0] for s in c_solns]

    if "lose" in c_value:
        solns[post] = ("win", remote(c_solns, "lose"))
    elif "tie" in c_value:
        solns[post] = ("tie", remote(c_solns, "tie"))
    else:
        solns[post] = ("lose", remote(c_solns, "win"))
    return solns[post]

# PRINT ANALYSIS
if g.__name__ == "tictactoe":
    solve(tuple(None for _ in g.POSTS))
else:
    solve(10) # g is 10-to-0-by-1-or-2

data = list(solns.values())
keys = {"win": 0, "lose": 0, "tie": 0}
dist = {}

for value, remote in data:
    if remote not in dist:
        dist[remote] = keys.copy()
    dist[remote][value] += 1

sort = sorted(dist.items(), key = lambda x: x[0], reverse=True)
sums = {**keys, "total": 0}
print(f"remote wins loss ties total")

for remote, value in sort:
    total = sum(value.values())
    print(f"{remote:<6} {value["win"]:<4} {value["lose"]:<4} {value["tie"]:<4} {total}")
    
    for key in keys:
        sums[key] += value[key]
    sums["total"] += total

print(f"\n{"total"}  {sums["win"]:<4} {sums["lose"]:<4} {sums["tie"]:<4} {sums["total"]}")