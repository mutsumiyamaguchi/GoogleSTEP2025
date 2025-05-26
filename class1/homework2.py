# 与えられた文字列の全てを用いなくてもいいように関数をアップグレードする

"""
1 与えられた文字列の文字数以下の文字の組み合わせを全て羅列して、1の時と同じように辞書、および入力文字を昇順にソート、探索
O(m)+O(2^n)*O(logm)

2 アナグラムが作れる=>出現文字をカウントして、それ以下のものであれば作ることができる
線形探索をして全ての文字列を取り出すようにする
O(m) + O(1) +O(m)

プログラムを書いて見て思ったこととして、今回の内容であればソートの必要はなかったのかなと感じた
"""

def sortcount_str(str):
    # ans = {"sorted":{"original":{counter}}}
    ans = {}

    # sort string
    lst = list(str)
    lst.sort
    word = "".join(lst)

    # counter = {"a":2,"b":3..}
    appeared = set()
    counter = {}
    for i in lst:
        if i not in appeared:
            counter[i] = 1
            appeared.add(i)
        else:
            counter[i] += 1

    ans[word] = {}
    ans[str][str] = counter
    
    return ans

def dictionary_sort(dictionary):
    newdictionary = []

    for i in dictionary:
        ans = {}

        # sort string
        lst = list(i)
        lst.sort
        word = "".join(lst)

        # counter = {"a":2,"b":3..}
        appeared = set()
        counter = {}
        for j in lst:
            if j not in appeared:
                counter[j] = 1
                appeared.add(j)
            else:
                counter[j] += 1

        ans[word] = {}
        ans[word][i] = counter

        newdictionary.append(ans)

    return newdictionary

def liner_search(target,dictionary):
    ans = []
    print("this is liner_search",target)
    
    # 辞書型の分解にfor文が必要
    for target_sorted,target_dic in target.items():
        for target_original,target_counter in target_dic.items():

            # 線形探索
            for i in dictionary:
                flag = 0
                for sorted,dic in i.items():
                    for original,counter in dic.items():
                        # print("kakuninn",original,counter,sorted,target_original)
                        # print("kakunin1",counter.keys())

                        # それぞれの文字についてtargetよりも数が少なければ良い、=>おおかったらbreakしてflagを立てる
                        for alpha in counter.keys():
                            # print("kakuninn2",alpha)

                            # 辞書の文字がtargetの文字として登場しない場合=>break
                            if alpha not in target_counter.keys():
                                flag = 1 #breakflag
                                break
                            else:
                                # print("koreha??",counter[alpha])
                                # 文字として登場しているけれど数が多い場合=>break
                                if counter[alpha] > target_counter[alpha]:
                                    flag = 1
                                    break
                        if flag == 0:
                            ans.append(original)
    return ans


def best_solution(random_word,dictionary):

    sorted_word = sortcount_str(random_word)
    
    answer = liner_search(sorted_word,dictionary)

    return answer

def main():

    # 辞書読み込み
    f = open('./words.txt', 'r', encoding='UTF-8')
    dictionary = f.read().splitlines()
    f.close()

    newdictionary = dictionary_sort(dictionary)

    # target読み込み
    f = open("./small.txt","r",encoding = "UTF-8")
    targetlst = f.read().splitlines()
    f.close

    for i in targetlst:
        print("this is i",i)
        lst = best_solution(i,newdictionary)
        print(lst)
        
        with open("small_ans.txt", mode='a', encoding='UTF-8') as f:
            f.write("[DEBUG]anagram for:"+i)
            for word in lst:
                f.write(word+"\n")
    


# このファイルを実行したときだけmain()を呼び出す
if __name__ == "__main__":
    main()
