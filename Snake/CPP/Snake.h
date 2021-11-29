#ifndef SNAKE_H
#define SNAKE_H

#define WIDTH 50
#define HEIGHT 25

#include <windows.h>
#include <unistd.h>
#include <vector>

const bool isWallAnEnd = 1;

class Snake{
    private:
        COORD pos;
        int len;
        int vel;
        char direction;

    public:
        std::vector<COORD> body;

        Snake(COORD pos, int vel);
        std::vector<COORD> getBody();
        COORD getPos();
        bool eatenFood(COORD foodPos);
        bool collided();
        void changeDir(char dir);
        void moveSnake();
        void growSnake();
};

Snake::Snake(COORD pos, int vel){
    this->pos = pos;
    this->vel = vel;
    len = 1;
    direction = 'n';
    body.push_back(pos);
}

void Snake::changeDir(char dir){
    direction = dir;
}

void Snake::moveSnake(){
    switch(direction){
        case 'u': 
            pos.Y -= 1;
            usleep(50000/vel);
            break;
        case 'd':
            pos.Y += 1;
            usleep(50000/vel);
            break;
        case 'l': 
            pos.X -= 1;
            break;
        case 'r':
            pos.X += 1;
            break;
    }
    usleep(50000/vel);

    if (!isWallAnEnd){
        if (pos.X>WIDTH-2){
            pos.X = 1;
        } else if (pos.X<1){
            pos.X = WIDTH-2;
        }

        if (pos.Y>HEIGHT-2){
            pos.Y = 1;
        } else if (pos.Y<1){
            pos.Y = HEIGHT-2;
        }
    }

    body.push_back(pos);
    if (body.size() > len){
        body.erase(body.begin());
    }
}

COORD Snake::getPos(){
    return pos;
}

bool Snake::eatenFood(COORD foodPos){
    if (foodPos.X==pos.X && foodPos.Y==pos.Y)
        return 1;
    return 0;
}

void Snake::growSnake(){
    len++;
}

bool Snake::collided(){
    if (pos.X<1 || pos.X>WIDTH-2 || pos.Y<1 || pos.Y>HEIGHT-2){
        return 1;
    }
    for (int i=0; i<body.size()-1; i++){
        if (pos.X==body[i].X && pos.Y==body[i].Y){
            return 1;
        }
    }
    return 0;
}

std::vector<COORD> Snake::getBody() {
    return body;
}

#endif