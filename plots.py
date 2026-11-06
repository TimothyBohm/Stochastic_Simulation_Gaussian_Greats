import matplotlib.pyplot as plt
import random
from Assignment import monte_carlo_volume
from pathlib import Path
from matplotlib.ticker import FuncFormatter
from Assignment import run_experiments
import numpy as np
from Assignment import (
    generate_points,
    generate_logistic_points,
    monte_carlo_volume
)

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