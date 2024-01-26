import game10 as g

solns = {}

def solve(post):
    """
    Solve(position) → { win, tie, lose }
        Function: returns the value of (position) based on exhaustively searching the tree. It will call DoMove, GenerateMoves, and PrimitiveValue as needed.
        Example: Solve(“10 pennies”) → win
        Example: Solve(“no pennies”) → lose
    """
    if post in solns:
        return solns[post]

    if g.is_primitive(post):
        return g.primitive_value(post)

    moves = g.generate_moves(post)
    child_posts = [g.do_move(post, move) for move in moves]
    child_solns = [solve(child) for child in child_posts]

    solns[post] = "win" if "lose" in child_solns else "lose"
    return solns[post]
    
[print(f"{post}: {solve(post)}") for post in g.POSTS]