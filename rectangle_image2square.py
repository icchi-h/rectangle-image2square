#!/usr/bin/env python
# coding: utf-8

"""
__doc__
長方形の画像を正方形にして出力するスクリプト
"""

__author__ = "Haruyuki Ichino"
__version__ = "1.4"
__date__ = "2017/09/21"

print(__doc__)

import sys
import os
import glob
import argparse
import numpy as np
import cv2
import imghdr
from scipy import ndimage
from datetime import datetime


def rectangle2square(image, method="wrap", margin_color=255):
    height, width, channels = image.shape

    if method is "wrap":
        max_length = max(width, height)
        min_length = min(width, height)
        start = int((max_length - min_length) / 2)
        end = int((max_length + min_length) / 2)

        # 背景画像の生成
        base_img = np.zeros((max_length, max_length, channels), dtype=np.uint8)
        base_img.fill(margin_color)

        # 上書き
        base_img[start:end, :] = image
        # 縦画像の場合: base_img[:, start:end] = org_img
        square_img = base_img
    else:
        min_length = min(width, height)
        center_x = int(width / 2)
        center_y = int(height / 2)
        offset = int(min_length / 2)

        left = int(center_x - offset)
        top = int(center_y - offset)
        right = int(center_x + offset)
        bottom = int(center_y + offset)

        # 画像の切り出し
        square_img = image[top:bottom, left:right]

    return square_img


if __name__ == '__main__':

    # const
    MARGIN_COLOR = 255 # white

    # オプションの設定
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        type=str,
        default="./input/",
        help="Input directory path."
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="./output/",
        help="Output directory path."
    )
    parser.add_argument(
        "--method",
        type=str,
        default="wrap",
        help="Transrate method [wrap or fit]"
    )
    parser.add_argument(
        "--resize",
        type=int,
        default=0,
        help="Output image size."
    )
    # パラメータ取得と実行
    FLAGS, unparsed = parser.parse_known_args()

    # 入力ディレクトリの存在確認
    if not os.path.isdir(FLAGS.input_path):
        print("Error: Not found input directory")
        sys.exit(1)

    # 出力ディレクトリの存在確認
    if not os.path.exists(FLAGS.output_path):
        os.makedirs(FLAGS.output_path)

    # ログ出力の準備
    log_dir = "./log/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    log_file = os.path.join(log_dir, 'faild-files_' + now_str + '.txt')
    f = open(log_file, 'w')


    # counter
    total_image_count = 0
    success_count = 0


    print("Processing...")

    # 各クラスディレクトリ
    classes = sorted(os.listdir(FLAGS.input_path))
    for tclass in classes:

        # .DS_Storeのチェック
        if tclass == ".DS_Store":
            continue

        class_path = os.path.join(FLAGS.input_path, tclass)

        # ディレクトリじゃない場合はスキップ
        if not os.path.isdir(class_path):
            continue

        # 出力用のクラスディレクトリを作成
        output_class_path = os.path.join(FLAGS.output_path, tclass)
        if not os.path.exists(output_class_path):
            os.makedirs(output_class_path)

        print("Class: " + tclass + " ---------------------------------")
        image_paths = sorted(glob.glob(os.path.join(class_path, '*.*[gG]')))
        total_image_count += len(image_paths)
        count = 1
        for image_path in image_paths:
            # 画像チェック
            if imghdr.what(image_path) is None:
                print("Error: Not image " + image_path)
                continue

            # 集めた画像データから顔が検知されたら、切り取り、保存する。
            print("["+str(count)+"/"+str(len(image_paths))+"] " + image_path)

            image = cv2.imread(image_path)
            height, width, channels = image.shape

            # 縦画像のチェック
            if height > width:
                print("\tError: 読み込まれた画像が縦画像です")
                f.write("元縦画像: " + image_path + "\n")

                # 回転
                angle = -90
                image = ndimage.rotate(image, angle)
                print("\tProcessed: 横画像に修正")

            # processing
            square_img = rectangle2square(image, FLAGS.method, MARGIN_COLOR)

            # 画像のりサイズ
            if (FLAGS.resize):
                try:
                    square_img = cv2.resize(square_img, (FLAGS.resize, FLAGS.resize))
                except:
                    print("\tError: Faild to resize cropped image")
                    continue

            #切り取った画像出力
            filename = os.path.basename(image_path)
            output_file = os.path.join(output_class_path, filename)
            cv2.imwrite(output_file, square_img)
            print("\tSaved: overlay image '" + output_file + "'")

            success_count += 1
            count += 1

    f.close()

    print()
    try:
        print("Success Rate: " + str(round(success_count/total_image_count*100, 2)) + "% (" + str(success_count) + "/" + str(total_image_count) + ")")
    except:
        print("Success Rate: 0% (0/0)")
    print("Completed")
