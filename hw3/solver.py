import tictactoe as g
from collections import defaultdict as d

REMOVE_SYM = True
solns = {} # Dictionary. Keys: position <post>
# Values: Tuple (string <value>, int <remote>)

def solve(post):
    def remote(children, value):
        
        match value:
            case "lose": func = max
            case "win": func = min
            case "tie": func = min

        filter = [c for c in children if c[0] == value]
        return 1 + func(filter, key = lambda c: c[1])[1]
    
    if REMOVE_SYM:
        post = g.canonical(post)
    if post in solns:
        return solns[post]
    
    value = g.primitive_value(post)
    if value:
        solns[post] = (value, 0)
        return (value, 0)

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
dict = d(lambda: {"win": 0, "lose": 0, "tie": 0})

for value, remote in data:
    dict[remote][value] += 1

sort = sorted(dict.items(), key = lambda x: x[0], reverse=True)
sums = {"win": 0, "lose": 0, "tie": 0, "total": 0}

print(f"remote win  lose tie  total")
for r, v in sort:
    total = sum(v.values())
    print(f"{r:<6} {v["win"]:<4} {v["lose"]:<4} {v["tie"]:<4} {total}")
    
    for key in sums.keys():
        if key == "total":
            sums[key] += total
        else:
            sums[key] += v[key]
print(f"\n{"total"}  {sums["win"]:<4} {sums["lose"]:<4} {sums["tie"]:<4} {sums["total"]}")