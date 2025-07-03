<!--
author:   Trung Hieu Nguyen, Jannik Gabriel, Josef Binye
email:    your@mail.org
version:  0.0.2
language: en
comment:  A student project report and presentation about programming classic games (Maze, Connect4) in Python, reflecting on challenges, learning, and fun insights.
-->

# Blabla

[![LiaScript](https://raw.githubusercontent.com/LiaScript/LiaScript/master/badges/course.svg)](https://liascript.github.io/course/?https://github.com/CodeBellinger/ProjectForEnglishClass/blob/main/Presentation.md)

---

## 1. Attention grabber

> "Have you ever wondered why a simple game like Connect4 or Maze can make even experienced programmers scratch their heads?"

---

## 2. What will audience get out of watching/listening to you? Why should they?

- Real stories from our experience building classic games in Python.
- Practical lessons learned from bugs, design choices, and unexpected twists.
- How to turn simple ideas into working code—and keep going when things break.
- Useful programming strategies that apply to any project, not just games.

---

## 3. What is the scope of your presentation?

- We present the core journey: from idea to playable Maze and Connect4.
- Focus on the real coding, problem-solving, and debugging process.
- We don't cover advanced AI or graphics—just the most valuable, transferable lessons.
- The aim: give you practical takeaways for your own programming projects!

---

## 4. What was your inspiration? What were your initial ideas? Was there anything you tried but abandoned?

- We chose Maze and Connect4 because they're classic, fun, and deceptively tricky to implement.
- Initial plan: make the basic game logic work, then add features like remote input and nicer visuals.
- Tried and abandoned:
  - Overly complex input methods.
  - Fancy AI (we realized a solid player-vs-player was challenging enough!).
  - Some display features that broke compatibility.
- The main insight: Simpler is often better—and finishing a game is harder than it looks!

---

## 5. What background information, theory or technical details do your audience need to know to be able to understand your show/game?

- **Maze**: Guide a player through a grid avoiding walls to reach the goal.
- **Connect4**: Two players drop pieces into a 7x6 board, aiming for four in a row (horizontal, vertical, diagonal).
- Both games:
  - Use grid logic and turn-based mechanics.
  - Require robust handling of user input and clear win/draw detection.
- You'll see Python concepts like loops, lists, and function calls in action.

---

## 6. Code (Product)

## Big picture

- Both games center around a main loop: get input → update state → draw board.
- **Maze**: Tracks player position, checks for collisions, redraws after each move.
- **Connect4**: Manages board state, alternates players, checks for wins or draws.

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

- Off-by-one errors: sometimes the player "disappeared" at the edge of the grid!
- Remote input and keyboard sometimes desynchronized, causing missed moves.
- Display incompatibilities: `display.fade()` needed a compatibility wrapper for different environments.
- Mapping coordinates between display and emulator required a conversion layer (like `map_coordinates()`).

---

## What did you already know, and what did you have to learn?

- Knew: Basic Python, game rules, simple data structures.
- Learned:
  - How to handle tricky input and grid logic.
  - Debugging strategies for hard-to-find bugs.
  - Writing modular, reusable code (especially for display compatibility).
  - The importance of clear commit messages and version control!

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
- The demo highlights:
  - Real-time board updates.
  - Clear win/loss messages.
  - How the code responds to user actions and edge cases.

---

## 9. Conclusion

- Building "simple" games is surprisingly complex—but also really rewarding.
- The biggest lessons come from debugging and fixing persistent issues.
- Success is not just having a working game, but understanding how and why it works.

---

## 10. Reflection. What did we get from taking part in this challenge?

- Stronger Python coding skills and confidence in tackling new problems.
- A better sense of how to break big problems into manageable pieces.
- The satisfaction of turning an idea into a playable reality—and sharing it with others.

---

## 11. Final thought/take-home message

> "Programming is like solving a puzzle: sometimes you get stuck, but every piece you place brings you closer to the big picture. Keep going, and celebrate every win—even the small ones!"

---
