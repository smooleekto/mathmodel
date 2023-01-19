import pygame
import math
import numpy as np
import os



WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
SPEED = 18
WAITING_MAX = 5
nV = 10
INF = 99


def draw_map():
    font = pygame.font.SysFont('comicsans', 40)
    for i in range(len(stop_cords)):
        text = font.render(str(i), True, BLACK)
        screen.blit(text, stop_cords[i])
    font = pygame.font.SysFont('comicsans', 20)
    for i in range(len(roads_distance)):
        text = font.render(str(roads_distance[i]), True, RED)
        screen.blit(text, roads_centers[i])
    for i in range(0, len(roads_cords)):
        pygame.draw.line(screen, BLACK, stop_cords[roads_cords[i][0]], stop_cords[roads_cords[i][1]], width=4)
    for i in range(0, len(stop_cords)):
        pygame.draw.circle(screen, BLUE, stop_cords[i], 15, width=0)


def bus_draw(x, y):
    screen.blit(bus_img, (x, y))



def floyd(G):
    dist = list(map(lambda p: list(map(lambda q: q, p)), G))
    for r in range(nV):
        for p in range(nV):
            for q in range(nV):
                dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])
    return dist

    

pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Transport system")

stop_cords = [[750, 371], [552, 497], [502, 716], [116, 172], [332, 414], [392, 176], [284, 612], [335, 782], [712, 620], [193, 488]]
roads_cords = [(4, 9),(0, 5), (0, 1), (0, 8), (4, 3), (5,4), (9, 5), (4, 1), (1, 8), (2, 8), (2, 7), (1, 6), (1, 2), (9, 6), (6, 7)]
roads_distance = []
for item in roads_cords:
    roads_distance.append(round(math.sqrt((stop_cords[item[1]][0] - stop_cords[item[0]][0])**2 + (stop_cords[item[1]][1] - stop_cords[item[0]][1])**2) *2))
roads_time = [round(roads_distance[i]/1000/18*3600/60, 2) for i in range(len(roads_distance))]
roads_centers = []
for item in roads_cords:
    roads_centers.append(((stop_cords[item[1]][0] + stop_cords[item[0]][0])/2, (stop_cords[item[1]][1] + stop_cords[item[0]][1])/2))
for i in range(len(roads_distance)):
    if roads_distance[i] > 800:
        print(f'Дорога між зупинками {roads_cords[i]} занадто довга, рекомендується додати зупинку')

run = True
path = os.path.abspath(__file__)
path = '\\'.join(path.split('\\')[:-1])
bus_img = pygame.image.load(f'{path}/bus.png')
bus_route1 = [0, 1, 4, 3]
bus_route2 = [5, 0, 8, 2, 7, 6, 9, 5]
bus_route3 = [5, 4, 1, 2, 8]
bus_route4 = [4, 9, 6, 1]
bus_routes = [bus_route1, bus_route2, bus_route3, bus_route4]
bus_quantity = [4, 5, 2, 7]

all_routes = []
for route in bus_routes:
    rev = list(reversed(route))
    all_routes.append([(route[i-1], route[i]) for i in range(1, len(route))])
    all_routes.append([(rev[i-1], rev[i]) for i in range(1, len(rev))])
all_routes_time = []
for i in range(len(bus_routes)):
    time = 0
    r = [(bus_routes[i][j-1], bus_routes[i][j]) for j in range(1, len(bus_routes[i]))]
    print(f'Маршрут #{i+1}: {r}')
    for j in range(len(r)):
        if r[j] in roads_cords:
            time += roads_time[roads_cords.index(r[j])]
        else:
            time += roads_time[roads_cords.index((r[j][1], r[j][0]))]
    time = time*2/bus_quantity[i]
    all_routes_time.append(round(time, 2))
print(f'Максимальний час очікування транспорту')
for i in range(len(all_routes_time)):
    print(f'Маршрут {i+1}: {all_routes_time[i]} хв')
    if all_routes_time[i] > WAITING_MAX:
        print(f'Максимальний час очікування транспорту на маршруті {i+1} більше за заданий поріг. Збільшіть кількість автобусів на маршруті')
c = 0
for item in roads_cords:
    if item not in [a for b in all_routes for a in b]:
        c+=1
        print(f'По цій дорозі не пролягає маршрут: {item}')

if c ==0:
    print('Маршрут пролягає по всім дорогам!')
else:
    print(f'Доріг, по яким не пролягають маршрути: {c}')

G = [[0, INF, INF, INF, INF, INF, INF, INF, INF, INF],
    [INF, 0, INF, INF, INF, INF, INF, INF, INF, INF],
    [INF, INF, 0, INF, INF, INF, INF, INF, INF, INF],
    [INF, INF, INF, 0, INF, INF, INF, INF, INF, INF],
    [INF, INF, INF, INF, 0, INF, INF, INF, INF, INF],
    [INF, INF, INF, INF, INF, 0, INF, INF, INF, INF],
    [INF, INF, INF, INF, INF, INF, 0, INF, INF, INF],
    [INF, INF, INF, INF, INF, INF, INF, 0, INF, INF],
    [INF, INF, INF, INF, INF, INF, INF, INF, 0, INF],
    [INF, INF, INF, INF, INF, INF, INF, INF, INF, 0]]
