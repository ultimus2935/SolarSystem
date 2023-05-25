# Version 0.3 - Ultimus (23/05/2003)

from vpython import *
import json

# Simulation Dataset Details
dataset_name = "Four-Body Simulation"
replay_rate = 1e+10 # Speed of Replay
skip_rate = 5000 # Number of datapoints to ignore between two rendered datapoints

# List of Body datasets
datasets = {}
with open(f'./datasets/{dataset_name}/Planets.json') as f:
    planets = json.load(f)
    for planet in planets: 
        dataset = open(f'./datasets/{dataset_name}/{planet}.txt')
        datasets[planet] = dataset
        
# List of all Body objects
global bodies
bodies = []

def createBody(
    name: str, mass: float, size:float, 
    pos: vector, velocity: vector = vector(0, 0, 0), 
    color: color = color.white, texture: textures = None, 
    trail_color: color = color.white, shininess: float = 0, trail: bool = False
    ):
    
    body = sphere(
        name = name, pos = pos, size = size, 
        color = color, texture = texture, trail_color = trail_color,
        shininess = shininess, make_trail = trail
        )
    
    body.tag = label(
        pos = body.pos, text = f"<i>{body.name}</i>\n{mag(body.pos):e}", font = 'sans', 
        xoffset = 30, yoffset = 30, height = 12, border = 4, line = False
        )  
    
    body.mass = mass; body.vel = velocity; body.acc = vector(0, 0, 0)
    
    return body

def createBodyBasic(
    name: str, size:float, pos: vector, 
    color: color = color.white, texture: textures = None, 
    trail_radius: float = 0, trail: bool = False,
    trail_color: color = color.white, shininess: float = 0
    ):
    
    body = sphere(
        name = name, pos = pos, size = size, 
        color = color, texture = texture, trail_color = trail_color,
        shininess = shininess, make_trail = trail
        )

    body.tag = label(
        pos = body.pos, text = f"<i>{body.name}</i>\n{mag(body.pos):e}", font = 'sans', 
        xoffset = 40, yoffset = 40, height = 10, border = 2, line = False
        )
    
    return body

def updateBody(body):
    try:
        datapoint = datasets[body.name].readline()
        position = eval(datapoint)
        body.pos = vector(position[0][0], position[0][1], position[0][2])
        
        body.tag.pos = body.pos
        body.tag.text = f"<i>{body.name}</i>\n{mag(body.pos):e}"
        
        for _ in range(skip_rate-1): datasets[body.name].readline()
    
    except EOFError or SyntaxError: 
        for dataset in datasets: dataset.close()
        quit()
    
# Loading all Bodies
with open(f'./datasets/{dataset_name}/Planets.json') as f:
    planets = json.load(f)
    
    for name in planets:
        body = createBodyBasic(
            name = name, 
            size = vector(planets[name]["size"][0], planets[name]["size"][1], planets[name]["size"][2]), 
            pos = vector(planets[name]["pos"][0], planets[name]["pos"][1], planets[name]["pos"][2]),
            color = vector(planets[name]["color"][0], planets[name]["color"][1], planets[name]["color"][2]),
            texture = planets[name]["texture"], trail = planets[name]["trail"],
            trail_color = vector(planets[name]["trail_color"][0], planets[name]["trail_color"][1], planets[name]["trail_color"][2])
            )
        
        bodies.append(body)
       
# Loading Skybox
# skybox = sphere(
#     name = "Skybox", size = 9.461e+14*vector(1, 1, 1), 
#     pos = vector(0, 0, 0), color = color.white, 
#     texture = './textures/background.jpg', shininess = 0
#     )

scene.camera.follow(bodies[2])

while True:
    rate(replay_rate) # Disable for max simulation speed
    
    for body in bodies:
        updateBody(body)
    
while True: rate(30)