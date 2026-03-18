from collections import deque

def bfs_next_step(grid, start, target):
    rows, cols = len(grid), len(grid[0])

    queue = deque([tuple(start)])
    visited = set([tuple(start)])
    parent = {}

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue:
        r, c = queue.popleft()

        if [r, c] == target:
            while parent.get((r, c)) != tuple(start):
                r, c = parent[(r, c)]
            return [r, c]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            # ❌ NO wrap-around
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != '#' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return start