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

- **Maze win-check:**

```python
if player_pos == destination_pos:
    print("You win!")
```

- **Connect4 win-detection:**

```python
def check_win(board, player):
    # Check horizontal, vertical, and diagonal for a win
    ...
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
