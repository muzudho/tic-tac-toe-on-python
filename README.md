# Tic tac toe on python

○×ゲームだぜ☆（＾～＾）  

* 他のプログラム言語
  * [プログラミング入門動画](https://www.youtube.com/playlist?list=PLllMJuAE0iK6kSsi96OBXBgNZHFg7KB9f) - 小学生は変女に Scratch でも教えられてろだぜ☆（＾～＾）
  * [Go ver](https://github.com/muzudho/tic-tac-toe-golang)
  * [Rust ver](https://github.com/muzudho/tic-tac-toe)

## How to make tic tac toe?

During development, you may need to reproduce the behavior of your computer.  
It is difficult to compare the behavior. Instead, it is useful to get the logs and compare the logs.  

* [x] Step 1. 'log.py' (You can code in 10 minutes)
  * [x] Clear - Log to empty.
  * [x] Write - Write to a file.
  * [x] Print - Write and display.

The first thing you have to create is your motive.  
It is important to start with the appearance.  

* [x] Step 2. 'look_and_model.py' (You can code in 4 hours)
  * [x] Piece - "O", "X".
  * [x] Game result - Win/Draw/Lose.
  * [x] Position - It's the board.
  * [x] Search - Computer player search info.

If you want to play immediately, you have the talent of a game creator.  
Being able to control your position means being able to play.  

* [x] Step 3. 'position.py' (You can code in 15 minutes)
  * [x] do_move
  * [x] undo_move
  * [x] opponent

Let's enter commands into the computer. Create a command line parser.  

* [x] Step 4. 'command_line_parser.py' (You can code in 40 minutes)
  * [x] Input.
  * [x] Starts with.
  * [x] Go next to.
  * [x] Rest.

People who are looking for something 10 minutes a day are looking for something for a week in a year.  
Before creating the game itself, let's first create the replay function. Let's get it for a week.  

* [x] Step 5. 'uxi_protocol.py' (You can code in 1.5 hours)
  * [x] To XFEN.
  * [x] Do. (Before 'From XFEN') Excludes legal moves and winning/losing decisions.
  * [x] From XFEN.
  * [x] Undo.

Let's make a principal command.  

* [x] Step 6. 'main.py' (You can code in 1 hours)
  * [x] position.
  * [x] pos.
  * [x] do.
  * [x] undo.
  * [x] uxi tic-tac-toe
  * [x] xfen.

Before you make a computer player, let's judge the outcome. And let's test.  

* [x] Step 7. 'win_lose_judgment.py' (You can code in 15 minutes)
  * [x] Win.
  * [x] Draw - Not win, not lose, can not play.
  * [ ] Lose. - Not win is lose.
* [x] 'uxi_protocol.py' (You can code in 1.5 hours)
  * [x] Do. Winning/losing decisions.

Before creating a computer player, let's create a mechanism to measure performance.  

* [x] Step 8. 'performance_measurement.py' (You can code in 15 minutes)
  * [x] Seconds. - Stopwatch.
  * [x] Node per second.

Finally, let's make a computer player. (You can code in 1.5 hours)  

* [x] Step 9. 'computer_player.py'
  * [x] Search.
  * [ ] Evaluation. - None.
* [x] 'main.py'
  * [x] Create "go" command.
* [x] Remeve all 'TODO' tasks. Examples: '// TODO Write a code here.'
