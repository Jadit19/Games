#ifndef CONFIG_H_INCLUDED
#define CONFIG_H_INCLUDED

#include <SFML/Graphics.hpp>
#include <random>

const int WINDOW_WIDTH = 1600;
const int WINDOW_HEIGHT = 900;

const int WALLS = 4;
const sf::Color WALL_COLOR = sf::Color::Red;
const float RAY_DENSITY = 3000;
const sf::Color RAY_COLOR = sf::Color::White;
const float ACCURACY = 2;

const double PI = 3.141592653589f;
extern sf::Vector2f _mousePos;

inline int random (int max, int min=0){ return ((rand() % (max-min)) + min); }

#endif // CONFIG_H_INCLUDED