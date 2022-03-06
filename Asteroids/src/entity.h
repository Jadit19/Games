#ifndef ENTITY_H_INCLUDED
#define ENTITY_H_INCLUDED

#include <string>

#include "animation.h"
#include "../config.h"

class Entity
{
    public:
        Entity(){
            life = 1;
        }

        void settings(Animation &a, int X, int Y, float Angle=0, int radius=1){
            x = X;
            y = Y;
            anim = a;
            angle = Angle;
            R = radius;
        }

        virtual void update(){ };

        virtual void draw(sf::RenderWindow &window){
            anim.sprite.setPosition(x, y);
            anim.sprite.setRotation(angle + 90);
            window.draw(anim.getSprite());
        }

        float x, y, dx, dy, R, angle;
        bool life;
        std::string name;
        Animation anim;
};

#endif // ENTITY_H_INCLUDED