import subprocess
import os


def run_vina(receptor, ligand, center, size, out_dir="data/results/"):
    os.makedirs(out_dir, exist_ok=True)
    out_pdbqt = os.path.join(out_dir, "out.pdbqt")
    log_file = os.path.join(out_dir, "log.txt")

    cmd = [
        "vina",
        "--receptor",
        receptor,
        "--ligand",
        ligand,
        "--center_x",
        str(center[0]),
        "--center_y",
        str(center[1]),
        "--center_z",
        str(center[2]),
        "--size_x",
        str(size[0]),
        "--size_y",
        str(size[1]),
        "--size_z",
        str(size[2]),
        "--out",
        out_pdbqt,
        "--log",
        log_file,
    ]
    subprocess.run(cmd)
    return out_pdbqt, log_file
