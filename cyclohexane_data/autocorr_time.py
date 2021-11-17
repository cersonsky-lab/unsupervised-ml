import numpy as np
from ase.io import read, write
import argparse

parser = argparse.ArgumentParser(
    description="Determine the decorrelated frames of a simulation"
)
parser.add_argument(
    "-f",
    "filename",
    metavar="f",
    type=str,
    nargs="+",
    help="filename to read",
    default="trajectory.xyz",
)
parser.add_argument(
    "-t",
    "threshold",
    metavar="T",
    type=float,
    nargs=1,
    help="threshold to determine tao",
    default=0.1,
)

args = parser.parse_args()

traj = read(args.filename, ":")
energy = np.array([a.info["energy_eV"] for a in traj])
ac_thresh = args.threshold


def autocorr(x):
    ac = np.zeros(len(x) // 2)
    xm = np.mean(x)
    for k in range(len(x) // 2):
        ac[k] = (
            sum([(x[i] - xm) * (x[i + k] - xm) for i in range(len(x) - k)])
            / sum([(x[i] - xm) for i in range(len(x) - k)]) ** 2
        )
    return ac


ace = autocorr(energy)
tao = np.where(ace < ac_thresh)[0][0]

ac_frames = traj[::tao]

write("ac_trajectory.xyz", traj[::tao])
