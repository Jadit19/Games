#ifndef ASTEROID_H_INCLUDED
#define ASTEROID_H_INCLUDED

#include <random>

#include "entity.h"

class Asteroid : public Entity
{
    public:
        Asteroid(){
            dx = rand()%8 - 4;
            dy = rand()%8 - 4;
            name = "asteroid";
        }

        void update(){
            x += dx;
            y += dy;

            if (x > WIDTH)
                x = 0;
            else if (x < 0)
                x = WIDTH;
            if (y > HEIGHT)
                y = 0;
            else if (y < 0)
                y = HEIGHT;
        }
};

#endif // ASTEROID_H_INCLUDED