# 与えられた文字列の全てを用いなくてもいいように関数をアップグレードする

"""
1 与えられた文字列の文字数以下の文字の組み合わせを全て羅列して、1の時と同じように辞書、および入力文字を昇順にソート、探索
O(m)+O(2^n)*O(logm)

2 アナグラムが作れる=>出現文字をカウントして、それ以下のものであれば作ることができる
線形探索をして全ての文字列を取り出すようにする
O(m) + O(1) +O(m)

? 全ての文字列を取り出したとして、どれを採用するのかというのはどのように決めたらいいのかわからない
A calculateしてしまい、それを辞書として格納、スコアが高い順にソートした上で線形探索、見つかったらそれを返し、breakすることで計算量削減

? largeを実行した時にすごく時間がかかったので二分探索を採用するべきであると思う。そうするとどの単語か使われるのかというのが辞書の長さに関わってくると思うが、どうすればスコアが高くなるのかわからない
A 二分探索は難しいので線形探索でできるだけ早い方法、スコアが高い方法を採用

プログラムを書いて見て思ったこととして、今回の内容であればソートの必要はなかったのかなと感じた
=> 省略
"""

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score


def sortcount_str(word):
    # ans = {"score":{"original":{counter}}}
    ans = {}

    """
    ソート不要であることに気が付いたので省略
    # sort string
    lst = list(str)
    lst.sort
    word = "".join(lst)
    """

    # score計算
    score = calculate_score(word)
    lst = list(word)

    # counter = {"a":2,"b":3..}
    appeared = set()
    counter = {}
    for i in lst:
        if i not in appeared:
            counter[i] = 1
            appeared.add(i)
        else:
            counter[i] += 1

    ans[score] = {}
    ans[score][word] = counter
    
    return ans

def dictionary_sort(dictionary):
    newdictionary = []

    for i in dictionary:
        ans = {}

        # # sort string
        # lst = list(i)
        # lst.sort
        # word = "".join(lst)

        # score
        score = calculate_score(i)

        # counter = {"a":2,"b":3..}
        appeared = set()
        counter = {}
        lst = list(i)
        for j in lst:
            if j not in appeared:
                counter[j] = 1
                appeared.add(j)
            else:
                counter[j] += 1

        ans[score] = {}
        ans[score][i] = counter

        newdictionary.append(ans)

    return newdictionary

def liner_search(target,dictionary):
    ans = []
    # print("this is liner_search",target)
    breakflag = 0
    
    # 辞書型の分解にfor文が必要
    for target_sorted,target_dic in target.items():
        for target_original,target_counter in target_dic.items():

            # 線形探索
            for i in dictionary:
                if breakflag ==1:
                    break
                else:
                    flag = 0
                    for score,dic in i.items():
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
                                # print(score)
                                # print(original)
                                ans.append(original)
                                breakflag = 1
                                # print("kakuninn1",ans)
    # print("kakuninn2",ans)                 
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
    newdictionary = sorted(newdictionary, key = lambda d: list(d.keys())[0],reverse=True)

    # target読み込み
    f = open("./large.txt","r",encoding = "UTF-8")
    targetlst = f.read().splitlines()
    f.close

    for i in targetlst:
        # print("this is i",i)
        lst = best_solution(i,newdictionary)
        # print(lst)
        
        # mode = 'a'というのが追記モード
        with open("large_ans2.txt", mode='a', encoding='UTF-8') as f:
            # f.write("[DEBUG]anagram for:"+i+"\n")
            for word in lst:
                f.write(word+"\n")
    


# このファイルを実行したときだけmain()を呼び出す
if __name__ == "__main__":
    main()
