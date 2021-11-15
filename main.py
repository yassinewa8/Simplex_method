import numpy as np
import sys

# def main():
#     name = input("1 or 0")
#     if name == '1':
#         maximisation()
#         print('Initiating maximisation')
#     elif name == '0':
#         print("Initiating minimisation")
#         minimisation()
#     else:
#         print("invalid input returing to main")
#         main()

with open('input.txt', "r") as input_txt:
    data = input_txt.read() #read file as string
input_txt = open('log.txt', 'w')
sys.stdout = input_txt
print('////////////////////////input file detected////////////////////////')
print(data)

#split lines to get a list of lines then split every character in a single line
data = data.splitlines()
LP_Arguments = []
for line in data:
    LP_Arguments.append(line.split())
#convert LP_Arguments from a list of strings to list of arays with a float data type
for i in range(len(LP_Arguments)):
    LP_Arguments[i] = np.asarray(LP_Arguments[i]).astype(float)
print('////////////////////////identifying contents////////////////////////')
#obtain the number of constraint and number of variables
number_of_constraint = int(LP_Arguments[0][0])
number_of_variables = int(LP_Arguments[0][1])
print('Number of Constraint =', number_of_constraint, '\nNumber of Variable =', number_of_variables)
#remove the constrains and vriable to make things easier
LP_Arguments.pop(0)
#Extracting objective function
objecetive_function = LP_Arguments[0]
objecetive_function = np.append(objecetive_function, [0] * number_of_constraint)
print('Objective Function =' , objecetive_function)
LP_Arguments.pop(0) #drop objective funtion

LP_Arguments = np.asarray(LP_Arguments) # convet to array
Constants = LP_Arguments[:, -1] #take last collum
print("Constants = ", Constants)

constrain_matrix = np.delete(LP_Arguments, -1, axis=1)
constrain_matrix = np.concatenate((constrain_matrix, np.identity(number_of_constraint)), axis=1)
print("constrain_matrix =\n", constrain_matrix)

###########################################################################################################

initial_variabls = []

slack_variabls = []

for i in range(1, number_of_variables+1):
    initial_variabls.append("x{}".format(i))  # Create decision variables.

for i in range(number_of_constraint):
    slack_variabls.append("x{}".format(number_of_variables+i+1))  # Create slack variables.


coefficient_format = initial_variabls + slack_variabls

variable_index = list(range(1, number_of_variables + 1))
slack_index = list(range(number_of_variables + 1, number_of_variables + number_of_constraint + 1))

variable_index_original = np.copy(variable_index)
slack_index_original = np.copy(slack_index)

print("coefficient_format = {", *coefficient_format, "}")
print("initial_variabls = {", *initial_variabls, "}", "\nslack_variabls = {", *slack_variabls, "}")
######################################################################################################
#initial values
Basic_coefficient = np.identity(number_of_constraint)
Basic_coefficient_inv = np.linalg.inv(Basic_coefficient)
cb = np.array([[0]] * number_of_constraint)
cb_transpose = np.transpose(cb)
kapa = np.dot(cb_transpose, Basic_coefficient_inv)  # dummy variable
M_inverse = np.identity(number_of_constraint + 1)
initial_resulting_matrix = np.dot(M_inverse, np.concatenate(([0], Constants), 0))

z = np.array([0] * len(objecetive_function))
Object_Row_slacks = [0] * number_of_constraint
a = 1
E = []
xb = Constants
entering_var_candidates = [-1]
np.set_printoptions(precision=4, suppress=True)
##########################################################################################################
def solution():
    output = open('solution.txt', 'w')
    sys.stdout = output
    print("////////////////////////Solution//////////////////////////////////////////////")
    print("Optimal Solution has been achieved. \nNumber of loops:{}".format(a))
    print("Optimal value of", current_sol[0], "has been reached.")
    print("Initial Variables:", end=" ")
    for i in range(number_of_variables):
        print("x{} = {:.2f}".format((i + 1), original_variables[i]), end=" ")
    print()
    print("Slack Variables:", end=" ")
    for i in range(number_of_constraint):
        print("s{} = {:.2f}".format((i + 1), slack_variables[i]), end=" ")
    print()
    output.close()
#############################################################################################################
def unbound_solution():
    output = open('solution.txt', 'w')
    sys.stdout = output
    print("////////////////////////Solution//////////////////////////////////////////////")
    print("This solution is unbounded. \nNumber of loops:{}".format(a))
    print("Initial Variables:", end=" ")
    for i in range(number_of_variables):
        print("x{} = {:.2f}".format((i + 1), original_variables[i]), end=" ")
    print()
    print("Variables:", end=" ")
    for i in range(number_of_constraint):
        print("x{} = {:.2f}".format((i + number_of_variables + 1), slack_variables[i]), end=" ")
    print()

    print("Final Solution =", current_sol[0], end=" + ")
    for i in range(len(variable_index) - 1):
        print("({:.2f})x{}".format(*-entering_var_candidates[variable_index[i] - 1], variable_index[i]), end=" + ")
    print("({:.2f})x{}".format(*-entering_var_candidates[variable_index[-1] - 1], variable_index[-1]))
    output.close()
