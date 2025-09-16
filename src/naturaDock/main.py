import argparse
import toml
from pathlib import Path

from naturaDock.preprocessing.protein import (
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
from naturaDock.docking.vina_dock import run_vina_docking


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
        "--center_x",
        type=float,
        help="X coordinate of the binding site center.",
    )
    parser.add_argument(
        "--center_y",
        type=float,
        help="Y coordinate of the binding site center.",
    )
    parser.add_argument(
        "--center_z",
        type=float,
        help="Z coordinate of the binding site center.",
    )
    parser.add_argument(
        "--size_x",
        type=float,
        default=20.0,
        help="Size of the binding site in the X dimension.",
    )
    parser.add_argument(
        "--size_y",
        type=float,
        default=20.0,
        help="Size of the binding site in the Y dimension.",
    )
    parser.add_argument(
        "--size_z",
        type=float,
        default=20.0,
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

    args = parser.parse_args()

    # Load config file if provided
    if args.config:
        config = toml.load(args.config)
        parser.set_defaults(**config)
        args = parser.parse_args()

    # Validate required arguments
    required_args = ["protein", "ligands", "output", "center_x", "center_y", "center_z"]
    for arg in required_args:
        if not getattr(args, arg):
            raise ValueError(f"Missing required argument: --{arg}")

    # Create output directory if it doesn't exist
    args.output.mkdir(exist_ok=True)

    # 1. Validate protein
    print("--- Validating Protein ---")
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
        center_x=args.center_x,
        center_y=args.center_y,
        center_z=args.center_z,
        size_x=args.size_x,
        size_y=args.size_y,
        size_z=args.size_z,
    )

    # 7. Run docking
    print("--- Running Docking ---")
    docking_results_dir = args.output / "docking_results"
    docking_results_dir.mkdir(exist_ok=True)

    for compound_pdbqt in prepared_compounds:
        output_pdbqt = docking_results_dir / f"{compound_pdbqt.stem}_docked.pdbqt"
        run_vina_docking(
            protein_pdbqt=protein_pdbqt,
            compound_pdbqt=compound_pdbqt,
            binding_site=binding_site,
            output_pdbqt=output_pdbqt,
        )

    print("--- naturaDock pipeline finished ---")


if __name__ == "__main__":
    main()
