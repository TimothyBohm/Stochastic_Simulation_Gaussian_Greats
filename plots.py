import matplotlib.pyplot as plt
import numpy as np
import random
from Assignment import monte_carlo_volume
from pathlib import Path
from matplotlib.ticker import FuncFormatter
<<<<<<< Updated upstream
from Assignment import run_experiments
import numpy as np
from Assignment import (
    generate_points,
    generate_logistic_points,
    monte_carlo_volume
)
=======
from Assignment import run_experiments, run_mixture_experiments
>>>>>>> Stashed changes

#Create Figures folder if it doesn't exist
figures_dir = Path(__file__).resolve().parent / "Figures"
figures_dir.mkdir(exist_ok=True)

sample_sizes = [100, 200, 300, 400, 500,750, 1000,2000,3000,4000, 5000, 10000, 15000, 20000, 25000, 35000, 50000, 75000, 100000]

#Run experiments for Question 1
results_a = run_experiments(1, 0.75, 0.4, sample_sizes)
results_b = run_experiments(1, 0.5, 0.5, sample_sizes)

#Extract results
N_a, volumes_a, errors_a = zip(*results_a)
N_b, volumes_b, errors_b = zip(*results_b)

#Setting up and running the experiments for exercise 3(a)
results_3a = run_experiments(1, 0.75, 0.4, sample_sizes, zc=0.1, rng=random.Random(69))

# Extract results for exercise 3(a)
N_3a, volumes_3a, errors_3a = zip(*results_3a)

# Run experiments for exercise 3(b) across different p values
p_values = [0.2, 0.5, 0.8]
results_3b = {}
for p in p_values:
    results_3b[p] = run_mixture_experiments(1, 0.75, 0.4, sample_sizes, p=p, xc=0, yc=0, zc=0.1)

#GRAPHS!!!
#Convergence of volume estimates
plt.figure(figsize=(8, 4))

plt.plot(N_a, volumes_a, marker='o', label='Case (a)')
plt.plot(N_b, volumes_b, marker='o', label='Case (b)')

plt.axhline(
    y=volumes_a[-1],
    color='royalblue',
    linestyle='--',
    alpha=0.7,
    label='Case (a): final estimate'
)

plt.axhline(
    y=volumes_b[-1],
    color='darkorange',
    linestyle='--',
    alpha=0.7,
    label='Case (b): final estimate'
)

plt.xscale('log')
plt.xticks([100,500, 1000, 5000, 10000,25000,50000, 100000], ['100', '500', '1k', '5k', '10k', '25k', '50k', '100k'])
plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated intersection volume')
plt.title('Monte Carlo Volume Estimation', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figures_dir / "convergence.png", dpi=300, bbox_inches="tight")
plt.show()


#Standard error versus sample size
plt.figure(figsize=(8, 4))

plt.plot(N_a, errors_a, marker='o', label='Case (a)')
plt.plot(N_b, errors_b, marker='o', label='Case (b)')

plt.xscale('log')
plt.xticks([100,500, 1000, 5000, 10000,25000,50000, 100000], ['100', '500', '1k', '5k', '10k', '25k', '50k', '100k'])
plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated standard error')
plt.title('Monte Carlo Standard Error', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figures_dir / "standard_error.png", dpi=300, bbox_inches="tight")
plt.show()


#Final volume estimates
plt.figure(figsize=(8, 4))

volumes = [volumes_a[-1], volumes_b[-1]]
errors = [errors_a[-1], errors_b[-1]]

bars = plt.bar(
    ['Case (a)', 'Case (b)'],
    volumes,
    yerr=errors,
    capsize=5
)

for bar, volume, error in zip(bars, volumes, errors):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        volume + error + 0.03,
        f'{volume:.5f}',
        ha='center',
        va='bottom'
    )

plt.ylabel('Estimated intersection volume')
plt.title('Intersection Volumes (N = 100,000)', fontsize=14)
plt.ylim(0, max(volumes) * 1.15)
plt.tight_layout()
plt.savefig(figures_dir / "volume_comparison.png", dpi=300, bbox_inches="tight")
plt.show()


<<<<<<< Updated upstream
#Generatew Table for Question 1

# TABLE for Monte Carlo results for Question 1

# Get final results (N = 100,000)
N_a, volume_a, error_a = results_a[-1]
N_b, volume_b, error_b = results_b[-1]

