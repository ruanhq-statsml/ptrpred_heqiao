//
//

//setting1: slope -10k, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Battery_Table_Based.H.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope1.csv", "Delimiter", ",");

//setting1: slope -100k, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Battery_Table_Based.H.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope2.csv", "Delimiter", ",");

//setting1: slope -3k, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Battery_Table_Based.H.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope4.csv", "Delimiter", ",");


//setting1: slope -5k, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Controlled_Temperature_Source.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope3.csv", "Delimiter", ",");


//setting1: slope -300, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Controlled_Temperature_Source.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope5.csv", "Delimiter", ",");


//setting1: slope -750, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Controlled_Temperature_Source.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope6.csv", "Delimiter", ",");


//setting1: slope -500, start time 20k, initial output 1e7
T1 = BatteryCCCVSimlog.Battery_Table_Based.H.T.series.values;
Q1 = BatteryCCCVSimlog.Controlled_Temperature_Source.Q.series.values;
AT1 = BatteryCCCVSimlog.Controlled_Temperature_Source.A.T.series.values;
I1 = BatteryCCCVSimlog.Controlled_Current_Source.i.series.values;
V1 = BatteryCCCVSimlog.Controlled_Current_Source.v.series.values;
df1 = horzcat(T1, Q1, AT1, I1, V1);
df1 = array2table(df1);
colnames = ["T1", "Q1", "AT1", "I1", "V1"];
df1.Properties.VariableNames = colnames;
writetable(df1, "batteryCCCV_slope7.csv", "Delimiter", ",");

//give me a line by line justification for the exchangeability condition for this permutation test.

