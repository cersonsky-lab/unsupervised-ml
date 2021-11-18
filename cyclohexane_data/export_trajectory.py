import os
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
    default="md.out",
)

args = parser.parse_args()

fn = args.filename

files = list(reversed([f"trajectory_{i}.xyz" for i in range(10)]))
start = 0
i = 0

for f in files:
    if os.path.exists(f):
        i = int(f[11:-4])
        start = i * 10000
        break

print(f"Starting at frame {start}.")
frames = read(fn, f"{start}:")

print(f"{len(frames)} to dump")

for frame in frames:
    frame.info["energy_eV"] = frame.get_total_energy()
    frame.arrays["forces_eV_per_au"] = frame.get_forces()

total_len = len(frames) + start
if total_len > 10000:
    for j in range(i, total_len // 10000 + 1):
        write(f"trajectory_{j}.xyz", frames[(j - i) * 10000 : (j - i + 1) * 10000])
else:
    write("trajectory.xyz", frames)

write("final.xyz", frames[-1])