k = 1
R_a, r_a = 0.75, 0.4
R_b, r_b = 0.5, 0.5


box_a = 3.2
box_b = 4.0

# Number of points inside the intersection
inside_a = round(volume_a / box_a * N_a)
inside_b = round(volume_b / box_b * N_b)

# Standard error as a percentage of estimated volume
error_pct_a = error_a / volume_a * 100
error_pct_b = error_b / volume_b * 100

columns = ["Parameter", "Case (a)", "Case (b)"]

data = [
    ["Sphere radius (k)", f"{k}", f"{k}"],
    ["Major radius (R)", f"{R_a}", f"{R_b}"],
    ["Minor radius (r)", f"{r_a}", f"{r_b}"],
    ["Bounding box",
     "[-1,1] x [-1,1] x [-0.4,0.4]",
     "[-1,1] x [-1,1] x [-0.5,0.5]"],
    ["Box volume", f"{box_a}", f"{box_b}"],
    ["Sample size (N)", f"{N_a:,}", f"{N_b:,}"],
    ["Points inside intersection", f"{inside_a:,}", f"{inside_b:,}"],
    ["Estimated volume", f"{volume_a:.6f}", f"{volume_b:.6f}"],
    ["Standard error",
     f"{error_a:.6f} ({error_pct_a:.3f}%)",
     f"{error_b:.6f} ({error_pct_b:.3f}%)"],
    ["Final estimate (V)",
     f"{volume_a:.6f} ± {error_a:.6f}",
     f"{volume_b:.6f} ± {error_b:.6f}"]
]

fig, ax = plt.subplots(figsize=(12, 5))
ax.axis('off')

table = ax.table(
    cellText=data,
    colLabels=columns,
    cellLoc='center',
    loc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8)

for j in range(len(columns)):
    table[(0, j)].set_facecolor('#DCE6F1')
    table[(0, j)].set_text_props(weight='bold')

for j in range(len(columns)):
    table[(len(data), j)].set_facecolor('#E2F0D9')
    table[(len(data), j)].set_text_props(weight='bold')

plt.title("Question 1: Monte Carlo Volume Estimation",
          fontsize=14, pad=20)

plt.savefig(
    figures_dir / "question1_table.png",
    dpi=300,
    bbox_inches='tight'
)
plt.show()


# Question 2

N = 100000
k, R, r = 1, 0.75, 0.4

random_points = generate_points(
    k, R, r, N, rng=random.Random(42)
)

logistic_points = generate_logistic_points(
    k, R, r, N,
    x0=0.1, y0=0.2, z0=0.3
)

# Extract x-coordinates
random_x = [point[0] for point in random_points]
logistic_x = [point[0] for point in logistic_points]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(
    random_x, bins=50, density=True,
    color='royalblue', alpha=0.8
)
axes[0].set_title('Uniform Random Sampling')

axes[1].hist(
    logistic_x, bins=50, density=True,
    color='darkorange', alpha=0.8
)
axes[1].set_title('Logistic Map Sampling (m = 3.8)')

for ax in axes:
    ax.set_xlabel('x-coordinate')
    ax.set_ylabel('Probability density')
    ax.set_xlim(-1, 1)
    ax.grid(alpha=0.2)

