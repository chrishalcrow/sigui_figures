# SpikeInterface-GUI paper figures

A repo allowing you to reproduce the Windows seen in the Figures in ["SpikeInterface-GUI: efficient and versatile spike sorting visualization and curation"](https://zenodo.org/records/19481268).

The Figures in the paper use real data from Harry Clark, Wolf De Wulf and Bri Vandrey while they were in the [Nolan Lab](https://nolansurmelilab.github.io/). In this repo, you can recreate the Figures using synthetic data.

To reproduce the SpikeInterface-GUI windows seen in the paper, first download this repo and change directory into it:

```
git clone https://github.com/chrishalcrow/sigui_figures.git
cd sigui_figures
```

Then to generate, e.g., Figure 2, run:

```
uv run fig2/fig2.py
```

If you do not have [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed, you can first add this package into a venv, and run e.g. `python fig2/fig2.py`.
