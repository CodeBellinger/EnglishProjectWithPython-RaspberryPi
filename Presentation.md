<!--
author:   Trung Hieu Nguyen, Jannik Gabriel, Josef Binye
email:    your@mail.org
version:  0.0.2
language: en
comment:  A student project report and presentation about programming classic games (Maze, Connect4) in Python, reflecting on challenges, learning, and fun insights.
-->

# Presentation

![Monkey](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExb28wd3RldmI1cm02ZTBicnVjYWlrY2RibHl2OGp5ZDdpMnVqa2hxMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zOvBKUUEERdNm/giphy.gif)

[![LiaScript](https://raw.githubusercontent.com/LiaScript/LiaScript/master/badges/course.svg)](https://liascript.github.io/course/?https://github.com/CodeBellinger/ProjectForEnglishClass/blob/main/Presentation.md)

---

## 1. Attention Please

> "Have you ever wondered why simple games like PacMan, Tic-Tac-Toe, Connect4 or Maze can make even experienced programmers scratch their heads? Now imagine this with inexperienced programmers"

![LED GIF](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGE4OGk5b2l2YjhqamRjOTh1aGJnYWc0ZWd1NjYzNnphcWtyYTFoayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JIX9t2j0ZTN9S/giphy.gif)

---

## 2. Why should you listen to us?

![LED GIF](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDlha216NGNweWM1YTBrOGl4cXNzMmJiMmRpNTlnaW54cW14aDJveiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YcXkgqd7wfSrbc82Ya/giphy.gif)

- Real stories from our experience building classic games in Python.
- Practical lessons learned from bugs, design choices, and unexpected twists.
- How to turn simple ideas into working code—and keep going when things break.
- Useful programming strategies that apply to any project, not just games.
- The cautionary tale of using LLM's/AI without oversight

---

## 3. Scope of presentation

- We present the core journey
- Focus on the real coding, problem-solving, and debugging process.
- We don't cover advanced AI or graphics—just the most valuable, transferable lessons.
- The aim: give you practical takeaways for your own programming projects!

---

## 4. Inspiration, ideas

- Everybody knows how to play retro games
- Why maze, connect4, tic-tac-toe, PacMan?
- Tried and abandoned:

  - Animations (too complex)
  - Overly complex input methods.
  - Fancy AI (we realized a solid player-vs-player was challenging enough!).
  - Some display features that broke compatibility.

- The main insight: Simpler is often better—and finishing a game is harder than it looks!

---

## 5. Historic Facts and interesting tidbits

![Maze](Multimedia/maze-illustrations.jpeg)

- **Maze**:
  - Labyrinths have been around for at least 4,000 years, appearing in various cultures and religions.
  - Difference between Labyrinths and Mazes
    - Labyrinth(Unicursal): One path from Start- to Endpoint. No dead ends. Impossible to go wrong way
    - Maze(Multicursal): Many dead ends. Multiple paths to choose from
  - Mazes were created in the Renaissance for Entertainment purposes

---

![Connect4](Multimedia/connect4jpg.jpg)

- **Connect4**:
  - Recently created game but apparently Captain James Cook (British Navy Salesman) in the 18th Century

---

![TicTacToe](Multimedia/tictactoe.png)

- **TicTacToe**:
  - *Roman Empire:* The earliest ancestor was called "Terni Lapilli."
  - *19th Century:* The modern name "Tic-Tac-Toe" appeared.
  - *1952:* "OXO" became one of the first-ever graphical computer games.

---

![PacMan](Multimedia/PacMan.jpeg)

- **PacMan**:
  - 22. Mai 1980 as *Puck Man* by Namco
  - Designer: Toru Iwatani
  
---

## 6. Code (Product)

![UML Diagram](TicTacToe/UML-DiagramTicTacToe.jpg)

- Both games center around a main loop: get input → update state → draw board.
- **Maze**: Tracks player position, checks for collisions, redraws after each move.
- **Connect4**: Manages board state, alternates players, checks for wins or draws.
- **PacMan**: Checking which field the player wants to choose and check with a list ghosts and walls
- **TicTacToe**: Checks which fields are open vs. occupied. Win condition is checked (three of a kind in one line)

---

## Important code snippets

- **Generating Maze with recursive backtracker algorithm:**

```python
def generate_maze_recursive_backtracker():
    """
    Generates a maze using the Recursive Backtracker algorithm.
    The maze is represented by a grid of 0s (paths) and 1s (walls).
    Initializes a grid twice the size for walls, then carves paths.
    """
    global maze

    # Initialize the entire physical maze grid to all walls (1)
    maze = create_grid(HEIGHT, WIDTH, 1)

    # Grid for maze generation logic (e.g., 8x8 cells for a 16x16 display)
    logical_rows = (HEIGHT - 1) // 2
    logical_cols = (WIDTH - 1) // 2

    # Visited grid for the logical cells
    visited = create_grid(logical_rows, logical_cols, False)
    # Stack for DFS (Depth-First Search)
    stack = []

    # Choose a random starting cell for maze generation
    start_logical_r = random.randrange(logical_rows)
    start_logical_c = random.randrange(logical_cols)

    # Mark the starting logical cell as visited
    visited[start_logical_r][start_logical_c] = True
    stack.append((start_logical_r, start_logical_c))

    # Carve out the starting logical cell
    maze[start_logical_r * 2 + 1][start_logical_c * 2 + 1] = 0

    while stack:
        current_logical_r, current_logical_c = stack[-1] # Peek at the top cell

        # Define possible neighbors and the wall positions between them
        neighbors = []
        # Define logical moves (dr, dc) for neighbor
        possible_moves = [
            (-1, 0), # Up
            (1, 0),  # Down
            (0, -1), # Left
            (0, 1)  # Right
        ]

        # Find unvisited neighbors
        for dr, dc in possible_moves:
            next_logical_r, next_logical_c = current_logical_r + dr, current_logical_c + dc
            # Ensure wall is actually a wall before carving
            if (is_valid(next_logical_r, next_logical_c, logical_rows, logical_cols) and
               not visited[next_logical_r][next_logical_c]):
                # Store logical next and original dr,dc
                neighbors.append((next_logical_r, next_logical_c, dr, dc))

        if neighbors:
            # Pick a random unvisited neighbor
            (next_logical_r, next_logical_c, dr, dc) = random.choice(neighbors)

            # Carve a path to the chosen neighbor cell (physical coord)
            maze[next_logical_r * 2 + 1][next_logical_c * 2 + 1] = 0

            wall_r = current_logical_r * 2 + 1 + dr
            wall_c = current_logical_c * 2 + 1 + dc
            maze[wall_r][wall_c] = 0
            
            # Mark the new cell as visited and add to stack
            visited[next_logical_r][next_logical_c] = True
            stack.append((next_logical_r, next_logical_c))
        else:
            # No unvisited neighbors, backtrack
            stack.pop()
```

- **Connect4 win-detection:**

```python
def check_win(game_board, player):
    # Determine the color of the current player
    player_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR

    # Horizontale Überprüfung
    for r in range(HEIGHT):
        for c in range(WIDTH - 3):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r, unified_c2 = map_coordinates(r, c + 1)
            unified_r, unified_c3 = map_coordinates(r, c + 2)
            unified_r, unified_c4 = map_coordinates(r, c + 3)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r][unified_c2] == player_color and \
               game_board[unified_r][unified_c3] == player_color and \
               game_board[unified_r][unified_c4] == player_color:
                return True

    # Vertikale Überprüfung
    for c in range(WIDTH):
        for r in range(HEIGHT - 3):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r2, unified_c = map_coordinates(r + 1, c)
            unified_r3, unified_c = map_coordinates(r + 2, c)
            unified_r4, unified_c = map_coordinates(r + 3, c)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r2][unified_c] == player_color and \
               game_board[unified_r3][unified_c] == player_color and \
               game_board[unified_r4][unified_c] == player_color:
                return True

    # Negative Diagonale (von oben links nach unten rechts)
    for r in range(HEIGHT - 3):
        for c in range(WIDTH - 3):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r2, unified_c2 = map_coordinates(r + 1, c + 1)
            unified_r3, unified_c3 = map_coordinates(r + 2, c + 2)
            unified_r4, unified_c4 = map_coordinates(r + 3, c + 3)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r2][unified_c2] == player_color and \
               game_board[unified_r3][unified_c3] == player_color and \
               game_board[unified_r4][unified_c4] == player_color:
                return True

    # Positive Diagonale (von oben rechts nach unten links)
    for c in range(WIDTH - 3):
        for r in range(3, HEIGHT):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r5, unified_c2 = map_coordinates(r - 1, c + 1)
            unified_r6, unified_c3 = map_coordinates(r - 2, c + 2)
            unified_r7, unified_c4 = map_coordinates(r - 3, c + 3)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r5][unified_c2] == player_color and \
               game_board[unified_r6][unified_c3] == player_color and \
               game_board[unified_r7][unified_c4] == player_color:
                return True
    return False
```

- **Handle imput for TicTacToe**

```python
def handle_input(self, key: str):
        if not self.is_running:
            self.start_game()
            return

        if key in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            self.input_controller.move_cursor(key)
            self.field.draw_board_state(self.input_controller.get_cursor_position())

        elif key == Direction.CONFIRM:
            player = self.get_current_player()
            if self.input_controller.confirm_selection(self.field, player):
                if self.rules.check_win(self.field, player):
                    self.end_game(winner=player)
                elif self.rules.check_draw(self.field):
                    self.end_game(winner=None)
                else:
                    self.next_turn()
                    self.field.draw_board_state(self.input_controller.get_cursor_position())
```

---

## Bug examples

![Debugging](Multimedia/Debugging.jpeg)

- Off-by-one errors: sometimes the player "disappeared" at the edge of the grid!
- Remote input and keyboard sometimes desynchronized, causing missed moves.
- Display incompatibilities: `display.fade()` needed a compatibility wrapper for different environments.
- Mapping coordinates between display and emulator required a conversion layer (like `map_coordinates()`).
- TicTacToe: Cannot find library
- PacMan: Difficulties with the game logic

---

## What did you already know, and what did you have to learn?

- Knew: Basic Python, game rules, simple data structures.
- Learned:
  - How to handle tricky input and grid logic.
  - Debugging strategies for hard-to-find bugs.
  - Writing modular, reusable code (especially for display compatibility).
  - The importance of clear commit messages and version control!
  - Everything in python is basically an object
  - Some things are more difficult than it seems
  - Understanding the concept before writing code

---

## 7. Code (process)

- We worked iteratively: get a basic version running, then add enhancements.
- Used GitHub for version control: each commit documented bugs, features, and fixes.
- Our process:
    1. Plan the next feature or fix.
    2. Implement in small steps.
    3. Test and debug—sometimes for hours!
    4. Commit and repeat.
- Collaboration meant learning from each other's mistakes (and solutions).

---

## 8. The show/game. Demo and description

- **Maze**: Move the player with arrow keys or remote input, avoid obstacles, and reach the target.
- **Connect4**: Take turns dropping pieces, trying to outsmart your opponent (or yourself).
- **TicTacToe**: Player 1 vs. Player 2. Determining Move order and winner starts with first move
- **PacMan**: Choose between four fields and start playing

---

## 9. Conclusion

- Building "simple" games is surprisingly complex—but also really rewarding.
- The biggest lessons come from debugging and fixing persistent issues.
- Success is not just having a working game, but understanding how and why it works. End result not as important as process

---

## 10. Reflection

![Relationship between AI vs. You](Multimedia/AIvsYou.gif)

- Stronger Python coding skills and confidence in tackling new problems.
- A better sense of how to break big problems into manageable pieces.
- The satisfaction of turning an idea into a playable reality—and sharing it with others.
- Understanding how to wield AI-Tools to your advantage
  - Using it carelessly with do more harm than good
- Documentation is important for reviewing your code

---

## 11. Final thought/take-home message

![Summit](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExejE2cjRhNG5zMWNjZXJtd2ppNWJta3Ntanl4YjJ3bzJtdndwd2NncSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QXqf43mbeBbYFTy4jR/giphy.gif)

> "Programming is like solving a puzzle: sometimes you get stuck, but every piece you place brings you closer to the big picture. Keep going, and celebrate every win—even the small ones!"

- Never use LLM's/AI without oversight
- Always use version control
- Debugging is very important
- Be patient: The code will not work on the first try (except when you are a genius)
- Always read the docs

---
