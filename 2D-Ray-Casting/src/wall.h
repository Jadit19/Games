#ifndef WALL_H_INCLUDED
#define WALL_H_INCLUDED

#include "../config.h"

class Wall
{
    public:
        Wall (){};
        Wall (sf::Vector2f pos1, sf::Vector2f pos2){
            start = pos1;
            end = pos2;
        }

        sf::Vector2f getStart (){
            return start;
        }
        sf::Vector2f getEnd (){
            return end;
        }

        void reset (){
            start = sf::Vector2f(random(WINDOW_WIDTH), random(WINDOW_HEIGHT));
            end = sf::Vector2f(random(WINDOW_WIDTH), random(WINDOW_HEIGHT));
        }

    private:
        sf::Vector2f start;
        sf::Vector2f end;
};

#endif // WALL_H_INCLUDED