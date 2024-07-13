# 导入数学模块和随机模块
import math
import random

# 定义一个城市类，包含序号，横坐标，纵坐标和计算距离的方法
class City:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def distance(self, city):
        # 计算两个城市之间的欧氏距离
        return math.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)

    def __repr__(self):
        # 返回城市的字符串表示
        return f"City({self.index}, {self.x}, {self.y})"

# 定义一个路径类，包含一个城市列表和计算适应度的方法
class Route:
    def __init__(self, cities):
        self.cities = cities

    def fitness(self):
        # 计算路径的适应度，即路径的总距离的倒数
        distance = 0
        for i in range(len(self.cities) - 1):
            # 累加相邻城市之间的距离
            distance += self.cities[i].distance(self.cities[i + 1])
        distance += self.cities[len(self.cities) - 1].distance(self.cities[0])
        return (1 / distance)*1000

    def __repr__(self):
        # 返回路径的字符串表示
        return f"Route({self.cities})"

# 定义一个遗传算法类，包含初始化种群，选择父代，交叉，变异，选择子代等方法
class GeneticAlgorithm:
    def __init__(self, cities, pop_size, elite_size, mutation_rate, generations):
        self.cities = cities # 城市列表
        self.pop_size = pop_size # 种群大小
        self.elite_size = elite_size # 精英个体数量
        self.mutation_rate = mutation_rate # 变异概率
        self.generations = generations # 迭代次数

    def create_route(self):
        # 随机创建一个路径
        return Route(random.sample(self.cities, len(self.cities)))

    def initial_population(self):
        # 初始化种群
        population = []
        for i in range(self.pop_size):
            # 随机生成pop_size个路径
            population.append(self.create_route())
        return population

    def rank_routes(self, population):
        # 对种群中的路径按照适应度进行排序
        return sorted(population, key=lambda route: route.fitness(), reverse=True)

    def selection(self, population):
        # 选择父代
        parents = []
        # 计算种群中所有路径的适应度之和
        fitness_sum = sum(route.fitness() for route in population)
        # 用轮盘赌法选择pop_size个父代
        for i in range(self.pop_size):
            # 生成一个随机数
            r = random.random()
            # 初始化累积概率
            p = 0
            for route in population:
                # 计算当前路径的概率
                p += route.fitness() / fitness_sum
                if p >= r:
                    # 如果累积概率大于等于随机数，选择当前路径作为父代
                    parents.append(route)
                    break
        return parents

    def crossover(self, parent1, parent2):
        # 交叉两个父代，生成一个子代
        child = []
        # 随机选择一个交叉区间
        start = random.randint(0, len(parent1.cities) - 2)
        end = random.randint(start + 1, len(parent1.cities) - 1)
        # 把第一个父代的交叉区间内的城市复制到子代
        child.extend(parent1.cities[start:end + 1])
        # 把第二个父代中不在子代的城市按照顺序添加到子代
        for city in parent2.cities:
            if city not in child:
                child.append(city)
        return Route(child)

    def mutation(self, route):
        # 对一个路径进行变异
        for i in range(len(route.cities)):
            # 对每个城市，以一定的概率与另一个随机城市交换位置
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(route.cities) - 1)
                route.cities[i], route.cities[j] = route.cities[j], route.cities[i]
        return route

    def new_population(self, population):
        # 生成新的种群
        new_population = []
        # 对原始种群按照适应度进行排序
        ranked_population = self.rank_routes(population)
        # 如果设置了精英个体数量，保留最优的elite_size个路径
        if self.elite_size > 0:
            new_population.extend(ranked_population[:self.elite_size])
        # 选择父代
        parents = self.selection(population)
        # 交叉生成子代
        for i in range(len(new_population), self.pop_size):
            # 随机选择两个父代
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            # 交叉生成一个子代
            child = self.crossover(parent1, parent2)
            # 添加到新的种群
            new_population.append(child)
        # 变异新的种群
        for i in range(self.elite_size, self.pop_size):
            # 对非精英个体进行变异
            new_population[i] = self.mutation(new_population[i])
        return new_population

    def run(self):
        # 运行遗传算法
        # 初始化种群
        population = self.initial_population()
        # 迭代generations次
        for i in range(self.generations):
            # 生成新的种群
            population = self.new_population(population)
            # 打印当前最优的路径和适应度
            best_route = self.rank_routes(population)[0]
            print(f"Generation {i + 1}: {best_route}, fitness = {best_route.fitness():.4f}")
        # 返回最终的最优路径
        return self.rank_routes(population)[0]

# 从data.txt文件中读取城市数据
cities = []
with open("data.txt", "r") as f:
    for line in f:
        # 按照逗号分隔每一行的数据
        index, x, y = line.split(" ")
        # 创建一个城市对象并添加到城市列表
        cities.append(City(int(index), float(x), float(y)))

# 设置遗传算法的参数
pop_size = 100 # 种群大小
elite_size = 20 # 精英个体数量
mutation_rate = 0.01 # 变异概率
generations = 500 # 迭代次数

# 创建一个遗传算法对象
ga = GeneticAlgorithm(cities, pop_size, elite_size, mutation_rate, generations)
# 运行遗传算法并得到最优路径
best_route = ga.run()
# 打印最优路径和对应的总距离
print(f"Best route: {best_route}, distance = {1000 / best_route.fitness():.2f}")
