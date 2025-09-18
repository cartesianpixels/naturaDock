# Technology Stack

This document outlines the official technology stack for the naturaDock V1 project.

- **Primary Language:** Python 3.10+
- **Core Libraries:**
    - RDKit: Molecular handling and descriptor calculation.
    - BioPython: Protein structure parsing and manipulation.
    - AutoDock Vina: Core docking engine (executed via subprocess).
    - Pandas: Data manipulation and analysis.
    - NumPy/SciPy: Numerical and statistical operations.
    - Matplotlib/Seaborn: Static plot generation for reports.
    - Py3Dmol: Generation of 3D molecular visualizations.
- **Deployment:** Docker

*Note: Specific versions for all libraries will be pinned in `requirements.txt` to ensure full reproducibility.*
