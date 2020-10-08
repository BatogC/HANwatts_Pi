import time

data0 = "231.79%230.78%231.00%0.00%0.00%0.00%0.00%231.46%50.01%1601895079%2%No ID%"
data = "229.86%228.68%226.20%0.00%0.00%14.22%0.00%0.00%50.04%1601897947%1%No ID%"
index = []
for i in range(len(data)):
        if (data[i] == '%'):
            index.append(i)
V1 = float(data[:index[0]])
V2 = float(data[index[0]+1:index[1]])
V3 = float(data[index[1]+1:index[2]])
I1 = float(data[index[2]+1:index[3]])
I2 = float(data[index[3]+1:index[4]])
I3 = float(data[index[4]+1:index[5]])
P = float(data[index[5]+1:index[6]])
E = float(data[index[6]+1:index[7]])
F = float(data[index[7]+1:index[8]])
Time = int(data[index[8]+1:index[9]])
SocketID = int(data[index[9]+1:index[10]])
UserID = data[index[10]+1:index[11]]

print(V1)
print(I1)

print(int(round(time.time())))

dataSend = [[V1, V2, V3, I1, I2, I3, P, E, F, UserID, Time]]
print(dataSend)
dataSend.append([21, V2, V3, I1, I2, I3, P, E, F, SocketID, Time])
print(dataSend)
input()