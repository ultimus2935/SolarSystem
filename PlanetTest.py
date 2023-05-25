from vpython import *

t = 0.00
xt = 1e+8 # Simulation Speed
dt = 10 # Time Increment

G = 6.674011e-11

def createBody(
    name: str, mass: float, size:float, 
    position: vector, velocity: vector = vector(0, 0, 0), 
    color: color = color.white, texture: textures = None, 
    trail_color: color = color.white, shininess: float = 0, trail: bool = False
    ):
    
    body = sphere(
        pos = position, size = size, 
        color = color, texture = texture, trail_color = trail_color,
        shininess = shininess, make_trail = trail
        )
    
    body.tag = label(
        pos = body.pos, text = f"<i>{name}</i>\n{mag(body.pos):e}", font = 'sans', 
        xoffset = 30, yoffset = 30, height = 12, border = 4, line = False
        )  
    
    body.mass = mass; body.name = name
    body.vel = velocity; body.acc = vector(0, 0, 0)
    
    return body

bodies = []

def gravitationalAcceleration(mainBody):
    mainBody.acc = vector(0, 0, 0)
    for otherBody in [body for body in bodies if body != mainBody]:
        radius = otherBody.pos - mainBody.pos
        mainBody.acc += norm(radius)*(otherBody.mass/mag2(radius))
        
    mainBody.acc *= G
    
def updateLabel(body):
    body.tag.pos = body.pos
    body.tag.text = f"<i>{body.name}</i>\n{mag(body.pos):e}"

def updateBody(body):
    gravitationalAcceleration(body)
    body.vel += body.acc*dt
    body.pos += body.vel*dt
    
    updateLabel(body)

def updateBodies(bodies):
    for body in bodies: updateBody(body)

sun = createBody(
    name = "Sun",
    mass = 1.9891e+30,
    size = 6.957e+8*vector(1, 1, 1),
    position = vector(0, 0, 0),
    color = vector(0.889, 0.748, 0.000),
    trail = True,
    trail_color = color.yellow
    )
bodies.append(sun)

earth = createBody(
    name = "Earth",
    mass = 5.97219e+24,
    size = 6.3781e+6*vector(1, 1, 1),
    position = vector(-1.471e+11, 0, 0),
    velocity = vector(0, -3.029e+4, 0),
    texture = textures.earth,
    trail = True,
    trail_color = color.blue
    )
bodies.append(earth)
        
while True:
    rate(xt/dt) # Disable for max simulation speed
    updateBodies(bodies)
    
    t += dt