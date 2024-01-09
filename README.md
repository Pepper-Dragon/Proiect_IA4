# The Ball


## Description
The Ball is a puzzle and platformer game. You move around the map at your own risk,
deflating or managing to reinflate.

## Features
- Sprite rendering
- Physical simulation
- Collision detection

## Installation
1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the game using `python game.py`

## Controls
- `SPACE` to jump
- `A` to move left
- `D` to move right

## Content
- `game.py` is the main file that initializes and runs the game
- `globals.py` contains global variables
- `scene.py` contains the Scene class where the game is played
- `player.py` contains the Player class that represents the player
- `ball.py` contains the Ball class that makes the ball soft body
- `rectangle.py` contains the Rect class that makes the rectangle soft body
- `objutils.py` contains collision and integration code for objects


## Project History

- ### Prototype stage

    Even before we started the project we had to make sure that it was posible to
    build such a game, so we first worked on making the actual soft body model, the ball. After some problems (physics simulations are really unpredictable) we got this:

    <img src = ./gifs/prot.gif>

    Broadly, the body is made out of springs that are connected in a circle. Easy enough, you apply gravity to the conecting points and spring formula known since high school , then you integrate to get the velocity and position. Well... that yields this:

    <img src = ./gifs/no_p.gif>

    The problem is fixed by adding pressure inside the ball and that gave us the idea for the whole gameplay loop: The player (the ball) looses pressure as it moves around the map , so to inflate itself back, it collects smaller balls.

    #### Problems encountered in this stage of dev
    - The pressure problem explained previously.
    - A really annoying delta time problem. We wanted the game to be framerate independent , so we added varaible deltatime. That crashed the simulation numerous times, apperently pyhsics simulations usually work only on a fixed deltatime. We eventually compromised by making the delta time semi-variable (it has a lower and a upper limit).


- ### Collisions and the addition of other objects

    #### Ball changes
    - Added a user input (the ball can roll around)
    - Added a small circle to indicate that the ball is rolling (makes the movement clearer)
    - The ball deflates as you move.

    The jelly physics are cool, but they don't make an exciting game, so we made other
    objects to interact with.
    
    Because we made a ball class it was really easy to make other smaller balls for the game mechanic we talked previously. After that we design rectangle like objects
    that are also the walls for the final version of the game. The dynamic version of them are made out of springs like the ball (they have springs on every side and on the diagonal for support)

    <img src = ./gifs/rect.gif>


    If we play the game now we will get this:


    <img src = ./gifs/no_col.gif>


    As you can see we cannot interact with the newly added object. That is because we don't have the collision algorithm made.

    #### Collisions

    Because we made our own objects we need to also handle collisions, before this point we used a simple y coordonate check to stop the objects from going through the floor.
    
    Collision steps:

    - check if a point of an object is inside another object.
 
    - if it is, find the nearest edge to the point and push it out so that the point is  on the edge.

    - update the velocity based on a elastic collision made between the point and a virtual point made to represent the side.

    We would not have any sliding by apllying the algorthm explained previously. We only use the normal velocity for the actual collision and the tangent velocity we make slightly smaller.

    The results so far:

    <img src = ./gifs/col.gif>

- ### Adding sprites and making a level
    #### Ball changes
    - The player can jump.
    - The ball inflates when it collects other balls.
    - The game has a camera that follows the player character.

    #### Game changes
    - The previous classes were reworked so that the code was modular, making it really easy to create/destroy objects.

    - A camera was implemented that follows the player.

    - The static rect objects can have sprites now. Also the game has background.

    - Made demo stage with puzzle and platformer elements.

    The finished product:

    <img src = ./gifs/done.gif>

## Sources
- #### We did not invent the soft body implementation. The model's theory is from this paper:
    https://www.researchgate.net/publication/228574502_How_to_implement_a_pressure_soft_body_model

- #### Collision code idea (we used a slightly modified version):
    https://www.youtube.com/watch?v=3OmkehAJoyo&t=52s
