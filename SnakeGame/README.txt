BUG WARNING! It is better not to press several keys that control the snake at the same time.
(More details about the bug are written in the documentation in the snake.py file in line 19 and beyond)

SNAKE CONTROL:
- keys 'wasd' or using the arrows on the keyboard

The gameplay is standard: apples appear on the playing field in a random place. If you eat them, the snake grows, and score increase.
Red apples increase the snake by 1 cell and increase the score by 1.
But there are also gold apples that appear along with red with a probability of 1/10.
They increase the score by 10 and the snake by 3 cells.
But they disappear some time after they appear, so you may not have time to eat them.

The snake moves through the cells in four directions.
If it goes beyond the edge of the field, it is transferred to the opposite edge.
Each time a snake eats apples, its speed increases until it reaches its maximum.
If the snake bites itself, the game stops and game statistics are displayed.

Points and game record are displayed at the top.
I added game record saving.
If a player scores more points than his previous record and loses, this record will be saved and will be displayed at the top the next time he starts.
Also, if during the game the player breaks his record, then after the game on the screen will be written "New Record!"
