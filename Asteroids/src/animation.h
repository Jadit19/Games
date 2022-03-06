#ifndef ANIMATION_H_INCLUDED
#define ANIMATION_H_INCLUDED

#include <SFML/Graphics.hpp>
#include <vector>

class Animation
{
    public:
        Animation () {};
        Animation(sf::Texture &t, int x, int y, int w, int h, int count, float _speed){
            frame = 0;
            speed = _speed;

            for (int i=0; i<count; i++){
                frames.push_back(sf::IntRect(x+i*w, y, w, h));
            }

            sprite.setTexture(t);
            sprite.setOrigin(w/2, w/2);
            sprite.setTextureRect(frames[0]);
        }

        void update(){
            frame += speed;
            int n = frames.size();

            if (frame >= n)
                frame -= n;
            if (n > 0)
                sprite.setTextureRect(frames[int(frame)]);
        }

        sf::Sprite getSprite(){
            return sprite;
        }

        float frame, speed;
        sf::Sprite sprite;
        std::vector<sf::IntRect> frames;
};

#endif // ANIMATION_H_INCLUDED