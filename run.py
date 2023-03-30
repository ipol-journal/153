#!/usr/bin/env python3

import subprocess
import argparse

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("transform_type", type=str)
ap.add_argument("robust", type=str)
ap.add_argument("lambd", type=int)
ap.add_argument("scales", type=int)
ap.add_argument("zfactor", type=float)
ap.add_argument("epsilon", type=float)
ap.add_argument("sigma", type=int)

args = ap.parse_args()

#run algo
p0 = subprocess.run(['add_noise', 'input_0.png', 'input_0.png', str(args.sigma)])

p1 = subprocess.run(['add_noise', 'input_1.png', 'input_1.png', str(args.sigma)])

p2 = subprocess.run(['inverse_compositional_algorithm', 'input_0.png', 'input_1.png',
                    '-f', 'transform.mat', '-t', str(args.transform_type), '-n', str(args.scales), '-z', str(args.zfactor),
                    '-e', str(args.epsilon), '-r', str(args.robust), '-l', str(args.lambd),
                    '-v', '-i', 'mat_0.mat', '-s', str(args.sigma)])

p3 = subprocess.run(['generate_output', 'input_0.png', 'input_1.png', 'transform.mat', 'mat_0.mat',
                    str(args.robust), str(args.lambd)])