model;

set N;
var x{N,N} binary;
var u{N} >= 0;
param c{N, N};

minimize v : sum{i in N} sum{j in N} c[1, j]*x[i, j];

subject to res1 {i in N}: sum{j in N} x[i,j] = 1;
subject to res2 {j in N}: sum{i in N} x[i, j] = 1;
subject to res3 {i in N}: x[i, i] = 0;

# subject to res4 {i in N, j in N : i <> j and i > 1 and j > 1}: u[i] - u[j] + card(N)*x[i,j] <= card(N) - 1;
	
option solver cplex;

data;
set N := 1 2 3 4 5;
param c: 1 2 3 4 5 :=
 	1 0 152 227 184 118
	2 152 0 220 201 70
	3 227 220 0 193 203
	4 184 201 193 0 146
	5 118 70 203 146 0;

# param c: 1 2 3 4 5 :=
# 1 0 132 217 164 58
# 2 132 0 290 201 79
# 3 217 290 201 79
# 4 164 201 113 0 196
# 5 58 79 303 196 0;
	
solve;
display v, x;
