# Python-Orbit-Sim
A 2D physics sim for orbits. Made using pygame and tkinter. High degree of intractability, 
allowing you to create celestial bodies of a custom mass and velocity within the simulation, 
select what specifically is displayed, and move the camera. High degree of accuracy in simulation, without sacrificing useablity. Using vectors and numpy for simulation math. 

## Setup
You need to have Python 3, Tkinter, and Pygame installed. 

Windows:
```
git clone git@github.com:EventHorizon150/Python-Orbit-Sim.git
cd Python-Orbit-Sim
pip install -r requirements.txt
```
Linux:
```
git clone git@github.com:EventHorizon150/Python-Orbit-Sim.git
cd Python-Orbit-Sim
pip3 install -r requirements.txt
```

## To run
Run Gravity.py to start.

Windows: 
```
python gravity.py
```
Linux:
```
python3 gravity.py
```
## Game Options

Display settings:
 * Draw vectors: Draws the speed and direction of the vector for each body onscreen. 
 * Draw gravity: Draws the pulls of gravity for each body by each other object onscreen.
 * Draw net grav: Draws the net pull of gravity for each object onscreen. 
 * Draw trail: Draws a trail behind each object onscreen. 
 * Draw center of mass: Draws the center of all mass that exists onscreen. 

 Presets:
 * None: Start with a blank screen for you to add their own bodies and stuff. 
 * Random: Starts the number of bodies you select onscreen. Location is determined by the seed. Seeds can be reused for the same results. Leave it blank for a random seed. 
 * Circular orbit: Starts 2 bodies onscreen, one with the mass of earth, and one with the velocity and mass of the moon. 
 * Oscellation: It looks cool just take a look. 
 
## Controls
 * Move camera with WASD. 
 * Press the spacebar to revert to preset.
 * Shift + spacebar to clear the screen 
 * Hold tab to pause
 * Tab + right arrow to progress frame by frame
 * Click to create a new body.
 * Click and drag to create a new body with velocity.
 * While holding right click, use the number keys to specify a specific mass for the body. 
 * Press enter to commit this new mass
 * Shift + click to create a fixed body. 
 * Escape key to exit. 
