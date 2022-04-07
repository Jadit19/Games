# 2D Ray Casting

## Setup
There is a wonderful video by <a href="https://www.youtube.com/watch?v=fcZFaiGFIMA&list=PLMZ_9w2XRxiYkf00joyT5_bKQ0AvnMLbl&index=2">Hopson</a> that explains how to get started with SFML and Codeblocks<br>
If you're like me, who wants to execute terminal commands instead, here you go:

0. I'm assuming you have a C++ compiler installed, preferably, the <a href="https://www.mingw-w64.org/downloads/">MinGW</a> one.
1. Follow `./lib/Instructions.md`
2. Copy-Paste the files present in `./lib/SFML/bin`, here:
```
- sfml-graphics-d-2.dll
- sfml-system-d-2.dll
- sfml-window-d-2.dll
```
3. Run the following codes in the exact same order
```sh
g++ -Wall -fexceptions -g -Ilib\SFML\include -c .\main.cpp -o .\main.o
```
```sh
g++ -Llib\SFML\lib -o .\2d_Ray_Casting.exe .\main.o -lsfml-graphics-d -lsfml-window-d -lsfml-system-d
```
```sh
.\2d_Ray_Casting.exe
```
4. Control is achieved using the cursor
5. Walls are generated randomly, so to reset, use `R`
6. Something magical happens on pressing `Spacebar`
7. As always, some details can be tweaked in `config.h`

## Other Info
1. Ray Casting was on my mind for quite a while, so I tried it out..
2. This is just an elementary level trial; if possible, I'll try making a 3D version of it as well, you know, kinda like Wolfenstein 3D. I'll update the repo if and when done