import sys

import numpy as np
from ase.io import read

dir = sys.argv[1]

md_start = list(open("./scripts/md.in"))

frame = read(f"{dir}/init.xyz")
frame.positions -= np.mean(frame.positions)
frame.positions += [7.5, 7.5, 7.5]

with open(f"{dir}/md.in", "w") as mdf:
    for l in md_start:
        mdf.write(l)
    for s, p in zip(frame.symbols, frame.positions):
        mdf.write("{}\t{}\t{}\t{}\n".format(s, *p))

    mdf.write("\nCELL_PARAMETERS angstrom\n")
    mdf.write("15.0 0.0 0.0\n0.0 15.0 0.0\n0.0 0.0 15.0\n")
