import random, sys, time

"""
質問
hash値を素数にすれば衝突が減り、実行時間が短くなるということに関して理解することはできたけれど、どのようにしたら再ハッシュの際に奇数にすることができるのか
ただ2倍、1/2倍にしていてはその性質から奇数である確率は下がってしまうと考えた
素数のリストを用意しておき、そこから選ぶようにして実装すれば良いのか=>OK

+1とかすることで奇数を実装(mod2を足したらいい)

ordの数分だけバイすればハッシュ関数はよりかぶらなくなる(X個ならX倍するようにする、X進数と同じ理論)
そうでないと今のままだと例えばa = 1 B = 10として aa = 11 Ba = 11となり、衝突する
A= 65 z = 122
つまり122-65+1 = 58種類存在している

assertionErrorが出てきてしまうのを解決したい => 等号が抜けていたからかも

"""

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value
def calculate_hash(key):

    # assertは式がtrueの時は何も起こらないけれどfalseの時はassertionerrorが表示される
    assert type(key) == str

    # Note: This is not a good hash function. Do you see why?
    hash = 0

    # for i in key:
    #     hash += ord(i)

    # # 桁によって10倍ずつしていくことでanagramのhash値の衝突を防ぐことができる
    # for index,i in enumerate(key):
    #     hash+= ord(i)*10**index


    # 10倍ではなく58種類存在しているため58倍するように変更する
    for index,i in enumerate(key):
        hash+= ord(i)*58**index


    return hash


# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0
        # ハッシュテーブルのサイズを素数にするために必要な変数
        self.prime_list = [11,23,47,97,193,389,773,1579]
        self.prime_index = 3

    
    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str


        # # ハッシュテーブルのサイズを2倍、1/2倍にする場合
        # if self.item_count <= self.bucket_size*0.3:
        #     self.update_hash_smaller()
        # if self.item_count >= self.bucket_size*0.7:
        #     self.update_hash_bigger()


        # ハッシュテーブルのサイズを素数にしたい場合
        # 素数のリストを用意しておき、そこから選ぶようにする。大きくなり過ぎた場合には2倍する関数を用いて対応するようにする
        # prime_list:素数のリスト
        # prime_index:現在のインデックスを格納しておくもの、初期は97なので3としている

        # 素数リスト範囲内
        if self.prime_index < 8 and self.prime_index > 0:
            if self.item_count <= self.bucket_size*0.3:
                self.prime_index -= 1
                self.rehash(self.prime_list[self.prime_index])
            elif self.item_count >= self.bucket_size*0.7:
                self.prime_index += 1
                self.rehash(self.prime_list[self.prime_index])
        # 範囲外
        else:
            if self.item_count <= self.bucket_size*0.3:
                self.update_hash_smaller()
            elif self.item_count >= self.bucket_size*0.7:
                self.update_hash_bigger()
        
        # print("[CHECK]this is after rehash",self.item_count,self.bucket_size)

        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str

        # rehashする必要があるか確認
        # 素数のリストを用意しておき、そこから選ぶようにする。大きくなり過ぎた場合には2倍する関数を用いて対応するようにする
        # prime_list:素数のリスト
        # prime_index:現在のインデックスを格納しておくもの、初期は97なので3としている

        # 素数リスト範囲内
        if self.prime_index < 8 and self.prime_index > 0:
            if self.item_count <= self.bucket_size*0.3:
                self.prime_index -= 1
                self.rehash(self.prime_list[self.prime_index])
            elif self.item_count >= self.bucket_size*0.7:
                self.prime_index += 1
                self.rehash(self.prime_list[self.prime_index])
        # 範囲外
        else:
            if self.item_count <= self.bucket_size*0.3:
                self.update_hash_smaller()
            elif self.item_count >= self.bucket_size*0.7:
                self.update_hash_bigger()

        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size

        previous_item = None #一つ前のアドレスを格納する変数
        next_item = self.buckets[bucket_index] #先頭アドレスを格納
        flg = 0 #return したかどうか判定するための変数だが、returnした時点でそれ以外の部分は実行されないのでwhile文を抜けたらfalseを返すようにすることでこの変数を省略できると思った
        
        while next_item:
            if next_item.key == key:
                if previous_item == None:
                    self.item_count -= 1
                    self.buckets[bucket_index] = next_item.next # 先頭ノードを削除した場合、このハッシュテーブルの先頭アドレス自体も更新する必要がある
                    flg = 1
                else:
                    previous_item.next = next_item.next
                    self.item_count -= 1
                    flg = 1
                return True
            previous_item = next_item #現在いる部分のアドレスを格納したい
            next_item = next_item.next
        if flg == 0:
            return False
        
    # rehash function
    # newsize => new bucket_size
    # 新たに指定したサイズに再ハッシュする関数
    def rehash(self,newsize):
        self.bucket_size = newsize
        old_buckets = self.buckets
        self.buckets = [None] * newsize
        # pld_bucketsに格納されている全てのインデックスについて探索（ただし全ての要素の中身はlinked list）
        for putitem in old_buckets:
            # putitem自体がlinked listの先頭要素のはず
            while putitem:
                # putと同じ実装（ただし同じものは2度と出現しないのでその仮定は不要）
                # 新しいインデックスを計算
                bucket_index = calculate_hash(putitem.key) % self.bucket_size
                # new_itemの三つ目の要素は現在のlinkedlistの先頭要素、それをnextに格納することで連結させることができる
                new_item = Item(putitem.key, putitem.value, self.buckets[bucket_index])
                # 新たなlinked listを格納
                self.buckets[bucket_index] = new_item
                #元のインデックスに格納されていた次の要素について探索する 
                putitem = putitem.next   

    # ハッシュテーブルを大きくする場合（2倍）
    # 必ず奇数にするにはself.bucket_size*2+1
    def update_hash_bigger(self):
        self.rehash(self.bucket_size*2)
    
    # ハッシュテーブルを小さくする場合（1/2倍）
    # 必ず奇数にするには(self.bucket_size//2)+(self.bucket_size%2+1)
    def update_hash_smaller(self):
        self.rehash(self.bucket_size//2)
    
    

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
