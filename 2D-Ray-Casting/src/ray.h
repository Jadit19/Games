#ifndef RAY_H_INCLUDED
#define RAY_H_INCLUDED

#include <iostream>
#include "../config.h"

class Ray
{
    public:
        Ray (){}
        Ray (float x, float y){
            _relative_end = sf::Vector2f(x, y) * 3000.f;
        }

        sf::Vector2f getEnd (){
            return _end;
        }

        void calcHit (sf::Vector2f p3, sf::Vector2f p4){
            const sf::Vector2f p1 = _mousePos;
            const sf::Vector2f p2 = _end;

            const float den = (p1.x - p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x - p4.x);
            if (den == 0){
                return;
            }

            const float t1 = ((p1.x - p3.x)*(p3.y - p4.y) - (p1.y - p3.y)*(p3.x - p4.x)) / den;
            const float t2 = -((p1.x - p2.x)*(p1.y - p3.y) - (p1.y - p2.y)*(p1.x - p3.x)) / den;

            // Checking for intersection..
            if (t1>0 && t1<1 && t2>0 && t2<1){
                _end.x = p1.x + t1*(p2.x - p1.x);
                _end.y = p1.y + t1*(p2.y - p1.y);
            }
        }

        void reset (){
            _end = _mousePos + _relative_end;
        }

    private:
        sf::Vector2f _relative_end;
        sf::Vector2f _end;
};

#endif // RAY_H_INCLUDED