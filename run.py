#!/usr/bin/env python3

import subprocess
import argparse

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
    print("Absolute Difference:", difference)
else:
    # Assign difference value of -1 if both sets of values are not equal
    difference = "-"


# Create header
head = ["Transformation", "Computed transformation (p)", "Ground truth transformation (p')", "Error |p'-p|"]

# Assign data
mydata = [
    ["Homography: (h00, h01,..., h21)", computed_trans, gT_trans, difference]
]

# Find maximum width for each column
max_widths = [max(len(str(x)) for x in column) for column in zip(*mydata, head)]

# Display table
with open('table1.txt', 'w') as file:
    # Write header
    file.write("|".join(head) + "\n")
    file.write("|".join("-" * width for width in max_widths) + "\n")

    # Write data rows
    for row in mydata:
        file.write("|".join(str(cell).ljust(width) for cell, width in zip(row, max_widths)) + "\n")


with open('stdout.txt', 'r') as f:
    content = f.readlines()
    Time = content[10].split('=')[1]
    RMSE = content[11].split('=')[1]
    Error = content[12].split('=')[1]
    computed_matrix = content[13].split('=')[1].split()
    gt_matrix = content[14].split('=')[1].split()


# Create header2
head = ["", "Added noise", "RMSE", "Error d(Hgtxi,Hxi)", "Time"]

# Assign data2
mydata = [
    ["Results", args.sigma, RMSE, Error, Time]
]

# Find maximum width for each column
max_widths = [max(len(str(x)) for x in column) for column in zip(*mydata, head)]

# Display table2
with open('table2.txt', 'w') as file:
    # Write header2
    file.write("|".join(head) + "\n")
    file.write("|".join("-" * width for width in max_widths) + "\n")

    # Write data2 rows
    for row in mydata:
        file.write("|".join(str(cell).ljust(width) for cell, width in zip(row, max_widths)) + "\n")


# Format the matrix values
format_computed_matrix = "\n".join(["\t".join(computed_matrix[i:i+3]) for i in range(0, len(computed_matrix), 3)])
format_gT_matrix = "\n".join(["\t".join(gt_matrix[i:i+3]) for i in range(0, len(gt_matrix), 3)])

print("Transformation Matrices\n")
# Print the computed matrix
print("\033[1mComputed Matrix:\033[0m")
print(format_computed_matrix)

# Print the computed matrix
print("\033[1mGround Truth:\033[0m")
print(format_gT_matrix)