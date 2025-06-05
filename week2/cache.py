import sys
import hash_table

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!



class Cacheitem:

    def __init__(self,contents,url,next,prev):
        self.contents = contents
        self.url = url
        self.next = next
        self.prev = prev

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    # hash:HashTable from hash_table
    # head: head node of cache
    # tail:tail node of cache

    def __init__(self, n):
        self.count_node = n 
        self.hash= hash_table.HashTable()
        self.head = None
        self.tail = None

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        
        # もし以前にアクセスしていなければ
        # 新たなデータ作成
        # stored:(item.value, True) or (None, False)
        stored = self.hash.get(url)

        if stored == (None,False):
            new_cacheitem = Cacheitem(contents,url,self.head,None)

            #cacheが満タンの場合 
            if self.count_node == 0:
        
                # 先頭更新
                self.hash.put(url,new_cacheitem)
                new_cacheitem.next = self.head
                if self.head:
                    self.head.prev = new_cacheitem
                self.head = new_cacheitem

                # 最後削除
                self.hash.delete(self.tail.url)
                # 2要素以上存在していた場合
                if self.tail.prev:
                    self.tail = self.tail.prev
                    self.tail.next = None
                # 1要素しかない時
                elif self.tail:
                    self.tail = new_cacheitem

            # cacheにあまりがある時
            else:
                # データをハッシュに追加し、先頭更新
                self.hash.put(url,new_cacheitem)
                new_cacheitem.next = self.head

                if self.head:
                    self.head.prev = new_cacheitem
                self.head = new_cacheitem

                # もしcache内の一つ目の要素であればtailとしても登録しておく
                if self.tail == None:
                    self.tail = new_cacheitem
                
                # 容量更新
                self.count_node -= 1
        
        # アクセスしていれば、その要素を先頭に持ってくる必要がある 
        else:
            stored = stored[0]

            # もしこの要素が先頭なら何もしなくて良い
            if stored == self.head:
                return

            # 前後の要素を更新する
            # 前の要素があった場合
            if stored.prev:
                stored.prev.next = stored.next
            # 後ろの要素があった場合
            if stored.next:
                stored.next.prev = stored.prev
                # print("kokodekiteru??")
            
            # もしこの要素がtailと一致していたらtailの更新が必要
            if stored == self.tail:
                self.tail = stored.prev
                # print("tail kousinn!!")
            
            # 先頭要素に関して更新
            self.head.prev = stored
            stored.next = self.head
            stored.prev = None
            self.head = stored

            # この目的の要素のハッシュテーブル更新
            self.hash.delete(stored.url)
            self.hash.put(stored.url,stored)
            
        

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
       
        # ret_list :最後に返すリスト
        # node :現在の探索ノード、初期値は先頭ノード
        ret_list = []
        node = self.head
        while node:
            ret_list.append(node.url)
            node = node.next
        
        # print(ret_list)
        return ret_list


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
