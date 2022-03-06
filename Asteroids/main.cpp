#include <cmath>
#include <list>
#include <iostream>

#include "src/asteroid.h"
#include "src/bullet.h"
#include "src/text.h"

float x=300, y=300;
float dx=0, dy=0, angle=0;
float speed=0;
int score=0, ammo=AMMO;
bool thrust=0, gameOver=0, win=0;

//! Collission detection function
bool isCollide(Entity *a, Entity *b){
    return ((b->x-a->x)*(b->x-a->x) + (b->y-a->y)*(b->y-a->y) < (b->R+a->R)*(b->R+a->R));
}

int main(){

    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "Asteroids");
    window.setFramerateLimit(60);

    //! Font and text
    sf::Font font;
    if (!font.loadFromFile("res/font/Regular.ttf")){
        std::cout << "\nFont could not be loaded!\nExiting..\n\n";
        return EXIT_FAILURE;
    }
    Text scoreText("SCORE: 0/"+std::to_string(ASTEROIDS), 10, 10, &font, sf::Color::White);
    Text ammoText("AMMO: "+std::to_string(ammo), 10, 42, &font, sf::Color::White);
    Text loseText("YOU LOSE!", WIDTH-120, 10, &font, sf::Color::Red);
    Text winText("YOU WIN!", WIDTH-110, 10, &font, sf::Color::Green);

    //! Texture atlas
    sf::Texture t1, t2, t3;
    t1.loadFromFile("./res/img/spaceship.png");
    t2.loadFromFile("./res/img/rock.png");
    t3.loadFromFile("./res/img/bullet.png");

    //! Sprites collection
    sf::Sprite sPlayer(t1);
    sPlayer.setTextureRect(sf::IntRect(40, 0, 40, 40));
    sPlayer.setOrigin(20, 20);

    //! Asteroids and Bullets
    Animation sRock(t2, 0, 0, 64, 64, 16, 0.2);
    Animation sBullet(t3, 0, 0, 32, 64, 16, 0.8);
    sRock.sprite.setPosition(400, 400);

    std::list<Entity*> entities;
    for (int i=0; i<ASTEROIDS; i++){
        Asteroid *a = new Asteroid();
        a->settings(sRock, rand()%WIDTH, rand()%HEIGHT, rand()%360, 25);
        entities.push_back(a);
    }

    while (window.isOpen()){
        sf::Event event;

        while (window.pollEvent(event)){
            if (event.type == sf::Event::Closed)
                window.close();

            if (event.type == sf::Event::KeyPressed && !gameOver){
                if (event.key.code == sf::Keyboard::Space){
                    Bullet *b = new Bullet();
                    b->settings(sBullet, x, y, angle, 10);
                    entities.push_back(b);
                    ammo--;
                }
            }
        }

        //! Game Ending events
        if (ammo<0){
            gameOver = 1;
        }
        if (score==ASTEROIDS){
            win = 1;
            gameOver = 1;
        }

        //! Keyboard inputs..
        if (!gameOver){
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right) || sf::Keyboard::isKeyPressed(sf::Keyboard::D))
                angle += 3;
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left) || sf::Keyboard::isKeyPressed(sf::Keyboard::A))
                angle -= 3;
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up) || sf::Keyboard::isKeyPressed(sf::Keyboard::W))
                thrust = 1;
            else
                thrust = 0;
        }

        //! Collission detection
        for (auto i: entities){
            if (i->name == "asteroid"){
                for (auto j: entities){
                    if (j->name == "bullet"){
                        if (isCollide(i, j)){
                            i->life = 0;
                            j->life = 0;
                            score++;
                        }
                    }
                }

                int powX = pow(sPlayer.getPosition().x-i->x, 2);
                int powY = pow(sPlayer.getPosition().y-i->y, 2);
                if (powX+powY < 1600){
                    gameOver = 1;
                }
            }
        }

        //! Spaceship movement
        if (!gameOver){
            if (thrust){
                dx += cos(angle*DEG_TO_RAD) * SENSITIVITY;
                dy += sin(angle*DEG_TO_RAD) * SENSITIVITY;
            } else {
                dx *= (1-FRICTION);
                dy *= (1-FRICTION);
            }

            speed = sqrt(dx*dx + dy*dy);
            if (speed > MAX_SPEED){
                dx *= MAX_SPEED/speed;
                dy *= dx;
            }
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
            
            sPlayer.setPosition(x, y);
            sPlayer.setRotation(angle + 90);
        }

        //! Entities movement
        if (!gameOver){
            for (auto i=entities.begin(); i!=entities.end(); ){
                Entity *e = *i;
                e->update();
                e->anim.update();

                if (!e->life){
                    i = entities.erase(i);
                    delete e;
                } else 
                    i++;
            }
        }

        //! Update texts
        scoreText.updateText("SCORE: "+std::to_string(score)+"/"+std::to_string(ASTEROIDS));
        ammoText.updateText("AMMO: "+std::to_string(ammo));
        
        //! Draw all
        window.clear(sf::Color::Black);

        window.draw(sPlayer);
        for (auto i: entities)
            i->draw(window);
        window.draw(scoreText.returnText());
        window.draw(ammoText.returnText());
        if (gameOver){
            if (win)
                window.draw(winText.returnText());
            else
                window.draw(loseText.returnText());
        }

        window.display();
    }

    return EXIT_SUCCESS;
}