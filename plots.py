import matplotlib.pyplot as plt
import random
from Assignment import monte_carlo_volume
from pathlib import Path
from matplotlib.ticker import FuncFormatter
from Assignment import run_experiments

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