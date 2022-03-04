#include <time.h>
#include <SFML/Graphics.hpp>
#include <iostream>

#include "config.h"

bool opened[COLUMNS+2][ROWS+2] = { 0 };
bool gameOver = 0;
int score = 0, maxScore = 0;
int grid[COLUMNS+2][ROWS+2] = { 0 };
int sgrid[COLUMNS+2][ROWS+2] = { 10 };
sf::Font font;

class sfText {
    public:
        sfText(std::string str, int posX, int posY, bool c=0){
            text.setFont(font);
            text.setCharacterSize(SCALE*32);
            text.setString(str);
            text.setPosition(posX, posY);
            if (c)
                text.setColor(sf::Color::Red);
            else
                text.setColor(sf::Color::White);
        }

        void changeText(std::string str){
            text.setString(str);
        }

        sf::Text returnText(){
            return text;
        }

    private:
        sf::Text text;
};

void reveal(int x, int y){
    sgrid[x][y] = grid[x][y];
    opened[x][y] = 1;
    if (grid[x][y]!=0)
        return;

    sgrid[x][y] = 10;
    if (x>1){
        if (opened[x-1][y]==0)
            reveal(x-1, y);
        if (y>1 && opened[x-1][y-1]==0)
            reveal(x-1, y-1);
        if (y<ROWS && opened[x-1][y+1]==0)
            reveal(x-1, y+1);
    }
    if (x<COLUMNS){
        if (opened[x+1][y]==0)
            reveal(x+1, y);
        if (y>1 && opened[x+1][y-1]==0)
            reveal(x+1, y-1);
        if (y<ROWS && opened[x+1][y+1]==0)
            reveal(x+1, y+1);
    }
    if (y>1 && opened[x][y-1]==0)
        reveal(x, y-1);
    if (y<ROWS && opened[x][y+1]==0)
        reveal(x, y+1);
}

int main() {
    srand(time(0));

    sf::RenderWindow window(sf::VideoMode(32*(COLUMNS+2)*SCALE, 32*(ROWS+5)*SCALE), "Minesweeper");

    sf::Texture texture;
    texture.loadFromFile("res/img/tiles.jpg");
    sf::Sprite sprite(texture);

    if (!font.loadFromFile("res/font/Regular.ttf")){
        std::cout << "Font could not be loaded!";
        return 1;
    }
    sfText nameText("PLAYER NAME       : "+NAME, 32*SCALE, (ROWS+2)*32*SCALE);
    sfText scoreText(" ", 32*SCALE, (ROWS+3)*32*SCALE);
    sfText loseText("TRY AGAIN!", 32*SCALE*(COLUMNS-3), (ROWS+2)*32*SCALE, 1);

    for (int i=1; i<=COLUMNS; i++){
        for (int j=1; j<=ROWS; j++){
            if (rand()%PROB == 0){
                grid[i][j] = 9;
                maxScore++;
            }
        }
    }

    for (int i=1; i<=COLUMNS; i++){
        for (int j=0; j<=ROWS; j++){
            int n=0;
            if (grid[i][j] == 9)
                continue;

            if (grid[i+1][j] == 9) n++;
            if (grid[i-1][j] == 9) n++;
            if (grid[i][j+1] == 9) n++;
            if (grid[i][j-1] == 9) n++;

            if (grid[i+1][j+1] == 9) n++;
            if (grid[i+1][j-1] == 9) n++;
            if (grid[i-1][j+1] == 9) n++;
            if (grid[i-1][j-1] == 9) n++;

            grid[i][j] = n;
        }
    }

    while (window.isOpen()){
        sf::Vector2i pos = sf::Mouse::getPosition(window);
        int x = pos.x/(SCALE*32);
        int y = pos.y/(SCALE*32);

        sf::Event event;

        while (window.pollEvent(event)){
            if (event.type == sf::Event::Closed)
                window.close();

            if (event.type == sf::Event::MouseButtonPressed && !gameOver){
                if ((x>0 && x<=COLUMNS) && (y>0 && y<=ROWS)){
                    if (event.key.code == sf::Mouse::Left)
                        reveal(x, y);
                    else if (event.key.code == sf::Mouse::Right){
                        if (sgrid[x][y] == 0){
                            sgrid[x][y] = 11;
                            score++;
                        } else if (sgrid[x][y] == 11){
                            sgrid[x][y] = 0;
                            score--;
                        }
                    }
                }
            }
        }

        window.clear(sf::Color::Black);
        for (int i=1; i<=COLUMNS; i++){
            for (int j=1; j<=ROWS; j++){
                if (sgrid[x][y] == 9){
                    sgrid[i][j] = grid[i][j];
                    score = maxScore;
                    gameOver = 1;
                }

                sprite.setTextureRect(sf::IntRect(sgrid[i][j]*32, 0, 32, 32));
                sprite.setScale(SCALE, SCALE);
                sprite.setPosition(i*SCALE*32, j*SCALE*32);
                window.draw(sprite);
            }
        }

        scoreText.changeText("MINES IDENTIFIED : " + std::to_string(score) + "/" + std::to_string(maxScore));

        window.draw(nameText.returnText());
        window.draw(scoreText.returnText());
        if (gameOver)
            window.draw(loseText.returnText());

        window.display();
    }

    return 0;
}
