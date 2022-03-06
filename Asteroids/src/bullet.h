#ifndef BULLET_H_INCLUDED
#define BULLET_H_INCLUDED

#include <cmath>

#include "entity.h"

class Bullet : public Entity
{
    public:
        Bullet(){
            name = "bullet";
        }

        void update(){
            dx = cos(angle*DEG_TO_RAD)*6;
            dy = sin(angle*DEG_TO_RAD)*6;

            x += dx;
            y += dy;

            if (x>WIDTH || x<0 || y>HEIGHT || y<0)
                life = 0;
        }
};

#endif // BULLET_H_INCLUDED