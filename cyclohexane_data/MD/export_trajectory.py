import numpy as np

from ase import Atoms
from ase.io import write


def get_energies(fn):
    lines = list(open(fn))
    new_energies = np.array(
        [float(line.split()[-2]) for line in lines if line.startswith("!")]
    )
    return new_energies


def get_coordinates(fn, position_flag="ATOMIC_POSITIONS (angstrom)\n", last=True):
    lines = open(fn).readlines()

    for li, l in enumerate(lines):
        if "lattice parameter (alat) " in l:
            lattice_param = float(l.split()[-2]) * 0.5292
            lattice = lattice_param * np.ones(3)
        if "CELL_PARAMETERS" in l:
            lattice = np.array(
                [ll.split() for ll in lines[li + 1: li + 4]], dtype=float
            )
        if "number of atoms" in l or ("nat" in l and "terminated" not in l):
            n_atoms = int(l.split()[-1].strip(","))
            if "nat" not in l:
                break
    try:
        _ = lattice
    except:
        raise AssertionError(f"Lattice not found in {fn}")

    position_starts = [i + 1 for i,
                       v in enumerate(lines) if v == position_flag]

    positions = np.array(
        [[l.split() for l in lines[p: p + n_atoms]] for p in position_starts]
    )
    if len(position_starts) > 1:
        coords = np.array(positions[:, :, 1:], dtype=float)
        species = np.array(positions[:, :, 0], dtype=str)

    else:
        coords = np.array(positions[:, :, 1:], dtype=float)
        species = np.array(positions[:, :, 0], dtype=str)

    if last:
        return lattice, coords[-1], species[-1]
    else:
        return np.array([lattice for c in coords]), coords, species


def get_forces(fn, nat):

    lines = list(open(fn))
    starts = [
        i + 2
        for i, line in enumerate(lines)
        if "Forces acting on atoms (cartesian axes, Ry/au):" in line
    ]

    return np.array(
        [
            [np.array(line.split()[-3:], dtype=float)
             for line in lines[i: i + nat]]
            for i in starts
        ]
    )


def export_trajectory(fn):
    lattice = None
    coords = None
    species = None

    lattice, coords, species = get_coordinates(fn, last=False)

    energies = get_energies(fn)
    forces = get_forces(fn, len(coords[0]))

    if lattice is not None:
        frames = [
            Atoms(cell=l, positions=c, symbols=s)
            for l, c, s in zip(lattice, coords, species)
        ]
        for i in range(len(frames)):
            frames[i].info["energy_ryd"] = energies[i]
            frames[i].arrays["forces_ryd_per_au"] = forces[i]

        write("trajectory.xyz", frames)
    else:
        input(f"FAILED")


if __name__ == "__main__":
    import sys

    if sys.argv[1].endswith("out"):
        export_trajectory(sys.argv[1])
