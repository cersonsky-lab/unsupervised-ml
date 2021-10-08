from ase.io import read, write
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
    default="md.out",
)

args = parser.parse_args()

fn = args.filename
frames = read(fn, ":")

for frame in frames:
    frame.info["energy_eV"] = frame.get_total_energy()
    frame.arrays["forces_eV_per_au"] = frame.get_forces()

write("trajectory.xyz", frames)
write("final.xyz", frames[-1])
