# AntColonyOptimization
## Description
AntColonyOptimization(蟻コロニー最適化)とは、
組み合わせ最適化の確率的アルゴリズムである。  
メタヒューリスティクス手法群の１つ。  
<img src="data/aco_demo.gif" width=500>

## Reference
* Marco Dorigo: Ant Colony Optimization -Artificial Ants as a Computational Intelligence Technique-  
https://courses.cs.ut.ee/all/MTAT.03.238/2011K/uploads/Main/04129846.pdf

* 巽 啓司, 谷野 哲三『解の多様性を維持するアントコロニー最適化手法』  
http://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1526-30.pdf


## Environment
### Python version
Python 3.6.3 :: Anaconda, Inc.

### Requirements

```requirements.txt
certifi==2017.11.5
cycler==0.10.0
matplotlib==2.1.1
numpy==1.13.3
olefile==0.44
Pillow==4.3.0
pyparsing==2.2.0
python-dateutil==2.6.1
pytz==2017.3
PyYAML==3.12
six==1.11.0
```

## Usage
蟻コロニー最適化アルゴリズムを実行するには、  

1. `antColony.AntColony` クラスのインスタンスを生成
1. そのインスタンスが持つメソッド `run_optimizer()` または `run_optimizer_parallel()` を呼ぶ。

### input 
`antColony.AntColony` クラスのコンストラクタ引数は以下の様になる。

| 引数名 | Type | 備考 |
| :---: | :---: | :--- |
| nodes | dict | 都市番号がKey， 座標がValueである辞書 |
| ant_num_of_each_nodes | int  | 初期化時、各ノードに配置する蟻の数 |
| init_pheromone_value | float | 初期化時、各エッジのフェロモン量 |
| alpha | float | フェロモン量とエッジのコストの比重. 論文参照 |
| beta | float | フェロモン量とエッジのコストの比重. 論文参照 |
| rho | float | フェロモンの時間経過損失率 | 
| random | float | 蟻がランダム行動を起こす確率を決めるパラメータ |
| contrary | float | 蟻が行動法則と逆選択を起こす確率を決めるパラメータ |
| pheromone_constant | float | フェロモン更新時定数パラメータ | 
| iterations | int | 実行ステップ数 | 
| verbose | int | 途中結果出力頻度パラメータ． Noneで途中結果出力なし． | 

## デモ実行
1. リポジトリクローン

    `git clone git@github.com:keng000/AntColonyOptimization.git`

1. モジュールインストール

    ```
    pip install -r requirements.txt
    ```

1. デモの実行

    ```
    cd controllers

    # 数値演算スクリプト
    python antColony.py

    # 可視化スクリプト
    python antVisualizer.py
    ```

### サンプルデータの作りかた
背景画像差し替えや、探索するノードの設定方法。

1. 新しい画像を用意する。
    ここでは例として、`google_map_japan.png` を用意し、`data/` に配置する。  
    <img src="data/google_map_japan.png" width=500>

1. `tasks/create_dataset.py` の2つのパラメータを書き変える。  
    `img_path` : 新しく用意した画像へのパス.<br>
    `save_path` : 画像をプロットすることで入力した座標データのpickle保存パス.<br>

1. 座標の入力  
    `create_dataset.py` を実行すると、新しく用意した画像が `matplotlib.pyplot` によって表示される。  
    画像の任意の箇所をクリックすることで、その地点をノードに追加出来る。  
    TODO: 大変残変なことに、クリックしてもリアクションはない。本当は赤いドットみたいなのをプロットしたい。  

1. `controllers/antVisualizer.py` の2つのパラメータを書き換える。  
    `which_dataset` : どのデータセットpickleを使うか。ここでは上記 `create_dataset.py` の `save_path` に対応する。  
    `base_img_path`: 背景画像までのパス。 ここでは上記 `create_dataset.py` の `img_path` に対応する。  


## Author
宮川 健吾

