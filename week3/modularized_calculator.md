# modularized_calcuator.pyのドキュメント

## 実装したもの

- 掛け算、割り算
- 括弧の計算
- abs,int,round

## 方針

### 掛け算割り算

1. (足し算引き座の時と同じように)"*"または"/"を読み取ったらそれぞれ{"type":"TIMES"},{"type":"DEVISION"}というtokenをtokens配列に格納する
2. evaluate関数にtokens配列を渡し、calculate_times_devisions(tokens)を実行する。この関数は、type = TIMESであれば前後のNUMBERを掛け算し、DEVISIONであれば前後の数を割り算する。
3. evaluate関数の中で掛け算、割り算の計算を足し算引き算よりも先に実行させることで足し算引き算よりも先に掛け算割り算の実行をさせることができる

### 括弧の計算

1. 文字列の読み取りの時には"("を{"type":"openparentheses"}として、")"を{"type":"closeparentheses"}としてtokens配列に格納する
2. calculate_parentheses(tokens)という関数について、以下の方法で実装した
    - 閉じかっこを見つけたらそれ以前を探索し開きかっこを見つける
    - 開きかっこから閉じかっこまでを小さなtokens配列として再帰的にevaluate関数に渡す
    - その中身は必ずtyoe = NUMBERとなるので開きかっこから閉じかっこまでの計算を行ったことと同様の値を得ることができる
    - 小さなtokens配列の範囲をNUMBERとして格納しindexを調整する
3. evaluate関数の中でcalculate_parentheses(tokens)という関数を掛け算割り算を行う関数よりも先に呼び出すことで括弧の計算の優先度を高くする

### abs,int,round

1. 文字列の読み取りの時には"a"という文字を読んだら{"type":"abs"}、"i"という文字を読んだら{"type":"int"}、"r"落ち雨文字を読んだらあ{"type":"round"}としてtokens配列に格納する　=> この時absという文字列は3文字で構成されているのでindexの調整を行う。同様の考え方でintおよびroundについてもindexの処理を行う
2. calculate_abs(tokens)、calculate_int(tokens)、calculate_round(tokens)という関数について、それぞれ以下のような方針で実装した
    - 入力文字列は"abs(計算式)"、または"int(計算式)"、"round(計算式)"という形式で渡されるのでevaluate関数の中で括弧の計算を行う関数を先に呼び出し、その後absなどを呼び出す　->このようにすることでtokens配列の並び順は必ず{"type":"abs" or "type":"int" or"type":"round"}{"type":"NUMBER"}となるのでtype:absなどの直後に存在しているnumberに関して次のような手順を施す
        - absについて、numberが負の数であれば正にする。tokens配列のついてはabsというtokenを削除し、numberを更新した後indexの調整を行う
        - intについて、numberの型を調べてfloatであればintにcastする。tokens配列についてはintというtokenを削除し、numberを更新した後indexの調整を行う
        - roundについて、numberに関わらずpythonの標準ライブラリに存在しているround()に渡す。適切に処理をされて帰ってくるのでnumberの更新を行う。tokens配列についてはroundというtokenを削除し、numberを正しく更新した後indexの調整を行う
3. 2で記載の通り、evaluate関数について括弧の計算を行う関数を呼び出した後abs,int,round関数を呼び出す。これら三つについてはそれぞれの優先度は同じなのでどの順に呼び出しても実行結果は同じになるはずである。その後掛け算割り算、足し算引き算を呼び出すことで計算機を実装した。

### テストケース、およびデバッグ

- 整数少数、足し算引き算掛け算割り算について一番小さい値から入り子になっているものまで用意することでデバッグをする際に役立てることができた。
- 具体的にはabs,int,roundのコードで元々書いていたものでは小さいテストケースはpassできるものの入り子になっているものにはfailとなってしまい実行することができていなかった
- デバッグする際には主にtokens配列がどのような動きになっているかを追うことで挙動の正確性を確認した。

### 気がついたこと

1. 足し算引き算、掛け算割り算の時と同じようにabs,int,roundの計算に関しても、優先度が同等であるのならば一つの関数にまとめた方が見やすいコードになると考えた。