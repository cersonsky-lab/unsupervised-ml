from ase.io import read, write
import numpy as np
import argparse

parser = argparse.ArgumentParser(
    description="Export a trajectory from a QE md simulation"
)
parser.add_argument(
    "-f",
    "--filename",
    metavar="f",
    type=str,
    nargs="+",
    help="filename to read",
    default=["md.out"],
)

parser.add_argument(
    "-o",
    "--output",
    metavar="f",
    type=str,
    nargs="+",
    help="filename to export",
    default=["trajectory.xyz"],
)

parser.add_argument("-t", "--trim", type=int, nargs=1, default=None)

args = parser.parse_args()

fn = args.filename[0]
ofn = args.output[0]
frames = read(fn, ":")

if args.trim is not None:
    frames = frames[: args.trim[0]]

for frame in frames:
    frame.info["energy_eV"] = frame.get_total_energy()
    try:
        frame.arrays["forces_eV_per_au"] = frame.get_forces()
    except RuntimeError:
        pass
    frame.positions -= np.mean(frame.positions, axis=0)
    frame.positions += np.diag(frame.cell) / 2

print(fn, len(frames))
write(ofn, frames)
