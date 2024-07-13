import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


def route(l):
    lu = 0
    for i in range(num - 1):
        lu += distance[l[i]][l[i + 1]]
    lu += distance[l[-1]][l[0]]
    return lu


def plot_route(city, best_route):
    plt.figure()
    plt.scatter(city[:, 0], city[:, 1], c='blue', marker='o', label='Cities')
    for i in range(len(best_route) - 1):
        plt.plot([city[best_route[i]][0], city[best_route[i + 1]][0]],
                 [city[best_route[i]][1], city[best_route[i + 1]][1]], 'k-', lw=1)
    plt.plot([city[best_route[-1]][0], city[best_route[0]][0]],
             [city[best_route[-1]][1], city[best_route[0]][1]], 'k-', lw=1)
    plt.title('TSP Path')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend()
    plt.show()


df = pd.read_csv('oliver30.tsp', skiprows=6, sep=" ", header=None)
num = len(df) - 1
city_x = df[1][:num]
city_y = df[2][:num]
city = np.array(list(zip(city_x, city_y)))

distance = np.zeros([num, num])
for i in range(num):
    for j in range(num):
        distance[i][j] = np.sqrt((city[i][0] - city[j][0]) ** 2 + (city[i][1] - city[j][1]) ** 2)

NP = 200
NG = 5000
F = 0.5
CR = 0.3
changdu = []
lujing = []

city_num = num
x_new = np.zeros([NP, city_num])
pi_old = np.zeros([NP, city_num])
pi_new = np.zeros([NP, city_num])

pop = np.random.rand(NP, num) * 5
k = 1
x_old = pop

while k <= NG:
    x = np.argsort(x_old)
    indbest = x[0]

    for i in range(1, NP):
        if route(x[i]) < route(indbest):
            indbest = x[i]
    changdu.append(route(x[i]))
    lujing.append(indbest)

    for i in range(NP):
        result = random.sample(range(NP), 4)
        for t in range(3):
            if i == t:
                result[t] = result[3]
        v = x_old[result[0]] + F * (x_old[result[1]] - x_old[result[2]])
        for c in range(num):
            randnum = random.uniform(0, 1)
            if CR < randnum:
                v[c] = x_old[i][c]
        if route(x[i]) >= route(np.argsort(v)):
            x_old[i] = v

    k += 1

best_route_indices = lujing[changdu.index(min(changdu))]
print("Min Distance:", min(changdu))
print("Best Route Indices:", best_route_indices)

# Plot the best route
plot_route(city, best_route_indices)




