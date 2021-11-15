A python implementation for simplex method
The current implementation uses simplex method and is able to resolve maximisation problems and it's capable of identifying cases of unbound solutions

To operate the program you must type the question into the input
I will use example 1 on page 26 of optimisation theory and application to explain the input format

Example 1:
max z= 60_x1+ 90_x2 + 300x_3

x_1 + x_2 + x_3 <= 600
x_1 + 3x_2 <= 600
2x_1 + x_3 <= 600

to input the example you must follow the given structure type in the coefficients of the problem  :

3 3         #number of constraints, number of variables
60 90 300   #objective function
1 1 1 600   #constraint 1
1 3 0 600   #constraint 2
2 0 1 900   #constraint 3

note: the must be no empty lines in the input line or else you'll get an error

After inputting the coefficients into the input.txt  by simply running main.py you'll generate two txt files:
log.txt     which shows the details of the problem and the working steps
solution    shows the final output and the optimal values achieved


Mini Research Project:
for the mini research project part i have implemented an algorithm for the identifying cases of unbound solutions, i have included the coefficiants for
the input of an unbounded question in my question.txt document simply copy and paste the coefficiants into the input.txt and my program should be able 
to analyse problem and display full functionality for dealing with unbounded problems