for i in range(len(roads_cords)):
    G[roads_cords[i][0]][roads_cords[i][1]] = round(roads_distance[i]/1000/18*3600/60, 2)
    G[roads_cords[i][1]][roads_cords[i][0]] = round(roads_distance[i]/1000/18*3600/60, 2)
shortest_all = floyd(G)

G1 = [[0, INF, INF, INF, INF, INF, INF, INF, INF, INF],
    [INF, 0, INF, INF, INF, INF, INF, INF, INF, INF],
    [INF, INF, 0, INF, INF, INF, INF, INF, INF, INF],
    [INF, INF, INF, 0, INF, INF, INF, INF, INF, INF],
    [INF, INF, INF, INF, 0, INF, INF, INF, INF, INF],
    [INF, INF, INF, INF, INF, 0, INF, INF, INF, INF],
    [INF, INF, INF, INF, INF, INF, 0, INF, INF, INF],
    [INF, INF, INF, INF, INF, INF, INF, 0, INF, INF],
    [INF, INF, INF, INF, INF, INF, INF, INF, 0, INF],
    [INF, INF, INF, INF, INF, INF, INF, INF, INF, 0]]
all_routes = [a for b in all_routes for a in b]
for i in range(len(roads_cords)):
    if roads_cords[i] in all_routes:
        G1[roads_cords[i][0]][roads_cords[i][1]] = G[roads_cords[i][0]][roads_cords[i][1]]
        G1[roads_cords[i][1]][roads_cords[i][0]] = G[roads_cords[i][1]][roads_cords[i][0]]
    elif (roads_cords[i][1], roads_cords[i][0]) in all_routes:
        G1[roads_cords[i][1]][roads_cords[i][0]] = G[roads_cords[i][1]][roads_cords[i][0]]
        G1[roads_cords[i][0]][roads_cords[i][1]] = G[roads_cords[i][0]][roads_cords[i][1]]
shortest_paths = floyd(G1)

c = 0
add = (nV+1) % 2
for i in range(nV):
    for j in range(i+add,nV):
        if shortest_paths[i][j] > shortest_all[i][j] and i!=j:
            c+=1
            print(f'Шлях з точки {i} в точку {j} неоптимізований! Різниця склала {round(shortest_paths[i][j] - shortest_all[i][j], 2)} хв.')
if c == 0:
    print('Всі маршрути оптимальні!')
for i in range(nV):
    for j in range(i+add,nV):
        if i !=j:
            print(f'Найкоротший шлях з точки {i} в точку {j} займає {round(shortest_paths[i][j], 2)} хв.')

busX = 750
busY = 371
norm = np.array((stop_cords[bus_route1[1]][0]-stop_cords[bus_route1[0]][0], stop_cords[bus_route1[1]][1] - stop_cords[bus_route1[0]][1]))
norm = norm / np.linalg.norm(norm)
busChangeX = norm[0]/3
busChangeY = norm[1]/3


busX2 = 392
busY2 = 176
norm2 = np.array((stop_cords[bus_route2[1]][0]-stop_cords[bus_route2[0]][0], stop_cords[bus_route2[1]][1] - stop_cords[bus_route2[0]][1]))
norm2 = norm2 / np.linalg.norm(norm2)
busChangeX2 = norm2[0]/3
busChangeY2 = norm2[1]/3


busX3 = 392
busY3 = 176
norm3 = np.array((stop_cords[bus_route3[1]][0]-stop_cords[bus_route3[0]][0], stop_cords[bus_route3[1]][1] - stop_cords[bus_route3[0]][1]))
norm3 = norm3 / np.linalg.norm(norm3)
busChangeX3 = norm3[0]/3
busChangeY3 = norm3[1]/3


busX4 = 332
busY4 = 414
norm4 = np.array((stop_cords[bus_route4[1]][0]-stop_cords[bus_route4[0]][0], stop_cords[bus_route4[1]][1] - stop_cords[bus_route4[0]][1]))
norm4 = norm4 / np.linalg.norm(norm4)
busChangeX4 = norm4[0]/3
busChangeY4 = norm4[1]/3

