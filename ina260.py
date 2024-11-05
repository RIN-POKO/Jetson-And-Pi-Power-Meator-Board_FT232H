import os
os.environ['BLINKA_FT232H'] = '1'  # 環境変数の設定

import board
import busio
import time

# I2Cバスの初期化
i2c = busio.I2C(board.SCL, board.SDA)

# デバイスアドレスとレジスタアドレスの定義
device_address = 0x40
register_address = 0x02

# 継続的な測定ループ
while True:
    # I2C通信が準備できるまで待機
    while not i2c.try_lock():
        pass

    try:
        # レジスタアドレスを指定して書き込み
        i2c.writeto(device_address, bytes([register_address]))

        # データの読み取り
        buffer = bytearray(2)
        i2c.readfrom_into(device_address, buffer)

        # 16ビットのデータを取得し、バイトオーダーを変換
        word = (buffer[1] << 8) | buffer[0]  # 元のコードと同様のエンディアン変換
        result = ((word << 8) & 0xFF00) + (word >> 8)  # 上位と下位バイトの入れ替え

        # 電圧計算
        volt = result * 1.25 / 1000  # 1.25mVスケーリングを適用し、ボルトに変換

        # 結果を表示
        print("Voltage:", volt)

    finally:
        # I2Cロックを解除
        i2c.unlock()

    # 1秒待機
    time.sleep(1)
