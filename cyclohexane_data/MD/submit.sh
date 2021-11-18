#!/bin/bash
#SBATCH --job-name="ML_unsup-cyclohexanes"
#SBATCH --partition=Slim
#SBATCH -n 24
#SBATCH -N 1
#SBATCH -t 12-00:00:00

set -u

cd /home/cersonsk/git_repos/unsupervised-ml/cyclohexane_data/MD

export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:/home/cersonsk/miniconda3/lib
mpirun -np 24 /home/cersonsk/q-e-qe-6.2.0/bin/pw.x -plumed < md.in | tee md.out
