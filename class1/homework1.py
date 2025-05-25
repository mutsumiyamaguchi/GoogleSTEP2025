# 与えられた文字列のAnagramを辞書ファイルから探して返すプログラムを作成する

"""
考え方
1 入力文字列の並び方を全て書き出してそれぞれ辞書と照合
入力文字数n、辞書mの時
入力文字列の総数=>n*n-1*n-2*,,,,=n!
さらに辞書mなので線形探索でO(n!*m)
二分探索でO(n!*logm)

2
アナグラムなので最終的に文字が作れればいい=>文字順は関係ない、辞書にその文字が存在していることが確認できればいい
入力文字列をソートO(1)
辞書も全ての単語について昇順にソート=>O(m)
そして線形探索をして一致するか全ての場合の一致を確認する（二分探索をすれば一つ見つけられても複数見つけられないと考えたため）=>O(m)
つまり計算量は0(1)+O(m)+O(m) => O(m)
"""

def sort_str(str):
    
    lst = list(str)
    lst.sort()
    resstr = "".join(lst)
    print(resstr)

    return resstr



def better_solution(random_word,dictionary):
    sorted_word = sort_str(random_word)

    newdictionary = []
    # newdictionary = [{"sorted":"original"}....]
    for i in dictionary:
        dic_word_sorted = sort_str(i)
        newdata = {}
        newdata[dic_word_sorted] = i
        newdictionary.append(newdata)
    
    # print(len(newdictionary))

    answer = []
    for i in newdictionary:
        # print(i.keys())
        # print(sorted_word)

        # このdictの使い方覚える！！！！
        for key,val in i.items():
            if key == sorted_word:
                answer.append(val)
            

    return answer

def main():
    print("input randomword")
    randomword = input()

    # ファイル読み込み
    f = open('./words.txt', 'r', encoding='UTF-8')
    dictionary = f.read().splitlines()
    f.close()

    ans = better_solution(randomword,dictionary)
    if len(ans) >=1: #見つかった場合
        # ans.remove(randomword) 入力文字そのものもアナグラム？
        for i in ans:
            print("this is anagram:",i)
    else:
        print("no anagram for this strings")
   


# このファイルを実行したときだけmain()を呼び出す
if __name__ == "__main__":
    main()


"""
テストケース(入力文字そのものはアナグラムなのか否か聞く)
1 cat =>this is anagram: act
        this is anagram: cat
2 から文字 =>no anagram for this strings
3 pale
this is anagram: leap
this is anagram: pale
this is anagram: peal
this is anagram: plea

4 a
this is anagram: a
"""