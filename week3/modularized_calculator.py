#! /usr/bin/python3

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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# tokensを受け取ったら掛け算割り算を行う関数
def caluculate_times_devisions(tokens):

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
                print('this function is not times or devision')
    
        index += 1
    
    return tokens

# tokensを受け取ったら足し算引き算を行う
def caluculate_plus_minus(tokens):
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



def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token

    # デバッグ
    print("this is token test",tokens)

    # tokensを渡したら掛け算割り算を行う
    tokens = caluculate_times_devisions(tokens)
    
    # デバッグ
    print("this is token test after times and dexvison",tokens)

    # 足し算引き算を行う
    answer = caluculate_plus_minus(tokens)

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
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
