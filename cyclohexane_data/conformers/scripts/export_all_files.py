from ase.io import read, write

for dir in ['chair','boat','half-boat','twist-boat','half-chair','planar']:
	frames = read(f'{dir}/md.out',':')

	for frame in frames:
	    frame.info['energy_eV'] = frame.get_total_energy()
	    frame.arrays['forces_eV_per_au'] = frame.get_forces()

	write(f'{dir}.xyz', frames)
