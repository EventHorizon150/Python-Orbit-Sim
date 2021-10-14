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
## Controls
 * Move camera with WASD. 
 * Press the spacebar to reset to the begining. 
 * Hold tab and use foreward arrow key to go frame by frame. 
 * Click to create a new body.
 * Click and drag to create a new body with mass. 
 * Click and release while holding shift to create a fixed body. 
 * Escape key to exit. 