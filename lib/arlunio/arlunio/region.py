import arlunio.ast as ast


def intersect(r1, r2):
    return ast.Node.intersect(r1, r2)


def union(r1, r2):
    return ast.Node.union(r1, r2)
