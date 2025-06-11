#! /usr/bin/python3
import math

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# 掛け算
def read_times(line,index):
    token = {'type':'TIMES'}
    return token,index + 1

# 割り算
def read_devision(line,index):
    token = {"type":'DEVISION'}
    return token,index + 1

# 始まりの括弧の読み取り
def read_parentheses_opening(line,index):
    token = {"type":"openparentheses"}
    return token,index + 1

# 終わりの括弧の読み取り
def read_parentheses_closing(line,index):
    token = {"type":"closeparentheses"}
    return token,index + 1

# abs(の読み取り
def read_abs(line,index):
    token = {"type":"abs"}
    return token,index + 3

# int読み取り
def read_int(line,index):
    token = {"type":"int"}
    return token,index + 3

# round読み取り
def read_round(line,index):
    token = {"type":"round"}
    return token,index + 5

def tokenize(line):
    tokens = []
    index = 0

    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_devision(line, index)
        elif line[index] == '(':
            (token, index) = read_parentheses_opening(line, index)
        elif line[index] == ')':
            (token, index) = read_parentheses_closing(line, index)
        elif line[index] == 'a':
            # for abs
            (token, index) = read_abs(line, index)
        elif line[index] == 'i':
            # for int
            (token, index) = read_int(line, index)
        elif line[index] == 'r':
            # for int
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# tokensを受け取ったら掛け算割り算を行う関数
def calculate_times_devisions(tokens):

    index = 1
    
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':

            # 掛け算の場合
            # 現在参照している数値の一つ前のインデックスが*なら
            # 二つ前のインデックスと現在参照しているインデックスを掛け算して、現在のインデックスを計算結果に更新
            # 二つ前のインデックスと、*は不要なため削除

            if tokens[index - 1]['type'] == 'TIMES':
                
                times_number = tokens[index-2]['number'] * tokens[index]['number']
                tokens[index]['number'] = times_number

                # 二つ前のインデックスを削除、一つ前のインデックスを削除（ただしポップすることで配列の長さが変わるため調整する必要がありindex-2としている）
                # 配列の長さが変わってしまうため、indexの調整を含める
                # インデックス調整用のデバッグも含めたコード

                poped1 = tokens.pop(index-2)
                # print("poped1",poped1)
                poped2 = tokens.pop(index-2)
                # print("poped2",poped2)
                index -= 2


            # 割り算の場合
            # 現在参照している数値の一つ前のインデックスが*なら
            # 二つ前のインデックスと現在参照しているインデックスを割り算して、現在のインデックスを計算結果に更新
            # 二つ前のインデックスと、/は不要なため削除
                    
            elif tokens[index - 1]['type'] == 'DEVISION':
                times_number = tokens[index-2]['number'] / tokens[index]['number']
                tokens[index]['number'] = times_number
                tokens.pop(index-2)
                tokens.pop(index-2)
                index -= 2
                    
            # どちらでもなければ何もしなくて良い
            else:
                # デバッグ用
                # print('this function is not times or devision')
                pass

        index += 1
    
    return tokens

# tokensを受け取ったら足し算引き算を行う
def calculate_plus_minus(tokens):
    answer = 0
    index = 1
    # 足し算引き算の計算をする 
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax pulus minus')
                exit(1)
        index += 1

    return answer

# 閉じ括弧のインデックスとtokenを受け取ったら一つ前の開き括弧を探しに行き、indexを返す関数
def search_openparentheses(index,token):

    for searchindex in reversed(range(index)):

        if token[searchindex]["type"] == "openparentheses":
            # for debug
            # print("this is open index",searchindex)
            return searchindex
        
    return False

# tokenを受け取ったら括弧の計算をする関数
def calculate_parentheses(tokens):
    index = 0
    while index < len(tokens):

        # もし閉じかっこを見つけたら、一つ前のopenparenthesesを探しに行く
        if tokens[index]['type'] == 'closeparentheses':
            openparentheses_index = search_openparentheses(index,tokens)

            assert openparentheses_index != False

            # 一つ前の開きかっこ〜閉じかっこまでを新たにtokenとしてevaluateに渡す（再帰的に括弧内の計算を行う）
            # この範囲内の要素を元のtokenから削除し、type == NUMBER　として新たに計算した値を元のtokenに渡す

            minimum_token = tokens[openparentheses_index+1:index]
            new_number = evaluate(minimum_token)
            
            # 削除する要素数をカウントしtokenから削除
            cut_index_count = index - openparentheses_index + 1

            # これを用いれば簡単にpopすることができるよ(メンターさん)
            # del list[start:end]
            for cut in range(cut_index_count):
                tokens.pop(openparentheses_index)

            
            # 元々開きかっこが存在していた位置に数字を格納
            tokens.insert(openparentheses_index,{'type': 'NUMBER', 'number': new_number})

            # tokenの長さが変わるので、index調整
            index = index - cut_index_count + 1
            
        index += 1
    
    # for debug
    # print("this is after parentheses",tokens)

    return tokens


