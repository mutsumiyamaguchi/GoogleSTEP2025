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


# def random_neighbor(tour):
def twoopt_neighbor(city1,city2,tour):
    # 近傍解を作成
    # この部分に2optの考え方を入れたい
    # 引数として渡された二つの都市の交差を解く（または元々交差していなければ交差させる）ようにする
    # 交差しているかしていないかの判断はしていないのでもしかしたら元々交差していないものを交差させてしまっている可能性がある

    neighbor1 = tour[:city1]
    neighbor2 = tour[city2+1:]
    reverse_tour = tour[city1:city2+1]
    reverse_tour.reverse()
    neighbor = neighbor1 + reverse_tour + neighbor2

    return neighbor

# ランダム化最近近傍法のpythonコードを疑似コードを元に作成
def randomized_nnm(cities):

    # 現在の都市のインデックスリスト作成
    cities_lst = [i for i in range(len(cities))]

    # 初期都市インデックス格納
    current = 0
    # 探索ルート用リストを作成、初期値格納
    route = [current]

    # 未探索集合を作成
    unsearched_set = set(cities_lst)
    unsearched_set.remove(current)

    # 未探索集合がある間は以下を繰り返す
    while unsearched_set:

        # 現在探索済みの最終ノードからの距離を算出する
        current_distance = {}
        for city in unsearched_set:
            city_distance = distance(cities[current],cities[city])
            current_distance[city] = city_distance

        # 現在探索済みの最終ノードからの距離のうち上位10ノードを取り出す
        k = 10
        nearest_set = sorted(current_distance.items(),key=lambda x:x[1])[:k+1]
        nearest_city = [city for city,distance in nearest_set]

        # その中から1つランダムに選び探索済みリストに追加（ルート作成）
        current = random.choice(nearest_city)
        route.append(current)
        # 未探索ノードから選んだ一つのノードを取り出す
        unsearched_set.remove(current)

    # ルートを返す
    return route


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


def simulated_annealing(cities, t0=100.0, t_min=1e-3, alpha=0.995, max_iter=100):
    
    # 初期解として、貪欲法とランダム化最近近傍法の良い方を選ぶようにする

    # 貪欲法実行
    greedy = greedy_tour(cities)
    # ランダム化最近近傍方を実行
    randomized = randomized_nnm(cities)
    # 貪欲法の経路の距離を算出
    greedy_dist = total_distance(greedy, cities)
    # ランダム化最近近傍方の距離を算出
    random_dist = total_distance(randomized, cities)

    # 二つの経路のうち短い方を初期経路として設定
    if greedy_dist < random_dist:
        current = greedy
    else:
        current = randomized
    
    # 暫定最適解に格納
    best = current[:]
    # 暫定距離に格納
    best_dist = total_distance(best, cities)

    # 温度を初期温度に設定
    t = t0

    # 最高試行回数まで試す
    for step in range(max_iter):
        print(step)
        improved = False

        # 候補解に存在している都市から二つ選ぶ（全組み合わせ試す）
        for i in range(len(current)-1):
            for j in range(i+1,len(current)):

                # 交差を解く（または作る）
                candidate = twoopt_neighbor(i,j,current)
                # 現在の解の距離を求める
                d_current = total_distance(current, cities)
                # 候補解の候補を出す
                d_candidate = total_distance(candidate, cities)
                # 候補解から現在の解の距離の差を出す
                delta = d_candidate - d_current

                # もし差が0より小さい（つまり短い経路）または、長くなっていたとしても温度が高い（探索開始から時間があまり経っていない）時には新しい経路を受け入れる
                if delta < 0 or random.random() < math.exp(-delta / t):
                    # 現在の経路を候補解に更新
                    current = candidate
                    # もし最適解よりも短い経路であれば
                    if d_candidate < best_dist:
                        # 最適解も更新
                        best = candidate
                        best_dist = d_candidate
                        improved = True
                    break
            if improved:
                break
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

