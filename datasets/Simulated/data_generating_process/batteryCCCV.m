//Battery CCCV Short Circuit Simulation with varying

//start = 1e10, end = 0.002, 
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC1.csv", "Delimiter", ",");


//start = 1e9, end = 0.02
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC2.csv", "Delimiter", ",");

//start = 1e8, end = 0.2
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC3.csv", "Delimiter", ",");

//start = 1e7, end = 2
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC4.csv", "Delimiter", ",");

//start = 1e5, end = 0.00002
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC5.csv", "Delimiter", ",");


//start = 1e4, end = 0.0002
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC6.csv", "Delimiter", ",");




//start = 1e3, end = 0.00002
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC7.csv", "Delimiter", ",");


//start = 1e2, end = 0.00002
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC8.csv", "Delimiter", ",");


//start = 1e1, end = 0.000002
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC9.csv", "Delimiter", ",");


//start = 1e0, end = 0.000002
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC10.csv", "Delimiter", ",");


//start = 1e6, end = 0.001
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC11.csv", "Delimiter", ",");

//start = 1e6, end = 0.0005
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC12.csv", "Delimiter", ",");

//start = 1e6, end = 0.0001
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC13.csv", "Delimiter", ",");

//start = 1e6, end = 0.00005
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC14.csv", "Delimiter", ",");

//start = 1e6, end = 0.00001
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC15.csv", "Delimiter", ",");

//start = 1e6, end = 0.000005
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC16.csv", "Delimiter", ",");

//start = 1e6, end = 0.000001
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC17.csv", "Delimiter", ",");

//start = 1e6, end = 0.0000005
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC18.csv", "Delimiter", ",");

//start = 1e6, end = 0.005
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC19.csv", "Delimiter", ",");


//start = 1e6, end = 0.01
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC20.csv", "Delimiter", ",");



//start = 1e6, end = 0.05
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC21.csv", "Delimiter", ",");

//start = 1e6, end = 0.1
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC22.csv", "Delimiter", ",");



//start = 1e6, end = 0.04
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC23.csv", "Delimiter", ",");



//start = 1e6, end = 0.03
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC24.csv", "Delimiter", ",");



//start = 1e6, end = 0.025
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC25.csv", "Delimiter", ",");



//start = 1e6, end = 0.02
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC26.csv", "Delimiter", ",");

//start = 1e6, end = 0.015
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC27.csv", "Delimiter", ",");

//start = 1e6, end = 0.0475
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC28.csv", "Delimiter", ",");

//start = 1e6, end = 0.055
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC29.csv", "Delimiter", ",");

//start = 1e6, end = 0.075
T = BatteryCCCVSimlog.Battery_Table_Based.cell_temperature.series.values;
I = BatteryCCCVSimlog.Battery_Table_Based.i.series.values;
power_dissi = BatteryCCCVSimlog.Battery_Table_Based.power_dissipated.series.values;
V = BatteryCCCVSimlog.Battery_Table_Based.v.series.values;
vrc = BatteryCCCVSimlog.Battery_Table_Based.vrc1.series.values;
df = horzcat(T, I, V, power_dissi, vrc);
writematrix(df, "batteryCCCV_SC30.csv", "Delimiter", ",");



