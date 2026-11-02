import numpy as np
import matplotlib.pyplot as plt
import random
from pathlib import Path

from Assignment import generate_points, inside_intersection

#Create Figures folder if it doesn't exist
figures_dir = Path(__file__).resolve().parent / "Figures"
figures_dir.mkdir(exist_ok=True)

#Parameters
k = 1
R = 0.75
r = 0.4
N = 300

xc, yc, zc = 0, 0, 0

rng = random.Random(42)

#Sphere surface
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 40)

x_sphere = k * np.outer(np.cos(u), np.sin(v))
y_sphere = k * np.outer(np.sin(u), np.sin(v))
z_sphere = k * np.outer(np.ones_like(u), np.cos(v))

#Torus surface
theta, phi = np.meshgrid(
    np.linspace(0, 2 * np.pi, 70),
    np.linspace(0, 2 * np.pi, 35)
)

x_torus = (R + r * np.cos(phi)) * np.cos(theta)
y_torus = (R + r * np.cos(phi)) * np.sin(theta)
z_torus = r * np.sin(phi)

#Generate random points
points = generate_points(k, R, r, N, rng=random.Random(42))

inside_points = []
outside_points = []

for x, y, z in points:
    if inside_intersection(x, y, z, k, R, r):
        inside_points.append((x, y, z))
    else:
        outside_points.append((x, y, z))

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(
    x_sphere, y_sphere, z_sphere,
    color='royalblue',
    alpha=0.18,
    edgecolor='darkblue',
    linewidth=0.20
)

ax.plot_surface(
    x_torus, y_torus, z_torus,
    color='orange',
    alpha=0.22,
    edgecolor='darkorange',
    linewidth=0.20
)

# Plot sampled points
if inside_points:
    x, y, z = zip(*inside_points)
    ax.scatter(x, y, z, color='green', s=12,
               label='Inside intersection')

if outside_points:
    x, y, z = zip(*outside_points)
    ax.scatter(x, y, z, color='red', s=8,
               label='Outside intersection')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Sphere–Torus Intersection (k=1, R=0.75, r=0.4)', fontsize=14)

ax.set_box_aspect((1, 1, 1))
ax.legend()

plt.tight_layout()
plt.savefig(figures_dir / "sphere_torus_3d.png", dpi=300, bbox_inches='tight')
plt.show()