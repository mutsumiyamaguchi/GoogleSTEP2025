import sys
from collections import deque
import copy

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        # BFSを実装
        queue = deque() #キューを準備 

        start_id = [id for id, value in self.titles.items() if value == start]#初期ノードに対応するidを探索
        queue.append((start_id[0],[start])) #(ノードid,[初期ノードからのpath])というデータ構造でキューに追加   
        searched_nodelst = [] # 探索済みノード用リスト

        while len(queue) > 0:# キューが空でない時
            
            now_node,path = queue.popleft() # キューの先頭のidおよび先頭からのpathを取り出す

            if self.titles[now_node] == goal:# 現在のノードidのタイトルがゴールと一致していたらpathを返す
                return path   
            searched_nodelst.append(now_node)# そうでなければ探索済みリストにid追加
            
            now_node_linked_lst = self.links[now_node]# 現在探索したノードに接続しているノードリストを準備

            
            
            for nodeid in now_node_linked_lst:# ノードリスト内のそれぞれのノードに対して、探索済みでなければキューに追加
                if nodeid not in searched_nodelst:

                    newpath = copy.copy(path)# pathをcopy
                    newpath.append(self.titles[nodeid])# 対応するtitlesを追加することで初期ノードからのpathを格納
                    queue.append((nodeid,newpath)) # (id,path)というデータをキューに追加する

        # グラフ内に目的ノードがなければNoneを返す
        return None

    # for homework2

    # pagerank関連初期化関数
    def add_initial_pagerank(self):
        self.pagerank = {} #pagerank格納用
        self.pagerankbuf = {} #pagerankを更新捨時のバッファ
        self.pagerank_initial = {} #pagerankbufを初期化するとき用
        self.node_counter = 0 #node数格納

        for id, value in self.titles.items():
            self.pagerank[id] = 1.0 #初期pagerank1.0を追加
            self.pagerankbuf[id] = 0 # pagerankbufの初期化
            self.pagerank_initial[id] = 0 #pagerank_initialの初期化
            self.node_counter += 1 #node数インクリメント
    
    # 収束していなければTrue
    # 収束していればFalseを返す
    def convergence_check(self):
        # 全てのノードについて
        for id,newpagerank in self.pagerankbuf.items():

            if abs(newpagerank - self.pagerank[id])**2 > 0.01:# 収束していない時 
                self.pagerank = self.pagerankbuf # pagerankをpagerankbufに更新
                self.pagerankbuf = self.pagerank_initial # pagerankbufを初期化
                return True
        
        # 収束していた場合
        self.pagerank = self.pagerankbuf # pagerankをpagerankbufに更新
        return False 
        
    # random_surferアルゴリズムを実行する関数
    def conduct_random_surfer(self):
 
        for id,pagerank in self.pagerank.items():# 全てのノードでページランクの分配を実行
            
            if self.links[id]:# linked_listがある時
                
                linkednode_pagerank = pagerank * 0.85 /len(self.links[id])# linkednodeに85%を分配
                allnode_pagerank = pagerank * 0.15 /self.node_counter# allnodeに15％分配

                for linkedid in self.links[id]: #linkedlistにpagerankを追加
                    self.pagerankbuf[linkedid] += linkednode_pagerank 
            
            else: # linked_listがない時
                allnode_pagerank = pagerank / self.node_counter # allnodeに100％分配

            for all_id,all_rank in self.pagerankbuf.items():#全てのノードにランクを分配
                    all_rank += allnode_pagerank
    
    # pagerank上位10ページを返す関数
    def topten_pagerank(self):
        
        pagerank_sorted = sorted(self.pagerank.items(), key=lambda x: x[1], reverse=True)# pagerankによってソート

        topten_lst = pagerank_sorted[:11]# pageranktop10を格納
        title_lst = [] #title格納用

        for id,pagerank in topten_lst:
            title_lst.append(self.titles[id])#titleのみリストに格納

        return title_lst



    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):

        self.add_initial_pagerank()# 全ノードに1を付与
        checkflg = True# 収束チェックフラグを用意

        while checkflg:# 収束していない間は以下を実行
            self.conduct_random_surfer()# random_surferを実行  
            checkflg = self.convergence_check()# 収束チェック
        
        top_pagerank = self.topten_pagerank()#pagerankトップ10を格納
        print(top_pagerank)
        
        


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()

    # Homework #1

    # path_small = wikipedia.find_shortest_path("C", "F")
    # print(path_small)

    # path_med = wikipedia.find_shortest_path("ソフトウエア工学", "カーネル")
    # print(path_med)

    # path_long = wikipedia.find_shortest_path("渋谷", "小野妹子")
    # print(path_long)

    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
