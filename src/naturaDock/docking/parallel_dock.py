
import concurrent.futures
from pathlib import Path
from tqdm import tqdm
import psutil

from .vina_dock import run_vina_docking

def run_parallel_docking(
    protein_pdbqt: Path,
    prepared_compounds: list[Path],
    binding_site: dict,
    docking_results_dir: Path,
    num_workers: int | None = None,
):
    """
    Runs AutoDock Vina docking in parallel for a list of compounds.

    Args:
        protein_pdbqt: Path to the prepared protein file in PDBQT format.
        prepared_compounds: List of paths to prepared compound files in PDBQT format.
        binding_site: Dictionary defining the docking box (center and size).
        docking_results_dir: Path to the directory to write the docked pose output files.
        num_workers: The number of parallel workers to use. If None, it will default to 
                     the number of available CPU cores.
    """
    if num_workers is None:
        num_workers = psutil.cpu_count(logical=False)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for compound_pdbqt in prepared_compounds:
            output_pdbqt = (
                docking_results_dir / f"{compound_pdbqt.stem}_docked.pdbqt"
            )
            future = executor.submit(
                run_vina_docking,
                protein_pdbqt=protein_pdbqt,
                compound_pdbqt=compound_pdbqt,
                binding_site=binding_site,
                output_pdbqt=output_pdbqt,
            )
            futures.append(future)

        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(prepared_compounds),
            desc="Running parallel docking",
        ):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred during docking: {e}")
