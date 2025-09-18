# naturaDock Product Requirements Document (PRD)

**Version:** 1.0 (MVP Scope)
**Date:** 2025-09-15
**Owner:** Abdellah Chaaibi

## 1. Goals and Background Context

### 1.1. Goals
*   **Accessibility Achievement:** Create a user-friendly pipeline accessible to researchers without computational expertise, reducing technical barriers in natural product drug discovery.
*   **Workflow Automation:** Develop an end-to-end automated system that handles data preparation, docking, and results analysis without manual intervention.
*   **Reproducibility Standard:** Establish a fully reproducible, open-source workflow that meets FAIR data principles and scientific publication standards.
*   **Academic Portfolio:** Generate a substantial project demonstrating computational biology skills for PhD applications.

### 1.2. Background Context
Researchers, especially in academic and natural products labs, struggle with a fragmented landscape of complex, disparate, and expensive computational tools. This creates a high technical barrier, requires significant command-line expertise, and leads to a lack of reproducibility across workflows. The cumulative impact is a slower, less efficient discovery process that excludes many researchers from the benefits of computational screening. naturaDock aims to solve this by offering an accessible, validated, and reproducible alternative.

### 1.3. Change Log
| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
| 2025-09-15 | 1.0 | First full draft based on stakeholder-provided summary | Abdellah Chaaibi |

## 2. Requirements

### 2.1. Functional Requirements
*   **FR1:** The system must accept compound libraries in SDF, SMILES, and MOL2 file formats.
*   **FR2:** The system must accept protein structures in the standard PDB file format.
*   **FR3:** The system must perform 3D conformer generation for input compounds using RDKit.
*   **FR4:** The system must allow users to specify binding site coordinates for the docking grid.
*   **FR5:** The system must integrate AutoDock Vina as the docking engine.
*   **FR6:** The system must support parallel processing to leverage multiple CPU cores for docking.
*   **FR7:** The system must generate a ranked list of compounds in both CSV and XLSX formats.
*   **FR8:** The system must generate publication-quality plots, including docking score distributions and enrichment analysis.
*   **FR9:** The entire workflow must be controllable via a single Command-Line Interface (CLI) that accepts a configuration file.
*   **FR10:** The system must provide a Docker container to ensure a fully reproducible environment with all dependencies.
*   **FR11:** The system must implement checkpointing to allow resumption of interrupted runs.

### 2.2. Non-Functional Requirements
*   **NFR1 (Performance):** The system must process a library of >10,000 compounds in under 24 hours on a standard 8-core system.
*   **NFR2 (Usability):** A new user must be able to execute their first successful screening within 2 hours using the provided tutorials.
*   **NFR3 (Reliability):** The pipeline must have a job failure rate of less than 5% for properly formatted inputs.
*   **NFR4 (Compatibility):** The Dockerized pipeline must be functional on Linux, macOS, and Windows.
*   **NFR5 (Reproducibility):** The pipeline must produce identical results when run with the same inputs, parameters, and random seeds across different environments.
*   **NFR6 (Resource-Efficiency):** The pipeline must run successfully on systems with 16 GB of RAM or less.

## 3. User Interface Design Goals

The V1 product will be exclusively a **Command-Line Interface (CLI)** tool. All user interaction will be through the command line, specified by arguments and a configuration file. There will be no Graphical User Interface (GUI). The focus is on creating a clear, well-documented CLI that is easy to use for both primary and secondary target users. All visual outputs will be in the form of static, publication-quality plots (e.g., PNG files).

## 4. Technical Assumptions

*   **Primary Language:** Python 3.10+
*   **Core Libraries:** RDKit, BioPython, AutoDock Vina, Pandas, NumPy/SciPy, Matplotlib/Seaborn.
*   **Deployment:** The system will be deployed exclusively via a Docker container.
*   **Architecture:** The workflow will be a modular, script-based pipeline where each stage (prep, docking, analysis) can be run independently and uses checkpoints.
*   **Testing:** Quality assurance will be handled via a CI testing pipeline (e.g., GitHub Actions) with unit and end-to-end tests.

## 5. Epic & Story Breakdown

### Epic 1: Core Pipeline Foundation
*Goal: Establish the project structure and implement a working, single-molecule docking workflow.*
*   **Story 1.1:** As a developer, I want to set up the Git repository, project structure, and Dockerfile, so that we have a reproducible development environment.
*   **Story 1.2:** As a researcher, I want to provide a protein PDB file and a single compound file (SDF/MOL2) as input, so that the pipeline can validate and prepare them for docking.
*   **Story 1.3:** As a researcher, I want the pipeline to automatically generate the docking grid box based on my specified coordinates, so that Vina knows where to perform the docking.
*   **Story 1.4:** As a developer, I want to create a wrapper script that executes a single AutoDock Vina docking run and captures the output score and pose.

### Epic 2: High-Throughput Screening & Analysis
*Goal: Scale the pipeline to handle large libraries and provide meaningful analysis of the results.*
*   **Story 2.1:** As a researcher, I want the pipeline to process an entire library of thousands of compounds in parallel, so that I can complete a screen in a reasonable amount of time.
*   **Story 2.2:** As a developer, I want to implement a results aggregation module that collects and parses the scores and poses from all completed docking jobs.
*   **Story 2.3:** As a researcher, I want the pipeline to rank all docked compounds by their Vina score and export the list to a CSV file, so that I can identify the top candidates.
*   **Story 2.4:** As a researcher, I want the pipeline to generate a statistical summary and distribution plot of the docking scores, so that I can assess the quality of the screening run.

