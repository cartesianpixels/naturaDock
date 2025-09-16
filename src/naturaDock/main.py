import argparse
import logging
import toml
from pathlib import Path

from naturaDock.log_config import setup_logging

from naturaDock.preprocessing.protein import (
    load_protein,
    validate_protein,
    prepare_protein,
    define_binding_site,
)
from naturaDock.preprocessing.compounds import (
    load_compounds,
    filter_compounds,
    generate_conformers,
    prepare_compounds,
)
from naturaDock.docking.parallel_dock import run_parallel_docking
from naturaDock.analysis.results import aggregate_results
from naturaDock.analysis.export import rank_and_export_results
from naturaDock.analysis.statistics import generate_statistics


def main():
    """Main function to run the naturaDock pipeline."""
    parser = argparse.ArgumentParser(
        description="naturaDock - A virtual screening pipeline for natural products."
    )
    parser.add_argument(
        "--config", type=Path, help="Path to a TOML configuration file."
    )
    parser.add_argument(
        "-p",
        "--protein",
        type=Path,
        help="Path to the protein PDB file.",
    )
    parser.add_argument(
        "-l",
        "--ligands",
        type=Path,
        help="Path to the compound library file (SDF, SMI, MOL2).",
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="Path to the output directory."
    )
    parser.add_argument(
        "--size_x",
        type=float,
        default=60.0,
        help="Size of the binding site in the X dimension.",
    )
    parser.add_argument(
        "--size_y",
        type=float,
        default=60.0,
        help="Size of the binding site in the Y dimension.",
    )
    parser.add_argument(
        "--size_z",
        type=float,
        default=60.0,
        help="Size of the binding site in the Z dimension.",
    )
    parser.add_argument(
        "--max_mol_weight",
        type=float,
        default=500.0,
        help="Maximum molecular weight for compound filtering.",
    )
    parser.add_argument(
        "--max_rotatable_bonds",
        type=int,
        default=10,
        help="Maximum number of rotatable bonds for compound filtering.",
    )
    parser.add_argument(
        "--min_logp",
        type=float,
        default=-5.0,
        help="Minimum logP for compound filtering.",
    )
    parser.add_argument(
        "--max_logp",
        type=float,
        default=5.0,
        help="Maximum logP for compound filtering.",
    )
    parser.add_argument(
        "--export_format",
        type=str,
        default="csv",
        help="Format for exporting ranked results (csv or xlsx).",
    )
    parser.add_argument(
        "--skip_analysis",
        action="store_true",
        help="Skip the analysis step.",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=None,
        help="Number of parallel workers for docking.",
    )
    parser.add_argument(
        "--log-file", type=Path, default="naturaDock.log", help="Path to the log file."
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging to the console."
    )

    args = parser.parse_args()

    # Load config file if provided
    if args.config:
        config = toml.load(args.config)
        parser.set_defaults(**config)
        args = parser.parse_args()

    # Validate required arguments
    required_args = ["protein", "ligands", "output"]
    for arg in required_args:
        if not getattr(args, arg):
            raise ValueError(f"Missing required argument: --{arg}")

    # Create output directory if it doesn't exist
    args.output.mkdir(exist_ok=True)

    # 1. Load and validate protein
    print("--- Loading and Validating Protein ---")
    protein_structure = load_protein(args.protein)
    validate_protein(args.protein)

    # 2. Prepare protein
    print("--- Preparing Protein ---")
    protein_pdbqt = args.output / f"{args.protein.stem}.pdbqt"
    prepare_protein(args.protein, protein_pdbqt)

    # 3. Load and filter compounds
    print("--- Loading and Filtering Compounds ---")
    compounds = load_compounds(args.ligands)
    filtered_compounds = filter_compounds(
        compounds,
        max_mol_weight=args.max_mol_weight,
        max_rotatable_bonds=args.max_rotatable_bonds,
        min_logp=args.min_logp,
        max_logp=args.max_logp,
    )

    # 4. Generate conformers
    print("--- Generating Conformers ---")
    compounds_with_conformers = generate_conformers(filtered_compounds)

    # 5. Prepare compounds
    print("--- Preparing Compounds ---")
    prepared_compounds_dir = args.output / "prepared_compounds"
    prepared_compounds_dir.mkdir(exist_ok=True)
    prepared_compounds = prepare_compounds(
        compounds_with_conformers, prepared_compounds_dir
    )

    # 6. Define binding site
    binding_site = define_binding_site(
        protein_structure,
        size_x=args.size_x,
        size_y=args.size_y,
        size_z=args.size_z,
    )

    # 7. Run docking
    print("--- Running Docking ---")
    docking_results_dir = args.output / "docking_results"
    docking_results_dir.mkdir(exist_ok=True)

    run_parallel_docking(
        protein_pdbqt=protein_pdbqt,
        prepared_compounds=prepared_compounds,
        binding_site=binding_site,
        docking_results_dir=docking_results_dir,
        num_workers=args.num_workers,
    )

    # 8. Run analysis
    if not args.skip_analysis:
        print("--- Running Analysis ---")
        results_df = aggregate_results(docking_results_dir)
        if not results_df.empty:
            rank_and_export_results(results_df, args.output, args.export_format)
            generate_statistics(results_df, args.output)
        else:
            print("No results to analyze.")

    print("--- naturaDock pipeline finished ---")


if __name__ == "__main__":
    main()
