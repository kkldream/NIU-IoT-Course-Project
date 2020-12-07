# Web API 功能

## 網路位置 (暫定)

客戶端首頁位置：http://120.101.8.240:5000/

影像串流位置：http://120.101.8.240:5000/stream

API位置：http://120.101.8.240:5000/api

## 使用者操作

### 獲取狀態
#### 輸入：`POST`
![](https://i.imgur.com/bzGgwdN.png)  
#### 輸出：`JSON`
status = 目前狀態  
student_id = 觸發此狀態的使用者  
![](https://i.imgur.com/NzxMXM4.png)  

### 驗證登入
#### 輸入：`POST`
變數：`student_id` & `password`  
![](https://i.imgur.com/6xDvVvW.png)  
#### 輸出：`字串`
`True` or `False`  

### 停機操作
會刷新狀態  
#### 輸入：`POST`
變數：`student_id` & `password`  
![](https://i.imgur.com/tzlSzow.png)  
#### 輸出：`字串`
`True` or `False`  

## 開發人員操作

### 開機操作
會刷新狀態  
#### 輸入：`POST`
變數：`student_id`  
![](https://i.imgur.com/qrBdBi0.png)  
#### 輸出：`字串`
`True` or `False`  

### 查詢狀態列表
#### 輸入：`POST`  
變數：`num` = 顯示最後幾個狀態數量  
![](https://i.imgur.com/s2dhey3.png)  
#### 輸出：`字串`
![](https://i.imgur.com/NGb5Epq.png)  

### 查詢使用者列表
#### 輸入：`POST`  
![](https://i.imgur.com/rcev7K3.png)  
#### 輸出：`字串`
![](https://i.imgur.com/GGDzLXG.png)  

### 新增使用者
#### 輸入：`POST`
變數：  
`card_id` = 卡號  
`password` = 密碼  
`student_id` = 學號  
`email` = 信箱 (選填)  
`phone` = 電話 (選填)  
`description` = 描述 (選填)  
![](https://i.imgur.com/5u45wRo.png)  
#### 輸出：`字串`
`True` or `False`  

### 刪除使用者
#### 輸入：`POST`
變數：`student_id`  
![](https://i.imgur.com/SnZ6uU7.png)  
#### 輸出：`字串`
`True` or `False`  