### Epic 3: Usability, Documentation & Validation
*Goal: Make the pipeline robust, user-friendly, and scientifically valid.*
*   **Story 3.1:** As a user, I want a master CLI script that accepts a single configuration file, so that I can easily define and execute a complete workflow.
*   **Story 3.2:** As a new user, I want comprehensive documentation and a tutorial with an example dataset, so that I can learn to use the pipeline quickly.
*   **Story 3.3:** As a user, I want the pipeline to provide robust logging and clear error messages, so that I can troubleshoot any problems that occur.
*   **Story 3.4:** As a developer, I want to implement end-to-end benchmark tests against known datasets (e.g., a DUD-E subset), so that we can validate the scientific accuracy of the pipeline.

## 6. Next Steps
*   **Immediate Actions:** Final PRD approval, begin detailed architecture design, set up the Git repository, and start development on the "Data Input & Preprocessing" module.
*   **PM Handoff:** This PRD defines the V1 MVP. The approved scope will now guide all architecture and development work.

---

## A. Repository & community hygiene
* **LICENSE:** Add a clear OSS license file (e.g., MIT or Apache-2.0).
* **CONTRIBUTING.md:** Pull request process, code style, review expectations, how to run tests locally.
* **CODE_OF_CONDUCT.md:** Standard contributor behaviour guidance.
* **ISSUE_TEMPLATE / PULL_REQUEST_TEMPLATE:** Encourage reproducible bug reports and standardized PRs.
* **CHANGELOG.md:** Follow Keep a Changelog format; update on each release.

## B. CI / CD & automated checks
* **CI pipeline (GitHub Actions):** steps for `lint` (flake8/mypy), `unit tests`, `docker build`, and a small `end-to-end` smoke test using the example dataset.
* **Security checks:** Dependabot or equivalent dependency vulnerability alerts; container image scan as part of CI.
* **Release automation:** tag → build Docker image → create GitHub Release artifact.

## C. Testing & Quality targets
* **Unit test coverage target:** 80–90% (set exact target in repo).
* **End-to-end smoke test:** automatic run in CI using a tiny benchmark (100 compounds) to verify the pipeline works.
* **Benchmarking tests:** separate scripts to run reproducible perf tests (time / RAM) for 1k, 10k compounds on target hardware.

## D. Config schema & CLI examples
**Sample config (YAML)**
```yaml
input:
  compounds: /path/to/library.sdf
  protein: /path/to/target.pdb
docking:
  vina_executable: /usr/bin/vina
  center: [x,y,z]
  size: [sx,sy,sz]
  exhaustiveness: 8
resources:
  n_cores: 8
  batch_size: 64
output:
  outdir: ./results/
  formats: [csv, xlsx, png]
reproducibility:
  random_seed: 42
checkpoint:
  enabled: true
```

**CLI example:**
```
naturaDock run --config config.yaml
```

## E. Outputs & filesystem layout
**Standardized output layout:**
```
/results/
  /raw_docking/
  /poses/
  /ranked/
  /plots/
  run_manifest.yaml
  pipeline_log.json
```
* Add a `run_manifest.yaml` that records parameters, git commit, docker image hash, dataset provenance.

## F. Provenance & FAIR metadata
* For each run include a `metadata.yaml` capturing:
  - dataset source and version (URL and citation)
  - preprocessing steps applied
  - git commit hash + Docker image digest
  - random seed and parameter values
* Add a short subsection describing how to cite the tool in publications.

## G. Benchmarking & validation protocol (QA)
* **Datasets:** DUD-E subset, curated ChEMBL actives (document exact subsets in repo).
* **Metrics:** ROC AUC, enrichment factor (EF) @1%, @5%, @10%, and bootstrap confidence intervals.
* **Statistical plan:** Use bootstrapping to compute 95% CI; report p-values for comparisons to baseline (Vina alone).
* **Output:** Standardized CSV/PNG naming for benchmark results stored under `/results/benchmarks/`.

## H. Reproducibility & randomness
* `random_seed` must be configurable and documented for all stochastic components (e.g., RDKit conformer generation).
* Require Docker image digest and git commit hash be recorded in run metadata for reproducibility.

## I. Logging, monitoring & diagnostics
* **Structured logs:** JSON logs with levels (INFO/DEBUG/WARN/ERROR) and timestamps.
* **Verbosity flags:** `--verbose`, `--quiet`.
* **Failed item report:** CSV of skipped/failed compounds + error messages.
* **Profiling hooks:** option to output basic CPU/RAM statistics per batch (for benchmarking).

## J. Performance / resource management
* Add a benchmarking script that measures average seconds per compound, memory usage, and total runtime.
* Add `--max-memory` or `--max-threads` guard and tuning guidance in docs.

## K. Security, licensing & legal
* **Dependency policy:** pin all dependencies in `requirements.txt` and Dockerfile; use reproducible builds.
* **Security statement:** clarify that user data is not transmitted externally; provide guidance for proprietary libraries.
* **Disclaimer:** predictions are computational and require experimental validation (not for clinical decisions).

## L. Definition of Done (DoD) per Epic
For each Epic include a checklist:
* Code merged into main
* Unit tests passing
* CI green
* Docs updated
* Example dataset validated
* Docker image built and smoke test passed

## M. Release & roadmap
* Use semantic versioning and a release checklist: tag, build, changelog, Docker push, create GitHub Release.
* Suggested releases: `v0.1 (dev)` → `v1.0 (MVP)` → `v1.1 (bugfix/benchmarks)`.

## N. Support & maintenance
* Recommended support channels: GitHub Issues for bugs/feature requests, FAQ, `examples/` folder, `MAINTAINERS.md` describing contacts and responsibilities.

---