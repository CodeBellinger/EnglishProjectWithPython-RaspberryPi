# Document for Project

## Review of project

### Introduction

This project was created to help us learn Python and teamwork by making simple games on the Raspberry Pi. At the start of the semester I did not know how much this project would actually help me discover some intricacies of coding like debugging and finding a solution. I didn't think much of it and thought I could just cruise through this course semester not realizing how challenging this project would be.

The main goal was to use easy-to-understand logic and code to build games that are fun and let us practice programming. My first idea was actually to create beautiful animations like a crashing wave or a pulsating spiral not realizing how difficult this would be to convert this idea to code. My main responsibility was to work on two games: maze.py and connect4.py. These games were chosen because they are classic, easy to explain, and show how programming can be used to make interactive software. But honestly talking with my team members and members of the other groups I almost saw no other project that I could implement with the lack of python skills and I ultimately gave up the idea of creating a beautiful animation in order to create something that would just work (Unfortunately it was not meant to be). Considering this was my first real coding project it was a steep learning curve. But a rewarding time for sure.

### Stages of project

#### Planning

At the beginning, we talked as a team about what we wanted to build. Maze and Connect4 were my choices in the end because talking with my peers made me realize creating seemingly easy logic games like Maze and Connect4 involved some interesting logic that was not obvious at first glance. For maze.py, I planned to make a simple maze that can be solved by moving the player with arrow keys or buttons. I wanted the game to check for walls and let the player know when they reach the finish. Maze had actually quite tricky algorithms to implement like a longest_path_algorithm, creating dead ends and so on.

For connect4.py, my plan was to create a board that lets two players take turns. I needed to think about how players drop pieces, how the grid works, and how to check who wins. I wrote down the main features, thought about how the game should look and how to implement some features like a firework with the color of the winner. This planning helped me break the big task into smaller steps.

#### Coding

For maze.py, I started by designing the maze layout as a list of lists, with numbers showing walls and open paths. I wrote code to draw the maze and move the player. I used input functions to let the player move up, down, left, or right. I added checks so the player could not go through walls. I also made the game show a message when the player reached the exit.

In connect4.py, I made a grid for the board and wrote code so players could drop pieces into columns. I had to use loops and conditionals to switch turns and check if a column was full. The biggest challenge was checking for a winner, so I wrote functions to look for four pieces in a row, in all directions (horizontal, vertical, diagonal). I added messages to tell the players who won or if the game was a draw. During coding, I used comments to explain my code and tried to keep it simple.

#### Testing

After I finished the first version of each game, I tested them by playing several rounds. In maze.py, I checked if the player could move smoothly and if the walls blocked movement correctly. I found a bug where the player could sometimes go through a wall, so I fixed the movement logic. I also tested the win condition to make sure the game ended at the right time.

For connect4.py, testing meant playing as both players, trying different ways to win and draw. I found some mistakes in how the winner was checked, especially for diagonal wins. I fixed the code by testing each direction carefully.

#### Improving

After testing, I worked on making both games better. For maze.py, I made the maze harder by adding more walls and making the path less direct. I improved the way messages were shown and cleaned up the code so it was easier to read. I also added more comments and made sure the controls were easy to use.

In connect4.py, I improved the way the board looked so it was clearer whose turn it was. I added checks to stop players from dropping pieces into a full column. I made the win-checking code faster and easier to understand. I also added instructions at the start, so new players could learn the game quickly. These improvements made the games more fun and easier for others to use.

With the imput of my team members I wrote the presentation and managed the Github Repository.

### Summary

#### Reflection

The more time I spend coding this project the more I realized how dangerous it is to just let an LLM write some code for you without completely understand what the code will do to the code base. The first problem actually getting settled with Visual Studio Code and Python Notebook, learning on the fly and just trying to set everything up and learning Python Syntax. The longer the project the went the more I understood what I needed to do but at the same time since it took me so long to just get accustomed to Python and Python Notebook I was lacking behind and I rushed just to get the program to run on the LED-Box

##### Challenges and solutions

One big challenge in maze.py was making sure the player could not move through walls. Sometimes, my code did not check the wall positions correctly, so the player could "jump" into a wall. I solved this by checking the position every time before moving and by testing different maze layouts.

In connect4.py, the hardest part was checking for a winner in all directions. My first code only checked left to right, but missed vertical and diagonal wins. I had to write extra functions to look in every direction and test them with different board setups. This process taught me how important it is to test all parts of the code and not just the easy ones.

##### Skills

One thing I realized when doing this project was the passion that I have for programming and the perseverance when things don't work. Programming can be frustrating especially when you see that other groups are so far ahead and you just try to keep up. I also gained valuable knowledge reading documentation, technical english and learning about the technical side of programming like structuring your code, documenting everything so I understand the code and using version control like Github and Git that is invaluable for every programmer. One thing that I know understand is that you have to very precise with LLM's: You can't give it a simple command and expect it to understand you completely.

### Conclusion

Working on maze.py and connect4.py taught me a lot about coding. The project showed me that even simple games can have tricky problems. I am proud of what I made and want to keep learning more about Python and programming in the future. Even though it was frustrating to see that the code was not working when it mattered even though it worked on the emulator it was actually a very valuable time for me where I could hone my skills programming, planning and thinking creatively about a project. It was stressful and challenging but it was also a lot of fun, a enjoyable experience and personally a valuable lesson for me to keep improving as a software engineer. It made me realize that I picked the right major.

Mit freundlichen Grüßen

Nguyen Trung Hieu

[Project Repository](https://github.com/CodeBellinger/EnglishProjectWithPython-RaspberryPi)
