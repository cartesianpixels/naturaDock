# Source Tree Structure

The project will follow a standard Python project layout:

```
naturaDock/
├── .github/                # CI/CD workflows
├── data/
│   ├── compounds/          # Example compound libraries
│   └── proteins/           # Example protein files
├── docs/
│   ├── architecture/       # Architecture and standards documents
│   ├── brief.md
│   └── prd.md
├── notebooks/              # Jupyter notebooks for experimentation
├── src/
│   └── naturaDock/         # Main application source code
│       ├── analysis/       # Results aggregation and analysis
│       ├── docking/        # AutoDock Vina execution and management
│       ├── preprocessing/  # Compound and protein preparation
│       ├── visualization/  # Report and image generation
│       └── main.py         # CLI entry point
├── tests/                  # Unit and integration tests
├── .gitignore
├── Dockerfile
└── README.md
```
