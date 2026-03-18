from collections import deque

def bfs_solve(grid):
    rows, cols = len(grid), len(grid[0])
    start, end = None, None

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)

    queue = deque([(start, 0)])
    visited = set([start])

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue:
        (r, c), dist = queue.popleft()

        if (r, c) == end:
            return True, dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                grid[nr][nc] != '#' and (nr, nc) not in visited):

                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))

    return False, -1