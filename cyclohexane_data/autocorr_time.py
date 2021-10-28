import numpy as np
from ase.io import read, write
import argparse

parser = argparse.ArgumentParser(
    description="Determine the decorrelated frames of a simulation"
)
parser.add_argument(
    "-f",
    "--filename",
    metavar="f",
    type=str,
    nargs="+",
    help="filename to read",
    default="trajectory.xyz",
)
parser.add_argument(
    "-t",
    "--threshold",
    metavar="T",
    type=float,
    nargs=1,
    help="threshold to determine tao",
    default=None,
)

args = parser.parse_args()

traj = read(args.filename, ":")
energy = np.array([a.info["energy_eV"] for a in traj])


def autocorr(x):
    ac = np.zeros(len(x) // 2)
    xm = np.mean(x)
    xmm = np.multiply(xm, x)
    xdenom = [0, *np.cumsum(x - xm) ** 2.0]

    for k in range(len(x) // 2):
        ac[k] = (
            np.sum(
                np.multiply(x[: len(x) - k], x[k:])
                - xmm[: len(x) - k]
                - xmm[k:]
                + xm ** 2.0
            )
            / xdenom[len(x) - k]
        )
    return ac


ace = autocorr(energy)

if args.threshold is not None:
    ac_thresh = args.threshold
else:
    from matplotlib import pyplot as plt

    plt.loglog(ace)
    plt.show()

    ac_thresh = float(input("Threshold?\t"))
tao = np.where(ace < ac_thresh)[0][0]

ac_frames = traj[::tao]

write("ac_trajectory.xyz", traj[::tao])
