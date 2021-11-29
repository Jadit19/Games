#ifndef FOOD_H
#define FOOD_H

#define WIDTH 50
#define HEIGHT 25

#include <windows.h>
#include <stdlib.h>

class Food{
    private:
        COORD pos;

    public:
        Food();
        void genFood();
        COORD getPos();
};

Food::Food(){
    genFood();
}

void Food::genFood(){
    pos.X = (rand() % (WIDTH-2)) + 1;
    pos.Y = (rand() % (HEIGHT-2)) + 1;
}

COORD Food::getPos(){
    return pos;
}

#endif