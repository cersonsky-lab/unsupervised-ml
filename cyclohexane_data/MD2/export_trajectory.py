from ase.io import read, write

frames = read('md.out',':')

for frame in frames:
    frame.info['energy_eV'] = frame.get_total_energy()
    frame.arrays['forces_eV_per_au'] = frame.get_forces()

write('trajectory.xyz', frames)
