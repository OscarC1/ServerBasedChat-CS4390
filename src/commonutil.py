def where(l, m):
    for e in l:
        if m(e):
            return e
    raise ValueError()
