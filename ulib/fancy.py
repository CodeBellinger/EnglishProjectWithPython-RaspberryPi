x, y, i = 0, 0, 0
hilbert_a = [[0,0]]
def hilbert(l):
    def hilbert_curve(level, dx, dy):
        global x, y, i, hilbert_a
        if level == 0:
            return  # Base case: stop recursion when level reaches 0

        # First recursive call: rotate -90 degrees
        hilbert_curve(level - 1, dy, dx)

        # Move right (or in the current direction) and store coordinates
        x += dx
        y += dy
        hilbert_a.append([x, y])
        i += 1

        # Second recursive call: move in the current direction
        hilbert_curve(level - 1, dx, dy)

        # Move up and store coordinates
        x += dy
        y += dx
        hilbert_a.append([x, y])
        i += 1

        # Third recursive call: continue movement
        hilbert_curve(level - 1, dx, dy)

        # Move left (back) and store coordinates
        x -= dx
        y -= dy
        hilbert_a.append([x, y])
        i += 1

        # Fourth recursive call: rotate +90 degrees
        hilbert_curve(level - 1, -dy, -dx)

    hilbert_curve(4,1,0)

    return hilbert_a[0:l]