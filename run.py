#!/usr/bin/env python3

import subprocess
import argparse
import sys
tabulate_path = "/usr/lib/python3/dist-packages"
sys.path.append(tabulate_path)
from tabulate import tabulate


# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("transform_type", type=int)
ap.add_argument("robust", type=int)
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
                    '-v', '-i', 'input_2.mat', '-s', str(args.sigma)])

p3 = subprocess.run(['generate_output', 'input_0.png', 'input_1.png', 'transform.mat', 'input_2.mat',
                    str(args.robust), str(args.lambd)])


#create tables
with open('transform.mat', 'r') as f, open('input_2.mat', 'r') as f1:
    computed_trans = f.readlines()[1]
    gT_trans = f1.readlines()[1]

# Extract values from the strings
computed_trans_values = [float(value) for value in computed_trans.split()]
gt_trans_values = [float(value) for value in gT_trans.split()]

# Check if both sets of values are equal
values_equal = computed_trans_values == gt_trans_values

if values_equal:
    # Compute the absolute difference if both sets of values are equal
    difference = [abs(computed - gT) for computed, gT in zip(computed_trans_values, gt_trans_values)]
else:
    # Assign difference value of -1 if both sets of values are not equal
    difference = "-"


# Create header
head = ["Transformation", "Computed transformation (p)", "Ground truth transformation (p')", "Error |p'-p|"]

if args.transform_type == 8:
    Transform = "Homography: (h00, h01,..., h21)"
elif args.transform_type == 4:
    Transform = "Similarity: (tx,ty,a,b)"
elif args.transform_type == 3:
    Transform = "Euclidean: (tx,ty,θ)"
elif args.transform_type == 2:
    Transform = "Translation: (tx,ty)"
elif args.transform_type == 6:
    Transform = "Affinity: (tx,ty,a00,a01,a10,a11)"


# Assign data
mydata = [
    [Transform, computed_trans, gT_trans, difference]
]

with open('table1.txt', 'w') as file:
  file.write(tabulate(mydata, headers=head, tablefmt="grid", numalign="center"))


with open('stdout.txt', 'r') as file:
    content = file.readlines()
    for line in content:
        if "Time=" in line:
            Time = line.split('=')[1].strip()
        if "d(Hx,H'x)=" in line:
            Error = line.split('=')[1].strip()
        if "RMSE=" in line:
            RMSE = line.split('=')[1].strip()
        if "Computed Matrix=" in line:
            computed_matrix = line.split('=')[1].split()
        if "Original Matrix=" in line:
            gt_matrix = line.split('=')[1].split()


# Create header2
head2 = ["", "Added noise", "RMSE", "Error d(Hgtxi,Hxi)", "Time"]

# Assign data2
mydata2 = [
    ["Results", args.sigma, RMSE, Error, Time]
]

#display table
with open('table2.txt', 'w') as file:
  file.write(tabulate(mydata2, headers=head2, tablefmt="grid", numalign="center"))


# Format the matrix values
format_computed_matrix = "\n".join(["\t".join(computed_matrix[i:i+3]) for i in range(0, len(computed_matrix), 3)])
format_gT_matrix = "\n".join(["\t".join(gt_matrix[i:i+3]) for i in range(0, len(gt_matrix), 3)])

# Write the formatted matrices to text files
with open("computed_matrix_file", "w") as file:
    file.write("Computed Matrix:\n")
    file.write(format_computed_matrix)
    file.write("\n\n")
    file.write("Ground Truth:\n")
    file.write(format_gT_matrix)
