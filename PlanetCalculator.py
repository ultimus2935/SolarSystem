# Version 0.3 - Ultimus (23/05/2003)

from vpython import *
import json, os, shutil
from time import perf_counter

# Simulation Dataset Details
dataset_name = "Earth System Simulation (Hierarchical System)"

if not os.path.exists(f'./datasets/{dataset_name}/'):
    os.mkdir(f'./datasets/{dataset_name}/')
    
    if not os.path.exists(f'./datasets/{dataset_name}/Planets.json'):
        shutil.copy('./Planets.json', f'./datasets/{dataset_name}/Planets.json')
    if not os.path.exists(f'./datasets/{dataset_name}/Moons.json'):
        shutil.copy('./Planets.json', f'./datasets/{dataset_name}/Moons.json')

global bodies, t, xt, dt

# Simulation Vari
t = 0.0
xt = 1e+8 # Simulation Speed
dt = 10.0 # Time Increment

tl = 6.307e+7 # Time Limit in seconds
epoch = 1000 # Number of datapoints written per save

# Constants
G = 6.674011e-11

# List of Body datasets
datasets = {}
with open(f'./datasets/{dataset_name}/Planets.json') as f:
    planets = json.load(f)
    for planet in planets: 
        dataset = open(f'./datasets/{dataset_name}/{planet}.txt', 'a')
        datasets[planet] = dataset
        
# List of all Body objects
bodies = []

# Defining properties of Body
class Body():
    global bodies, t, xt, dt
    
    def __init__(self, 
        name: str,
        mass: float, 
        size: vector, 
        position: vector, 
        velocity: vector = vector(0, 0, 0)
    ):
        self.name = name; self.mass = mass; self.size = size # Name of Body, Mass, Dimensions
        self.pos = position; self.vel = velocity # Postion, Velocity
        self.acc = vector(0, 0, 0) # Acceleration
        
        self.index = 0 # Index of written data
        
    def gravitationalAcceleration(self): 
        acc = vector(0, 0, 0)
        for otherBody in [body for body in bodies if body != self]:
            radius = otherBody.pos - self.pos # Distance vector from body to otherBody
            self.acc += norm(radius)*(otherBody.mass/mag2(radius)) # Newton's Law of Gravitation
            
        acc *= G
        
        return acc
            
    def update(self): 
        self.acc = self.gravitationalAcceleration()
        self.vel += self.acc*dt
        self.pos += self.vel*dt
            
    def log(self): 
        dataset = datasets[self.name]
        
        # Data format: [[posx, posy, posz], [velx, vely, velz], time]
        data = f"[[{self.pos.x}, {self.pos.y}, {self.pos.z}], [{self.vel.x}, {self.vel.y}, {self.vel.z}], {t}]\n"
        dataset.write(data)
        
        self.index += 1
        if self.index >= epoch:
            dataset.flush()
            os.fsync(dataset.fileno())
            
            self.index = 0

# Loading all Bodies
with open(f'./datasets/{dataset_name}/Planets.json') as f:
    planets = json.load(f)
    
    for name in planets:
        body = Body(
            name = name,
            mass = planets[name]["mass"],
            size = vector(planets[name]["size"][0], planets[name]["size"][1], planets[name]["size"][2]),
            position = vector(planets[name]["pos"][0], planets[name]["pos"][1], planets[name]["pos"][2]),
            velocity = vector(planets[name]["vel"][0], planets[name]["vel"][1], planets[name]["vel"][2])
            )
        bodies.append(body)

print("Simulation Initiated.")
start = perf_counter()

try:
    while t <= tl:
        rate(xt/dt) # Disable for max simulation speed
        
        for body in bodies: 
            body.update()
            body.log()
            
        t += dt
        
except KeyboardInterrupt:
    for dataset in datasets: dataset.close()
    print("Simulation Terminated.")
    print(f"Completed in {perf_counter() - start}s")