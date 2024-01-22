# x-to-0-solver.py

import game25 as g

def solve(post):
    """
    Solve(position) → { win, tie, lose }
        Function: returns the value of (position) based on exhaustively searching the tree. It will call DoMove, GenerateMoves, and PrimitiveValue as needed.
        Example: Solve(“10 pennies”) → win
        Example: Solve(“no pennies”) → lose
    """
    if g.is_primitive(post):
        return g.primitive_value(post)

    moves = g.generate_moves(post)

    child_posts = [g.do_move(post, move) for move in moves]
    child_values = [solve(child) for child in child_posts]

    return "win" if "lose" in child_values else "lose"
    
[print(f"{post}: {solve(post)}") for post in g.POSTS]