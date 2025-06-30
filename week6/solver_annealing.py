import math
import random
import sys
from common import print_tour, read_input


def distance(city1, city2):
    # 二つの地点の距離を求める
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])


def total_distance(tour, cities):
    # distanceの合計値をスコアとする
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))


def random_neighbor(tour):
    # ランダムに二つの地点を入れ替えた近傍解を作成
    a, b = random.sample(range(len(tour)), 2)
    neighbor = tour[:]
    neighbor[a], neighbor[b] = neighbor[b], neighbor[a]
    return neighbor


def greedy_tour(cities):
    # 貪欲法で一つ解を見つける
    N = len(cities)
    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited = set(range(1, N))
    tour = [current_city]

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    return tour


def simulated_annealing(cities, t0=300.0, t_min=1e-3, alpha=0.995, max_iter=200000):
    # 一つ貪欲法で求める
    current = greedy_tour(cities)
    # 暫定最適解に格納
    best = current[:]
    # 暫定距離に格納
    best_dist = total_distance(best, cities)

    t = t0
    for step in range(max_iter):
        # 近傍解から候補を出す
        candidate = random_neighbor(current)
        # 現在の解の距離を求める
        d_current = total_distance(current, cities)
        # 候補解の候補を出す
        d_candidate = total_distance(candidate, cities)
        # 候補解から現在の解の距離の差を出す
        delta = d_candidate - d_current

        # もし差が0より小さいつまり短い経路または、長くなっていたとしても温度が高い（探索開始から時間があまり経っていない）時には新しい経路を受け入れる
        if delta < 0 or random.random() < math.exp(-delta / t):
            # 現在の経路を候補解に更新
            current = candidate
            # もし最適解よりも短い経路であれば
            if d_candidate < best_dist:
                # 最適解も更新
                best = candidate
                best_dist = d_candidate
        # 温度を下げる
        t *= alpha
        # 温度が最低を下回ったら探索をやめる
        if t < t_min:
            break
    
    print(total_distance(best,cities))
    return best


def solve(cities):
    return simulated_annealing(cities)
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print("Distance:", total_distance(tour, read_input(sys.argv[1])))