while run:
    screen.fill(WHITE)
    draw_map()
    busX += busChangeX
    busY += busChangeY
    bus_draw(busX, busY)
    for i in range(0, len(bus_route1)):
        if round(busX) == stop_cords[bus_route1[i]][0] and round(busY) == stop_cords[bus_route1[i]][1] and round(busX) != stop_cords[bus_route1[-1]][0] and round(busY) != stop_cords[bus_route1[-1]][0]:
            norm = np.array((stop_cords[bus_route1[i+1]][0]-stop_cords[bus_route1[i]][0], stop_cords[bus_route1[i+1]][1]-stop_cords[bus_route1[i]][1]))
            norm = norm / np.linalg.norm(norm)
            busChangeX = norm[0]/3
            busChangeY = norm[1]/3
        if round(busX) == stop_cords[bus_route1[-1]][0] and round(busY) == stop_cords[bus_route1[-1]][1]:
            bus_route1 = list(reversed(bus_route1))
            norm = np.array((stop_cords[bus_route1[i+1]][0]-stop_cords[bus_route1[i]][0], stop_cords[bus_route1[i+1]][1]-stop_cords[bus_route1[i]][1]))
            norm = norm / np.linalg.norm(norm)
            busChangeX = norm[0]/3
            busChangeY = norm[1]/3


    busX2 += busChangeX2
    busY2 += busChangeY2
    bus_draw(busX2, busY2)
    for i in range(0, len(bus_route2)):
        if round(busX2) == stop_cords[bus_route2[i]][0] and round(busY2) == stop_cords[bus_route2[i]][1] and round(busX2) != stop_cords[bus_route2[-1]][0] and round(busY2) != stop_cords[bus_route2[-1]][0]:
            norm2 = np.array((stop_cords[bus_route2[i+1]][0] - stop_cords[bus_route2[i]][0], stop_cords[bus_route2[i+1]][1]-stop_cords[bus_route2[i]][1]))
            norm2 = norm2 / np.linalg.norm(norm2)
            busChangeX2 = norm2[0]/3
            busChangeY2 = norm2[1]/3
        if round(busX2) == stop_cords[bus_route2[-1]][0] and round(busY2) == stop_cords[bus_route2[-1]][1]:
            i = 0
            norm2 = np.array((stop_cords[bus_route2[i+1]][0]-stop_cords[bus_route2[i]][0], stop_cords[bus_route2[i+1]][1]-stop_cords[bus_route2[i]][1]))
            norm2 = norm2 / np.linalg.norm(norm2)
            busChangeX2 = norm2[0]/3
            busChangeY2 = norm2[1]/3


    busX3 += busChangeX3
    busY3 += busChangeY3
    bus_draw(busX3, busY3)
    for i in range(0, len(bus_route3)):
        if round(busX3) == stop_cords[bus_route3[i]][0] and round(busY3) == stop_cords[bus_route3[i]][1] and round(busX3) != stop_cords[bus_route3[-1]][0] and round(busY3) != stop_cords[bus_route3[-1]][0]:
            norm3 = np.array((stop_cords[bus_route3[i+1]][0] - stop_cords[bus_route3[i]][0], stop_cords[bus_route3[i+1]][1]-stop_cords[bus_route3[i]][1]))
            norm3 = norm3 / np.linalg.norm(norm3)
            busChangeX3 = norm3[0]/3
            busChangeY3 = norm3[1]/3
        if round(busX3) == stop_cords[bus_route3[-1]][0] and round(busY3) == stop_cords[bus_route3[-1]][1]:
            bus_route3 = list(reversed(bus_route3))
            norm3 = np.array((stop_cords[bus_route3[i+1]][0]-stop_cords[bus_route3[i]][0], stop_cords[bus_route3[i+1]][1]-stop_cords[bus_route3[i]][1]))
            norm3 = norm3 / np.linalg.norm(norm3)
            busChangeX3 = norm3[0]/3
            busChangeY3 = norm3[1]/3


    busX4 += busChangeX4
    busY4 += busChangeY4
    bus_draw(busX4, busY4)
    for i in range(0, len(bus_route4)):
        if round(busX4) == stop_cords[bus_route4[i]][0] and round(busY4) == stop_cords[bus_route4[i]][1] and round(busX4) != stop_cords[bus_route4[-1]][0] and round(busY4) != stop_cords[bus_route4[-1]][0]:
            norm4 = np.array((stop_cords[bus_route4[i+1]][0] - stop_cords[bus_route4[i]][0], stop_cords[bus_route4[i+1]][1]-stop_cords[bus_route4[i]][1]))
            norm4 = norm4 / np.linalg.norm(norm4)
            busChangeX4 = norm4[0]/3
            busChangeY4 = norm4[1]/3
        if round(busX4) == stop_cords[bus_route4[-1]][0] and round(busY4) == stop_cords[bus_route4[-1]][1]:
            bus_route4 = list(reversed(bus_route4))
            norm4 = np.array((stop_cords[bus_route4[i+1]][0]-stop_cords[bus_route4[i]][0], stop_cords[bus_route4[i+1]][1]-stop_cords[bus_route4[i]][1]))
            norm4 = norm4 / np.linalg.norm(norm4)
            busChangeX4 = norm4[0]/3
            busChangeY4 = norm4[1]/3


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