plt.suptitle('Question 2: Sampling Distributions', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(figures_dir / 'q2_distributions.png',
            dpi=300, bbox_inches='tight')
plt.show()


#Question 2 Table Method comparison

N = 100000
columns = [
    'Parameter', 'Case (a)', 'Case (b)'
]

data = []

results = []

for R, r in [(0.75, 0.4), (0.5, 0.5)]:

    uniform, se = monte_carlo_volume(
        1, R, r, N,
        method='random',
        rng=random.Random(42)
    )

    logistic, _ = monte_carlo_volume(
        1, R, r, N,
        method='logistic',
        x0=0.1, y0=0.2, z0=0.3
    )

    difference = abs(logistic - uniform)
    percentage = difference / uniform * 100

    results.append((uniform, se, logistic,
                    difference, percentage))

a, b = results

data = [
    ['Sample size', f'{N:,}', f'{N:,}'],
    ['Uniform estimate', f'{a[0]:.6f}', f'{b[0]:.6f}'],
    ['Uniform standard error', f'{a[1]:.6f}', f'{b[1]:.6f}'],
    ['Logistic estimate', f'{a[2]:.6f}', f'{b[2]:.6f}'],
    ['Absolute difference', f'{a[3]:.6f}', f'{b[3]:.6f}'],
    ['Relative difference',
     f'{a[4]:.3f}%', f'{b[4]:.3f}%']
]

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.axis('off')

table = ax.table(
    cellText=data,
    colLabels=columns,
    cellLoc='center',
    loc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8)

for j in range(3):
    table[(0, j)].set_facecolor('#DCE6F1')
    table[(0, j)].set_text_props(weight='bold')

plt.title('Question 2: Sampling Method Comparison', pad=20, fontsize=14)
plt.tight_layout()

plt.savefig(figures_dir / 'q2_table.png',
            dpi=300, bbox_inches='tight')
plt.show()

#Question 3a

# QUESTION 3.a: Convergence with multiple random seeds

sample_sizes = [
    100, 250, 500, 1000, 2500, 5000,
    10000, 20000, 30000, 50000,
    75000, 100000
]

seeds = [42, 123, 456]

cases = [
    ("Centered torus (Q1.a)", 0, "royalblue"),
    ("Shifted torus (Q3.a)", 0.1, "darkorange")
]

plt.figure(figsize=(9, 5))

for label, zc, color in cases:
    final_volumes = []

    for seed in seeds:
        # Restart the generator for each sample size
        results = []

        for N in sample_sizes:
            volume, error = monte_carlo_volume(
                1, 0.75, 0.4, N,
                zc=zc,
                rng=random.Random(seed)
            )
            results.append(volume)

        final_volumes.append(results[-1])

        plt.plot(
            sample_sizes,
            results,
            color=color,
            alpha=0.45,
            linewidth=1.5,
            marker='o',
            markersize=3
        )

    # Average final estimate across the three seeds
    mean_final = np.mean(final_volumes)

    plt.axhline(
        mean_final,
        color=color,
        linestyle='--',
        linewidth=2,
        label=f'{label}: mean at 100k = {mean_final:.4f}'
    )

plt.xscale('log')
plt.xticks(
    [100, 1000, 10000, 100000],
    ['100', '1k', '10k', '100k']
)

plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated intersection volume')
plt.title('Monte Carlo Convergence Across Three Random Seeds', fontsize=14)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    figures_dir / 'q3a_multiple_seeds.png',
    dpi=300,
    bbox_inches='tight'
)
plt.show()
=======



# Exercise 3(b): Convergence and Bias comparison
plt.figure(figsize=(9, 5))

# Reference line for the baseline case (p = 1.0)
plt.plot(N_3a, volumes_3a, marker='o', color='black', linewidth=2, label='Question 3(a) Baseline (p = 1.0)')

# Lines for different values of p from the mixture proposal
colors = {0.2: '#d62728', 0.5: '#ff7f0e', 0.8: '#1f77b4'}
for p in p_values:
    N_mix, vol_mix, _ = zip(*results_3b[p])
    plt.plot(N_mix, vol_mix, marker='o', linestyle='--', color=colors[p], label=f'Mixture p = {p}')

plt.xscale('log')
plt.xticks([100, 500, 1000, 5000, 10000, 25000, 50000, 100000], 
           ['100', '500', '1k', '5k', '10k', '25k', '50k', '100k'])
plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated intersection volume')
plt.title('Mixture Proposal Convergence & Bias', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figures_dir / "mixture_convergence_bias.png", dpi=300, bbox_inches="tight")
plt.show()




# Exercise 3(b): Standard Error comparison
plt.figure(figsize=(9, 5))

# Baseline error of Question 3(a) for reference
plt.plot(N_3a, errors_3a, marker='o', color='black', linewidth=2, label='Question 3(a) Baseline (p = 1.0)')

# Error lines for different values of p from the mixture proposal
colors = {0.2: '#d62728', 0.5: '#ff7f0e', 0.8: '#1f77b4'}
for p in p_values:
    N_mix, _, err_mix = zip(*results_3b[p])
    plt.plot(N_mix, err_mix, marker='o', linestyle='--', color=colors[p], label=f'Mixture p = {p}')

plt.xscale('log')
plt.xticks([100, 500, 1000, 5000, 10000, 25000, 50000, 100000], 
           ['100', '500', '1k', '5k', '10k', '25k', '50k', '100k'])
plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated standard error')
plt.title('Question 3(b): Standard Error vs Sample Size', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figures_dir / "mixture_standard_error.png", dpi=300, bbox_inches="tight")
plt.show()



#THE 3D PLOTS BELOW!!! One which shows the geometry of the boxes B and S, and the other one which shows the MC simulations 
# how the dots are more concentrated in box S:

#3D PLOT 1: Geometry of the sphere, shifted torus, and boxes B and S
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 1. Sphere (k=1)
u = np.linspace(0, 2 * np.pi, 30)
v = np.linspace(0, np.pi, 30)
xs = 1.0 * np.outer(np.cos(u), np.sin(v))
ys = 1.0 * np.outer(np.sin(u), np.sin(v))
zs = 1.0 * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_wireframe(xs, ys, zs, color='blue', alpha=0.15, label='Sphere (k=1)')

# 2. Shifted Torus (R=0.75, r=0.4, zc=0.1)
theta = np.linspace(0, 2 * np.pi, 30)
phi = np.linspace(0, 2 * np.pi, 30)
theta, phi = np.meshgrid(theta, phi)
R, r, zc = 0.75, 0.4, 0.1
xt = (R + r * np.cos(phi)) * np.cos(theta)
yt = (R + r * np.cos(phi)) * np.sin(theta)
zt = zc + r * np.sin(phi)
ax.plot_surface(xt, yt, zt, color='orange', alpha=0.3, edgecolor='none')

# Helper function to draw boxes
def draw_box(ax, bounds, color, label, linestyle='-'):
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = bounds
    corners = np.array([
        [x_min, y_min, z_min], [x_max, y_min, z_min], [x_max, y_max, z_min], [x_min, y_max, z_min], [x_min, y_min, z_min],
        [x_min, y_min, z_max], [x_max, y_min, z_max], [x_max, y_max, z_max], [x_min, y_max, z_max], [x_min, y_min, z_max]
    ])
    ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color=color, linestyle=linestyle, label=label)
    for i in [(1, 6), (2, 7), (3, 8)]:
        ax.plot([corners[i[0], 0], corners[i[1], 0]],
                [corners[i[0], 1], corners[i[1], 1]],
                [corners[i[0], 2], corners[i[1], 2]], color=color, linestyle=linestyle)

# 3. Box B en Box S
from Assignment import bounding_box, small_bounding_box
bounds_B = bounding_box(1, 0.75, 0.4, xc=0, yc=0, zc=0.1)
bounds_S = small_bounding_box(xc=0, yc=0, zc=0.1)

draw_box(ax, bounds_B, color='black', label='Box B (Full)', linestyle='--')
draw_box(ax, bounds_S, color='red', label='Box S (Small)', linestyle='-')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D View: Sphere, Shifted Torus, Box B and Box S', fontsize=13)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(figures_dir / "3d_geometry_boxes.png", dpi=300)
plt.show()

#3D PLOT 2: Monte Carlo Simulations with Mixture Proposal:

from Assignment import generate_mixture_points, inside_intersection

fig2 = plt.figure(figsize=(10, 8))
ax2 = fig2.add_subplot(111, projection='3d')

# Generate a smaller number of points for visualization purposes :)
N_vis = 2500
pts = generate_mixture_points(1, 0.75, 0.4, N_vis, p=0.5, zc=0.1, rng=random.Random(46))

inside_pts = [p for p in pts if inside_intersection(p[0], p[1], p[2], 1, 0.75, 0.4, zc=0.1)]
outside_pts = [p for p in pts if not inside_intersection(p[0], p[1], p[2], 1, 0.75, 0.4, zc=0.1)]

if inside_pts:
    ix, iy, iz = zip(*inside_pts)
    ax2.scatter(ix, iy, iz, color='green', s=6, label=f'Intersection Hits ({len(inside_pts)})')

if outside_pts:
    ox, oy, oz = zip(*outside_pts)
    ax2.scatter(ox, oy, oz, color='gray', alpha=0.15, s=2, label=f'Misses ({len(outside_pts)})')

draw_box(ax2, bounds_S, color='red', label='Box S Boundary', linestyle='-')

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Mixture Sampling Density (N=2,500, p=0.5)', fontsize=13)
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig(figures_dir / "3d_sampling_density.png", dpi=300)
plt.show()
>>>>>>> Stashed changes
