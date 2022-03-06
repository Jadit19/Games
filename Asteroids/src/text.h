#ifndef TEXT_H_INCLUDED
#define TEXT_H_INCLUDED

#include <SFML/Graphics.hpp>
#include <string>

class Text
{
    public:
        Text(std::string str, int posX, int posY, sf::Font* font, sf::Color c){
            text.setFont(*font);
            text.setCharacterSize(30);
            text.setString(str);
            text.setPosition(posX, posY);
            text.setColor(c);
        }

        void updateText(std::string str){
            text.setString(str);
        }

        sf::Text returnText(){
            return text;
        }

    private:
        sf::Text text;
};

#endif // TEXT_H_INCLUDED