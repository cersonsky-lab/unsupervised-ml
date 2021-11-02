#!/bin/bash
#SBATCH --job-name="ML_unsup-cyclohexanes"
#SBATCH --partition=Slim
#SBATCH -n 24
#SBATCH -N 1
#SBATCH -t 96:00:00

set -u

cd /home/cersonsk/git_repos/unsupervised-ml/cyclohexane_data/MD

mpirun -np 24 /home/cersonsk/q-e-qe-6.7.0/bin/pw.x -i md.in | tee md.out
