<!--
author:   Trung Hieu Nguyen, Jannik Gabriel, Josef Binye
email:    your@mail.org
version:  0.0.1
language: en
comment:  A student project report and presentation about programming classic games (Maze, Connect4) in Python, reflecting on challenges, learning, and fun insights.
-->
# Presentation

[![LiaScript](https://raw.githubusercontent.com/LiaScript/LiaScript/master/badges/course.svg)](https://liascript.github.io/course/?https://github.com/TUBAF-IUZ-LiaScript/STEM-English-1/blob/main/presentation_template.md)

1. Attention grabber
2. What will audience get out of watching/listening to you? Why should they?
3. What is the scope of your presentation (how much are you loading on to the audience)?
4. What was your inspiration? What were your initial ideas? Was there anything you tried but abandoned?
5. What background information, theory or technical details do your audience need to know to be able to understand your show/game?
6. Code (Product)
  - Big picture
  - Important code snippets
  - Bug examples
  - What did you already know (and from where do you know it) and what did you have to learn to complete the project?
7. Code (process)
  - How did you code? Vibe? GitHub?
8. The show/game. Demo and description
9. Conclusion
10. Reflection. What did we get from taking part in this challenge?
11. Final thought/take-home message

---

## 1. Attention grabber

> "Have you ever wondered why a simple game like Connect4 or Maze can make even experienced programmers scratch their heads?"

---

## 2. What will audience get out of watching/listening to you? Why should they?

- Insights into the reality of building classic games from scratch
- Lessons learned from real bugs and mistakes
- Fun facts about game logic, Python coding, and how small details can turn into big challenges
- A relatable journey through coding, debugging, and celebrating small victories

---

## 3. What is the scope of your presentation (how much are you loading on to the audience)?

- Brief introduction to the projects (Maze & Connect4 in Python)
- Key coding challenges and solutions
- Demo/highlight of the games
- Reflections and takeaways
- All in about 15 minutes!

---

## 4. What was your inspiration? What were your initial ideas? Was there anything you tried but abandoned?

- Inspired by childhood games and the challenge of recreating them in code
- Initial idea: make a simple, playable version—ended up adding features and facing unexpected bugs
- Tried various input methods (keyboard, remote client) and display modes (including emulators)
- Some ideas (like advanced AI or fancy graphics) were set aside to focus on core gameplay and stability

---

## 5. What background information, theory or technical details do your audience need to know to be able to understand your show/game?

- **Maze**: A grid where the player moves from start to finish, avoiding walls
- **Connect4**: Players alternate dropping pieces into a 7x6 board, trying to get four in a row
- Basic Python programming: using loops, conditionals, and lists
- Challenge of handling user input, grid-based logic, and visual feedback

---

## 6. Code (Product)

### Big picture

- Each game is structured around a main loop: input, update, draw
- Maze: tracks player position, checks collisions, redraws after every move
- Connect4: manages board state, checks for wins/draws after each turn

### Important code snippets

- **Maze win-check:**
  ```python
  if player_pos == destination_pos:
      print("You win!")