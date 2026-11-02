import random
import math

#Random Number Generator
rng = random.Random(42)

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

def box_volume(bounds):
    volume = 1.0
    for low, high in bounds:
        volume *= high - low
    return volume


def estimate_standard_error(inside, N, box_volume):
    #The standard error is given by the formula: SE = Volume_box * sqrt(p_hat * (1 - p_hat) / N)
    p_hat = inside / N
    return box_volume * math.sqrt(p_hat * (1 - p_hat) / N) 


def generate_points(k, R, r, N, xc=0, yc=0, zc=0, rng=None):
    #Generate N uniformly distributed points within the bounding box
    if rng is None:
        rng = random.Random()

    x_bounds, y_bounds, z_bounds = bounding_box(k, R, r, xc, yc, zc)

    points = []
    for i in range(N):
        x = rng.uniform(*x_bounds)
        y = rng.uniform(*y_bounds)
        z = rng.uniform(*z_bounds)
        points.append((x, y, z))

    return points


def generate_logistic_points(k, R, r, N, x0, y0, z0, m=3.8, xc=0, yc=0, zc=0):
    x_bounds, y_bounds, z_bounds = bounding_box(k, R, r, xc, yc, zc)

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
                       x0=0.1, y0=0.2, z0=0.3, xc=0, yc=0, zc=0, rng=None):
    
    if method == "random":
        points = generate_points(k, R, r, N, xc, yc, zc, rng)
    elif method == "logistic":
        points = generate_logistic_points(k, R, r, N, x0, y0, z0, xc, yc, zc)
    else:
        raise ValueError("Method must be 'random' or 'logistic'")

    inside = 0 #initial value of points inside

    for x, y, z in points: 
        if inside_intersection(x, y, z, k, R, r, xc, yc, zc):
            inside += 1
    
    #Calculate the volume of the bounding box
    bounds = bounding_box(k, R, r, xc, yc, zc)
    volume_box = box_volume(bounds)
    
    #Estimate standard error for independent uniform samples
    if method == "random":
        error = estimate_standard_error(inside, N, volume_box)
    else:
        error = None
    
    # Estimate the intersection volume
    volume = volume_box * inside / N
    
    return volume, error

def run_experiments(k, R, r, sample_sizes, xc=0, yc=0, zc=0, rng=None):
    results = []

    if rng is None:
        rng = random.Random(42)

    for N in sample_sizes:
        #Use same seed for reproducibility and fairness in convergence graphs
        experiment_rng = random.Random(46) 
        volume, error = monte_carlo_volume(k, R, r, N, xc=xc, yc=yc, zc=zc, rng=experiment_rng)
        results.append((N, volume, error))

    return results

