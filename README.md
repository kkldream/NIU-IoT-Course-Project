# 1091_智慧物聯網概論與應用_專題

## 網路位置 (暫定)

客戶端首頁位置：http://120.101.8.132:5000/

影像串流位置：http://120.101.8.132:5000/stream

API位置：http://120.101.8.132:5000/api

## Web API 說明

[Web_API.md](Web_API.md)

## 上傳檔案
檔案網址 (Google Drive)：http://bit.ly/3dprintingdragon

目錄說明：
```
根目錄
│ Video.mp4 (實體操作錄影檔)
│
├─Android_APP (APP 目錄)
│  └─app
│     └─src
│        └─main
│            │ AndroidManifest.xml (屬性設定檔)
│            │
│            ├─java
│            │  └─com
│            │     └─example
│            │        └─application_webview
│            │             MainActivity.java (主程式)
│            │
│            └─res
│               └─layout
│                   activity_main.xml (介面布局)
│
└─Raspberry_Pi (Raspberry Pi 目錄)
    │  gpio.py (GPIO 控制函式庫)
    │  mysql.py (資料庫連接函式庫)
    │  rc522.py (讀卡機執行續)
    │  stream_server.py (伺服器串流主程式)
    │
    └─templates
        index.html (網頁登錄介面)
        login.html (網頁操作介面)
```