# tokenを受け取ったらabsの計算を行う関数
# absの後ろをevaluateしてそれがマイナスならプラスに変換する処理を行う

def calculate_abs(tokens):

    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'abs':
            
             # 先に括弧の計算を行っているので
            # {"type":"abs"}{'type': 'NUMBER', 'number': n}
            # という順番に並んでいるはず

            abs_number = tokens[index+1]['number']

            if abs_number < 0:
                abs_number = abs(abs_number)

            # {"type":"int"}{'type': 'NUMBER', 'number': n}のまとまりを削除し、
            # {'type': 'NUMBER', 'number': int_number}を元のindexに代入する
            # indexの調整を行う

            del tokens[index:index+2]
            tokens.insert(index,{'type': 'NUMBER', 'number': abs_number})
            index -= 1   
        index += 1

    # for debug
    # print("this is after abs tokens",tokens)

    return tokens

# tokenを受け取ったらintの計算を行う関数
# intの後ろをevaluateして切り捨てる計算を行う

def calculate_int(tokens):

    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'int':
            
            # 先に括弧の計算を行っているので
            # {"type":"int"}{'type': 'NUMBER', 'number': n}
            # という順番に並んでいるはず

            int_number = tokens[index+1]['number']

            # もしfloat型ならintに変換する
            if isinstance(int_number, float):
                int_number = int(int_number)

            # {"type":"int"}{'type': 'NUMBER', 'number': n}のまとまりを削除し、
            # {'type': 'NUMBER', 'number': int_number}を元のindexに代入する
            # indexの調整を行う

            del tokens[index:index+2]
            tokens.insert(index,{'type': 'NUMBER', 'number': int_number})
            index -= 1

        index += 1

    # for debug
    # print("this is after abs tokens",tokens)

    return tokens


# tokenを受け取ったらroundの計算を行う関数
# roundの後ろをevaluateして四捨五入する

def calculate_round(tokens):

    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'round':
            
            # 先に括弧の計算を行っているので
            # {"type":"round"}{'type': 'NUMBER', 'number': n}
            # という順番に並んでいるはず

            round_number = tokens[index+1]['number']

            round_number = round(round_number)

            # {"type":"int"}{'type': 'NUMBER', 'number': n}のまとまりを削除し、
            # {'type': 'NUMBER', 'number': int_number}を元のindexに代入する
            # indexの調整を行う

            del tokens[index:index+2]
            tokens.insert(index,{'type': 'NUMBER', 'number': round_number})
            index -= 1

        index += 1

    # for debug
    # print("this is after abs tokens",tokens)

    return tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token

    # デバッグ
    # print("this is token test",tokens)

    # 先に括弧の計算を行う
    tokens = calculate_parentheses(tokens)
    
    # その後abs,int,roundの計算を行う
    # この順番にすることでabs,int,roundの後ろは必ず{NUMBER}になる
    tokens = calculate_abs(tokens)
    tokens = calculate_int(tokens)
    tokens = calculate_round(tokens)

    # tokensを渡したら掛け算割り算を行う
    # 足し算引き算よりも優先度を上げて計算する
    tokens = calculate_times_devisions(tokens)
    
    # デバッグ
    # print("this is token test after times and dexvison",tokens)

    # 足し算引き算を行う
    answer = calculate_plus_minus(tokens)

    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    # for homework2
    print("==== Test started for homework2! ====")
    test("2")
    test("3+4")
    test("2.0+3")
    test("2.3+4.0")
    test("-3")
    test("4-3")
    test("3-4")
    test("3.0-4")
    test("4.0-3.0")
    test("1+3+4-2")
    test("-3+2-5")
    test("-4.0+3.0-3")
    test("2*3")
    test("2.0*3.0")
    test("2*3.0")
    test("2.3*4.5")
    test("5/2")
    test("5.0/2")
    test("5.0/2.0")
    test("5.0/2.0/3")
    test("5*4/2")
    test("5.0*4.0*2.0/2.0/3")

    # for homework3
    print("==== Test started for homework3! ====")
    test("(3)")
    test("(-2)")
    test("(3+4)")
    test("(3*4)+(2+4)")
    test("((5-1)/(3-1))*5+(8*9)")
    test("(6+(9+7))/2")
    test("(((2.0+3)/2*5)+(8+9))/2.0")

    #for homework4 abs 
    print("==== Test started for homework4 abs! ====")
    test("abs(-3)")
    test("abs(3)")
    test("abs(-3+4)")
   #for homework4 int
    print("==== Test started for homework4 int! ====")
    test("int(-3.0)")
    test("int(3.0)")
    test("int(-3.12+4.15)")

   #for homework4 round
    print("==== Test started for homework4 round! ====")
    test("round(-3.54)")
    test("round(3.2)")
    test("round(-3.12+4.15)")

   #for homework4 mix
    print("==== Test started for homework4! ====")
    test("round(-3.54)+int(abs(-3.65))")
    test("round(3.2+int(5.78)+abs(-3.56+int(5.2)))")
    test("abs(-3.12+4.15+round(3.89)+abs(int(-4.6)+round(3.0)))")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
