# Rectangle image to square with Python
長方形の画像を正方形にして出力するスクリプト

* 長方形に余白を付けて正方形に
* 長方形の中心から最大の正方形を切り出す
* [Unimplemented] 長方形を正方形に変形


## 使い方
### pythonパッケージをインストール

```bash
pip install opencv-python
```

### ディレクトリ構造
以下のようなディレクトリ構造に。

```
.
├── README.md
├── rectangle-image2square.py
├── input
│   ├── class1
│   │   ├── class1_1.jpg
│   │   ├── class1_10.jpg
│   │   ├── class1_11.jpg
│   ├── class2
│   │   ├── class2_1.jpg
│   │   ├── class2_10.jpg
│   │   ├── class2_11.jpg
│   └── class3
│       ├── class3_1.jpg
│       ├── class3_10.jpg
│       └── class3_11.jpg
└── output
```

### 実行

#### Options
| Option       | Default parameter | Description               |
|:-------------|:------------------|:--------------------------|
| --input_path | `./input/`        | 入力ディレクトリのパス    |
| --method     | `wrap`            | wrap: 余白入り正方形<br>fit: 長方形から取得できる最大の正方形       |
| --resize     | `0 (無効)`        | 出力画像サイズ            |

#### Run
```bash
python rectangle-image2square.py [--input_path "./input/"] [--resize 224] [--method <wrap or fit>]
```
