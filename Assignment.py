import random
import math

#Geometry Checks
def inside_sphere(x, y, z, k):
    return x**2 + y**2 + z**2 <= k**2

def inside_torus(x, y, z, R, r, xc=0, yc=0, zc=0):
    return ((math.sqrt((x-xc)**2 + (y-yc)**2) - R)**2 + (z-zc)**2 <= r**2)

def inside_intersection(x, y, z, k, R, r, xc=0, yc=0, zc=0):
    return (inside_sphere(x, y, z, k) and inside_torus(x, y, z, R, r, xc, yc, zc))


def bounding_box(k, R, r, xc=0, yc=0, zc=0):
    outer_radius = R + r

    x_bounds = (max(-k, xc - outer_radius), min(k, xc + outer_radius))
    y_bounds = (max(-k, yc - outer_radius), min(k, yc + outer_radius))
    z_bounds = (max(-k, zc - r), min(k, zc + r))

    return x_bounds, y_bounds, z_bounds


def generate_points(k, R, r, N):
    x_bounds, y_bounds, z_bounds = bounding_box(k, R, r) # generate random points

    points = []
    for i in range(N): 
        x = random.uniform(*x_bounds) # equivalent to random.uniform(x_bounds[0], x_bounds[1])
        y = random.uniform(*y_bounds) # the choice of uniform distribution is quite obvious
        z = random.uniform(*z_bounds)
        points.append((x, y, z))
    return points


def generate_logistic_points(k, R, r, N, x0, y0, z0, m=3.8):
    x_bounds, y_bounds, z_bounds = bounding_box(k, R, r)

    X, Y, Z = x0, y0, z0
    points = []

    for i in range(N):
        X = m * X * (1 - X)
        Y = m * Y * (1 - Y)
        Z = m * Z * (1 - Z)

        # Transform values from [0, 1] into the bounding box we created, that is now we transfrom the 0,1 numbers to numbers
        #that go from edge to edge
        x = x_bounds[0] + X * (x_bounds[1] - x_bounds[0])
        y = y_bounds[0] + Y * (y_bounds[1] - y_bounds[0])
        z = z_bounds[0] + Z * (z_bounds[1] - z_bounds[0])

        points.append((x, y, z))

    return points

def monte_carlo_volume(k, R, r, N, method="random",
                       x0=0.1, y0=0.2, z0=0.3):
    
    if method == "random":
        points = generate_points(k, R, r, N)

    elif method == "logistic":
        points = generate_logistic_points(k, R, r, N, x0, y0, z0)

    else:
        raise ValueError("Method must be 'random' or 'logistic'")

    inside = 0 #initial value of points inside

    for x, y, z in points:
        sphere = x**2 + y**2 + z**2 <= k**2 #check wether the point is inside the sphere
        torus = (math.sqrt(x**2 + y**2) - R)**2 + z**2 <= r**2 #check wether the point is inside the torus

        if sphere and torus:
            inside += 1 #so we essentially add 1 for every point inside

    x_bounds, y_bounds, z_bounds = bounding_box(k, R, r)

    box_volume = (
        (x_bounds[1] - x_bounds[0])
        * (y_bounds[1] - y_bounds[0])
        * (z_bounds[1] - z_bounds[0])
    )

    return box_volume * inside / N

print("Case (a):", monte_carlo_volume(1, 0.75, 0.4, 100000))
print("Case (b):", monte_carlo_volume(1, 0.5, 0.5, 100000))
