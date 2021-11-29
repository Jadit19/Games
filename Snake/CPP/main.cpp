#include <iostream>
#include <cstdlib>
#include <conio.h>
#include <ctime>

#include "Snake.h"
#include "Food.h"

#define WIDTH 50
#define HEIGHT 25
Snake snake({ WIDTH/2, HEIGHT/2 }, 2);
Food food;
bool gameOver = 0;
int score = 0;

using namespace std;

void ShowConsoleCursor(bool showFlag){
    HANDLE out = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO cursorInfo;
    GetConsoleCursorInfo(out, &cursorInfo);
    cursorInfo.bVisible = showFlag;
    SetConsoleCursorInfo(out, &cursorInfo);
}

void board(){
    COORD snakePos = snake.getPos();
    COORD foodPos = food.getPos();
    std::vector<COORD> snakeBody = snake.getBody();

    cout << "\tSCORE: " << score << "\n\n\t\t";
    for (int i=0; i<WIDTH; i++)
        cout << "-";
    cout << "\n";
    for (int i=1; i<HEIGHT-1; i++){
        cout << "\t\t|";
        for (int j=1; j<WIDTH-1; j++){
            if (j==snakePos.X && i==snakePos.Y){
                cout << "0";
            } else if (j==foodPos.X && i==foodPos.Y) {
                cout << "o";
            } else {
                bool isBodyPart = 0;
                for (int k=0; k<snakeBody.size()-1; k++){
                    if (i==snakeBody[k].Y && j==snakeBody[k].X){
                        cout << "*";
                        isBodyPart = 1;
                        break;
                    }
                }

                if (!isBodyPart)
                    cout << " ";
            }
        }
        cout << "|\n";
    }
    cout << "\t\t";
    for (int i=0; i<WIDTH; i++)
        cout << "-";
}

int main(){
    system("cls");
    ShowConsoleCursor(false);
    srand(time(NULL));

    food.genFood();
    while (!gameOver){
        board();

        if (kbhit()){
            switch(getch()){
                case 72:
                case 'w':
                    snake.changeDir('u');
                    break;
                case 75:
                case 'a':
                    snake.changeDir('l');
                    break;
                case 80:
                case 's':
                    snake.changeDir('d');
                    break;
                case 77:
                case 'd':
                    snake.changeDir('r');
                    break;
            }
        }

        if (snake.eatenFood(food.getPos())){
            food.genFood();
            snake.growSnake();
            score++;
        }

        if (snake.collided()){
            gameOver = 1;
            cout << "\n\n\tYour final score is: " << score << "\n\tPress any key to continue..";
        }

        snake.moveSnake();

        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), {0, 0});
    }

    getch();
    system("cls");
    return 0;
}