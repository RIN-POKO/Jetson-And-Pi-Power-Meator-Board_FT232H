# Jetson-And-Pi-Power-Meator-Board_FT232H

[Jetson ＆ Pi 電力測定ボード](https://bit-trade-one.co.jp/adjtsb01/)を[FT232H](https://www.adafruit.com/product/2264#technical-details)経由で利用するためのスクリプトです。

電流、電圧、消費電力をリアルタイムでモニタリングするPythonスクリプトを提供します。

## セットアップ

1. **環境構築**

    ```bash
    pip install adafruit-circuitpython-ina260 matplotlib numpy
    ```

2. **接続**

   Jetson ＆ Pi 電力測定ボードとFT232HボードをI2Cで接続してください。

## 使用方法

### スクリプト1: ina260.py

電圧を1秒ごとに表示します。
adafruit_ina260ライブラリを使用せず、直接I2C通信を行います。

```bash
python3 ina260.py
```

### スクリプト2: ina260_adafruit.py

電流、電圧、消費電力をコンソールに表示します。

```bash
python3 ina260_adafruit.py
```

コンソールに以下の形式でデータが表示します。

 ```bash
 Current: 0.50 Voltage: 12.30 Power: 6.15
 ```

### スクリプト3: ina260_plot.py

電流、電圧、消費電力をリアルタイムでプロットします。

```bash
python3 ina260_plot.py
```

### スクリプト4: ina260_oled.py

電流、電圧、消費電力をOLEDディスプレイに表示します。

```bash
python3 oled_display.py
```
