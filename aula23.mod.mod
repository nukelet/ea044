reset;

var x12 binary;
var x13 binary;
var x24 binary;
var x25 binary;
var x35 binary;
var x46 binary;
var x56 binary;

minimize v : 4*x12 + 3*x13 + 3*x24 + 2*x25 + 4*x35 + 2*x46 + 2*x56;

subject to no1: x12 + x13 = 1;
subject to no2: x24 + x25 - x12 = 0;
subject to no3: x35 - x13 = 0;
subject to no4: x46 - x24 = 0;
subject to no5: x56 - x25 - x35 = 0;
subject to no6: -x46 - x56 = -1;

option solver cplex;
solve v;

display x12, x13, x24, x25, x35, x46, x56;