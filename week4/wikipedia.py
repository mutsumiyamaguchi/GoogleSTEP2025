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

    # for homwwork1
    # 新しいデータ構造として{id:一つ上のnodeのid}というデータを格納するための準備をする関数
    def add_initilal_data(self):
        self.pre_id = {}

        for id,val in self.titles.items():
            self.pre_id[id] = None

    # 現在のノードのidを受け取ったら初期ノードまで逆人探索し、pathを返す関数
    def ret_path(self,node):
        node = node
        path = []

        while node != None:
            path.insert(0,self.titles[node])#現在参照しているnodeのtitleをpathの先頭に追加
            previd = self.pre_id[node]
            node = previd
        return path


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        # BFSを実装
        self.add_initilal_data() #データを格納することができるよう、初期化
        queue = deque() #キューを準備 

        start_id = [id for id, value in self.titles.items() if value == start]#初期ノードに対応するidを探索

        queue.append(start_id[0]) #(ノードid,1つ上のノードのid)というデータ構造でキューに追加  
        self.pre_id[start_id[0]] = None #初期ノードの親ノードはNoneなので格納 

        
        # これだと探索にO(n)かかってしまうので,
        # set()を用いた方がいいO(1)　順番が必要じゃない時はの方がいい
        # 辞書の書き方もあるね

        # 空間計算量的にO(V**2)になってしまうから探索済みのpathを一つだけ格納しておいてそれを最後に辿るようにする

        searched_nodeset = set() # キューに格納済みノード用リスト
        searched_nodeset.add(start_id[0])# そうでなければ探索済みリストにid追加

        while len(queue) > 0:# キューが空でない時
            
            now_node= queue.popleft() # キューの先頭のidおよび親nodeのidを取り出す

            if self.titles[now_node] == goal:# 現在のノードidのタイトルがゴールと一致していたら
                path = self.ret_path(now_node)# pathを生成して返してもらう
                return path 
              
            now_node_linked_lst = self.links[now_node]# 現在探索したノードに接続しているノードリストを準備 
            
            for nodeid in now_node_linked_lst:# ノードリスト内のそれぞれのノードに対して、探索済みでなければキューに追加
                if nodeid not in searched_nodeset:

                    searched_nodeset.add(nodeid)# キューに格納済みリストにid追加
                    queue.append(nodeid) # idをキューに追加する
                    self.pre_id[nodeid] = now_node #pre_idを保存しておくデータに追加しておく

        # グラフ内に目的ノードがなければNoneを返す
        return None

    # for homework2
    # デバッグする時には何回計算しているかを確認するといい

    # smallで実行してできていれbアルゴリズムが間違っているわけではないはず
    # pagerank関連初期化関数

    def add_initial_pagerank(self):
        self.pagerank = {} #pagerank格納用
        self.pagerankbuf = {} #pagerankを更新捨時のバッファ
        self.pagerank_initial = {} #pagerankbufを初期化するとき用
        self.node_counter = 0 #node数格納
        self.allnode_pagerank = 0 #全てのノードに均等に分配されているpagerank
        self.allnode_pagerankbuf = 0 #allnode_pagerankを更新するために用いるバッファ

        for id, value in self.titles.items():
            self.pagerank[id] = 1.0 #初期pagerank1.0を追加
            self.pagerankbuf[id] = 0 # pagerankbufの初期化
            self.pagerank_initial[id] = 0 #pagerank_initialの初期化
            self.node_counter += 1 #node数インクリメント

    # copy = O(N) だからinitialを初期化するときにforぶん回して0にしているのと同じことをしている
    
    # 収束していなければTrue
    # 収束していればFalseを返す
    def convergence_check(self):
        # 全てのノードについて
        for id,newpagerank in self.pagerankbuf.items():
            
            # 全ノード均等のページランク + そのノード特有のページランク　で実際のページランクを算出
            if abs((self.allnode_pagerankbuf + newpagerank) - (self.allnode_pagerank + self.pagerank[id]))**2 > 0.01:# 収束していない時 
                self.pagerank = self.pagerankbuf.copy() # pagerankをpagerankbufに更新
                self.pagerankbuf = self.pagerank_initial.copy() # pagerankbufを初期化
                self.allnode_pagerank = self.allnode_pagerankbuf # 均等に分配する必要のあるページランクの更新
                self.allnode_pagerankbuf = 0 #allnode_pagerankbufの初期化
                return True
        
        # 収束していた場合
        self.pagerank = self.pagerankbuf.copy() # pagerankをpagerankbufに更新
        return False 
        
    # random_surferアルゴリズムを実行する関数
    def execute_random_surfer(self):
         
        for id,pagerank in self.pagerank.items():# 全てのノードでページランクの分配を実行
            
            
            if self.links[id]:# linked_listがある時
                
                linkednode_pagerank = (self.allnode_pagerank + pagerank) * 0.85 /len(self.links[id])# linkednodeに85%を分配
                self.allnode_pagerankbuf += (self.allnode_pagerank+pagerank) * 0.15 /self.node_counter# allnodeに15％分配

                for linkedid in self.links[id]: #linkedlistにpagerankを追加
                    self.pagerankbuf[linkedid] += linkednode_pagerank 
            
            else: # linked_listがない時
                self.allnode_pagerankbuf += (self.allnode_pagerank + pagerank) / self.node_counter # allnodeに100％分配

            # print("data structure chek",self.pagerankbuf)

             
    
    # pagerank上位10ページを返す関数
    def topten_pagerank(self):
        
        pagerank_sorted = sorted(self.pagerank.items(), key=lambda x: x[1], reverse=True)# pagerankによってソート

        topten_lst = pagerank_sorted[:11]# pageranktop10を格納
        title_lst = [] #title格納用

        for id,pagerank in topten_lst:
            title_lst.append({self.titles[id]:pagerank})#titleのみリストに格納

        return title_lst



    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):

        self.add_initial_pagerank()# 全ノードに1を付与
        checkflg = True# 収束チェックフラグを用意

        print("finished add initial pagerank")

        self.counter = 0
        while checkflg:# 収束していない間は以下を実行
            
            self.counter += 1
            print("counter:",self.counter)

            self.execute_random_surfer()# random_surferを実行
            # print("this is pagerank :",self.pagerank)  
            checkflg = self.convergence_check()# 収束チェック
        
        top_pagerank = self.topten_pagerank()#pagerankトップ10を格納
        print(top_pagerank)
        
        

    # for homework3
    def add_longestpath_data(self):

        self.longestpath = {} #新たなデータ型を用意

        for id,val in self.titles.items(): # {id:preid}となるようにする 
            self.longestpath[id] = []
            
        print("add longest path finished!!!")

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    def make_path(self,node,prenode):

        path = []
        goal_title = self.titls[node]
        path.append(goal_title)

        node = prenode

        while node!= None:
            title = self.titles[node]
            path.insert(0,title)

            

    def find_dfs_path(self, start, goal):

        # DFSのキューに同じノードを複数回受け入れるver.のコードで実装
        # 2回目以降の探索の場合、pathを長い方に更新していくようにする

        # 仮に目的のデータが見つかってもreutnrせず全探索=>計算量およびメモリ使用量がとても多い
        # 無限ループになってしまうのはどうしたらいいのかわからない

        # じぶんのpathにあるノードには戻らないという制約を加える

        self.add_longestpath_data()# 新たなデータ型を用意

        # DFSを実装
        stack = deque() #stack準備
        searched_node = set() #探索済み集合の準備

        for id,title in self.titles.items():
            if title == start:
                start_id = id #startのtitleに一致するもののid取得
            elif title == goal:
                goal_id = id #goalのtitleに一致するもののid取得
        
        # データ構造は{id:preid}とする
        self.longestpath[start_id] = None #startのidとを格納
        
        stack.append(start_id) #stackに初期ノード追加

        # 計算量はO(N!)　pathに入る可能性はN種類の並び方を考えると計算量はO(N!)
        # DFSのpart2の方針で考えてみる

        # 次に行くlinkednodeをシャッフルすると長いところに辿り着く可能性が増えるかもしれない
        # 最短経路を先に知っておいて、その経路から一番遠い経路を辿るようにする（局所的に一番遠い方法）
        # DFSからとりあえず経路を探索して、一つ選ぶ、その両端の中身を一つずつ削ってその経路の中で長いものをとってくる、更新する、これを繰り返してできるだけ長いものを作成する
        # DFSを複数回回す時にはランダム性を入れてあげた方がながいPATHが見つかるかのうせいがあがる

        while len(stack) > 0:

            now_node = stack.pop() #右から一つの要素を取得
            searched_node.add(now_node)

            # pathをアップデートするか検討
            if self.longestpath[now_node[0]]:
                pre_path = self.longestpath[now_node[0]]
                if len(pre_path) < len(now_node[1]): #現在のpathより長ければ更新
                    self.longestpath[now_node[0]] = now_node[1]
            
            linknode_lst = self.links[now_node[0]]
            print(linknode_lst)

            for nodeid in linknode_lst:
                stack.append(nodeid)#stack追加
                self.longestpath[nodeid] = now_node

        # 探索終了後
        print(self.longestpath[goal_id])



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
    # # Example
    # wikipedia.find_longest_titles()
    # # Example
    # wikipedia.find_most_linked_pages()

    # Homework #1

    # path_small = wikipedia.find_shortest_path("A", "E")
    # print(path_small)

    # path_med = wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # print(path_med)

    # path_long = wikipedia.find_shortest_path("渋谷", "小野妹子")
    # print(path_long)

    # # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    # wikipedia.find_longest_path("A", "E")
    # wikipedia.find_longest_path("渋谷", "池袋")
