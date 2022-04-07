#include <iostream>
#include <SFML/System.hpp>

#include "src/ray.h"
#include "src/wall.h"

// Global Variables..
sf::Vector2f _mousePos = sf::Vector2f(0, 0);
bool flag = 1;

bool checkDist(sf::Vector2f p1, sf::Vector2f p2){
    float x = pow(p1.x - p2.x, 2);
    float y = pow(p1.y - p2.y, 2);
    if (sqrt(x+y) < ACCURACY)
        return true;
    else
        return false;
}

int main()
{
    srand(time(NULL));
    sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "2D Ray Casting");

    // Walls..
    std::vector<Wall> walls;
    for (int i=0; i<WALLS; i++){
        const sf::Vector2f START = sf::Vector2f(random(WINDOW_WIDTH), random(WINDOW_HEIGHT));
        const sf::Vector2f END = sf::Vector2f(random(WINDOW_WIDTH), random(WINDOW_HEIGHT));
        walls.push_back(Wall(START, END));
    }
    sf::VertexArray wallLine(sf::Lines, 2);
    wallLine[0].color = WALL_COLOR;
    wallLine[1].color = WALL_COLOR;

    // Rays..
    std::vector<Ray> rays;
    const float STEP = 1.f / RAY_DENSITY;
    for (float i=0; i<2*PI; i+=STEP){
        const float X = cos(i);
        const float Y = sin(i);
        rays.push_back(Ray(X, Y));
    }
    sf::VertexArray rayLine(sf::Lines, 2);
    rayLine[0].color = RAY_COLOR;
    rayLine[1].color = RAY_COLOR;

    sf::Vector2f mousePos;

    while (window.isOpen()){
        sf::Event e;

        while (window.pollEvent(e)){
            if (e.type == sf::Event::Closed)
                window.close();
            if (e.type == sf::Event::KeyPressed){
                if (e.key.code == sf::Keyboard::Escape)
                    window.close();
                else if (e.key.code == sf::Keyboard::R){
                    for (int i=0; i<WALLS; i++)
                        walls[i].reset();
                    sf::sleep(sf::milliseconds(200));
                } else if (e.key.code == sf::Keyboard::Space)
                    flag = !flag;
            }
        }

        _mousePos = sf::Vector2f(sf::Mouse::getPosition(window));
        // if (_mousePos == mousePos)
            // continue;
        
        rayLine[0].position = _mousePos;
        window.clear();

        for (Ray ray: rays){
            ray.reset();
            for (int i=0; i<WALLS; i++)
                ray.calcHit(walls[i].getStart(), walls[i].getEnd());
            rayLine[1].position = ray.getEnd();
            if (flag)
                window.draw(rayLine);
            else {
                for (Wall w: walls){
                    if (checkDist(w.getEnd(), ray.getEnd()) || checkDist(w.getStart(), ray.getEnd())){
                        window.draw(rayLine);
                        break;
                    }
                }
            }
        }

        for (int i=0; i<WALLS; i++){
            wallLine[0].position = walls[i].getStart();
            wallLine[1].position = walls[i].getEnd();
            window.draw(wallLine);
        }

        window.display();
        mousePos = _mousePos;
    }

    return 0;
}
