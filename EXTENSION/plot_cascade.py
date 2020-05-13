from pathlib import Path
import matplotlib.pyplot as plt 
import json
import os 

plt.style.use('ggplot')
cwd = os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = os.path.join(cwd, "Cascades")

OUTPUT_DIR = os.path.join(os.path.dirname(cwd), 'Plots')
with os.scandir(INPUT_DIR) as it:
    for entry in it:
        if entry.name.endswith('.json') and entry.is_file():
            fig, ax = plt.subplots(figsize=(10,6))
            stream = Path(entry.name).stem
            if stream == "TF":
                stream = "Adaptive"
            elif stream == "BL":
                stream = "Baseline"
            file_path = os.path.join(INPUT_DIR, entry.name)
            with open(file_path) as f:
                data = json.load(f)
            node_count = 0
            for thresh, statuses in data.items():
                iteration = list()
                percentage_infected = list()
                for status in statuses:
                    node_count = sum(status['node_count'].values())
                    iteration.append(status['iteration'])
                    infected = status['node_count']['1']
                    percentage_infected.append((infected/node_count) * 100)
                ax.plot(iteration, percentage_infected, label=f"Threshold {thresh}")

            ax.set_title(f"{stream} stream: Diffusion of information with high-degree seed")
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Percentage of nodes infected")
            ax.set_ylim(0,100)
            ax.legend()
            out_file = os.path.join(OUTPUT_DIR, f"{stream}_cascade.png")
            plt.savefig(out_file)