###########################################################################################################
while 1:

    print("////////////////////////////////////////////////////////////////////////////////")
    print("{}.loop".format(a))
    print("Objective Row Sacks Variables =", *Object_Row_slacks)
    I_m = np.identity(number_of_constraint)
    if a == 1:
        print("Objective_Row\t", end=" ")
        for i in range(number_of_variables):
            print("x{}:".format(variable_index[i]), objecetive_function[i], "\t", end=" ")
        print()
    # Define entering variable.
    entering_var_candidates = []
    carpan = np.concatenate(([1], kapa[0]))
    for i in range(len(objecetive_function)):
        zj_cj = np.transpose(np.concatenate(([[-objecetive_function[i]]], [constrain_matrix[:, i]]), axis=1))
        entering_var_candidates.append(np.dot(carpan, zj_cj))
    entering_var_candidates = np.asarray(entering_var_candidates)
    if a > 1:
        print("Objective_Row\t", end=" ")
        for i in range(number_of_variables):
            print("x{}:{}".format(variable_index[i], -entering_var_candidates[variable_index[i] - 1]), "\t", end=" ")
        print()
##########################################################################################################################
# For optimal solution:
    if all(i >= 0 for i in np.around(entering_var_candidates, decimals=4)):
        slack_dictionary = {}
        original_variables = [0] * number_of_variables
        slack_variables = [0] * number_of_constraint
        for i in range(len(slack_index)):
            slack_dictionary[slack_index[i]] = (Solution_Column[i])
            # np.round(Solution_Column[i])
        for var in variable_index_original:
            if var in slack_dictionary:
                original_variables[var - 1] = (slack_dictionary[var])
        for var in slack_index_original:
            if var in slack_dictionary:
                slack_variables[var - slack_index_original[0]] = slack_dictionary[var]
        solution()
        break
########################################################################################################
    entering_var = min(entering_var_candidates)
    entering_var_idx = np.argmin(entering_var_candidates)
    p = entering_var_idx
    print("Pivot Row is x{}".format(entering_var_idx + 1))
    t = np.dot(Basic_coefficient_inv, constrain_matrix[:, p])
    print("Pivot Row Value ={}".format(t))
    # Check if the solution is unbounded.Condition: if every elements of t lower than zero,
    #  solution is unbounded.
################################################################################################
    #for unbound solutions
    if all(i <= 0 for i in np.round(t, decimals=4)):
        print("Original:", end=" ")
        slack_dictionary = {}
        original_variables = [0] * number_of_variables
        slack_variables = [0] * number_of_constraint
        for i in range(len(slack_index)):
            slack_dictionary[slack_index[i]] = float(Solution_Column[i])
        for var in variable_index_original:
            if var in slack_dictionary:
                original_variables[var - 1] = (slack_dictionary[var])
        for var in slack_index_original:
            if var in slack_dictionary:
                slack_variables[var - slack_index_original[0]] = slack_dictionary[var]
        sol = M_inverse[1:, 1:]
        print()
        unbound_solution()
        break
####################################################################################################
    positive_values = t[t > 0]
    idx_of_positive_values = np.array(np.where(t > 0)).reshape((-1, 1))
    ratio = xb[idx_of_positive_values]
    ratio = ratio / t[idx_of_positive_values]
    print("Ratio", end=" ")
    for i in range(len(ratio)):
        print("x{}:".format(slack_index[idx_of_positive_values[i][0]]), "{:3.4f}\t".format(*ratio[i]), end="")
    print()
    leaving_var_idx = idx_of_positive_values[np.argmin(ratio)]
    leaving_var = (number_of_variables + 1) + leaving_var_idx
    print("Pivot Row is the least non-negative ratio\nChoosing ratio x{}".format(*leaving_var))
    q = leaving_var_idx
    eta_vector = -t
    eta_vector[q] = 1
    eta_vector = eta_vector / t[q]
    I_m[:, q] = eta_vector.reshape((-1, 1))
    eta_matrix = I_m
    Basic_coefficient_inv = np.dot(eta_matrix, Basic_coefficient_inv)
    cb[q] = objecetive_function[p]
    cb_transpose = np.transpose(cb)
    kapa = np.dot(cb_transpose, Basic_coefficient_inv)
    M_inverse = np.concatenate(([[1]], kapa), axis=1)
    dim = len(M_inverse[0]) - 1
    dim = np.array([[0]] * dim)
    expanded_B_inv = np.concatenate((dim, Basic_coefficient_inv), axis=1)
    M_inverse = np.concatenate((M_inverse, expanded_B_inv))
    # print current solution is:
    current_sol = np.dot(M_inverse, np.concatenate(([0], Constants)))
    xb = np.dot(eta_matrix, xb)
    # Organize variables
    N_copy = np.copy(initial_variabls)
    B_copy = np.copy(slack_variabls)
    initial_variabls[int(p)] = B_copy[int(q)]
    slack_variabls[int(q)] = N_copy[int(p)]
    N_idx_copy = np.copy(variable_index)
    B_idx_copy = np.copy(slack_index)
    variable_index[int(p)] = B_idx_copy[int(q)]
    slack_index[int(q)] = N_idx_copy[int(p)]
    Solution_Column = current_sol[1:]
    print("Solution_Column =", Solution_Column)
    Object_Row_slacks = kapa
    a += 1
input_txt.close()
# main()