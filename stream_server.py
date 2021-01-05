from flask import Flask, request, Response, jsonify, render_template
from time import time, sleep
import mysql
import gpio
import cv2
import os
import threading
app = Flask(__name__)
# app.config["DEBUG"] = True
cap = cv2.VideoCapture(0)
INSIDE_HOST = '192.168.1.20'
OUT_HOST = '120.101.8.132'
PORT = 5000
gpio_out = False
@app.route('/', methods=['GET', 'POST'])
def home():
    global gpio_out
    if request.method == 'POST':
        action = request.values.get('action')
        # 停機
        if action == 'shutdown':
            student_id = request.values.get('student_id').upper()
            password = request.values.get('password')
            login_result = mysql.login_verification(student_id, password)
            status_result = mysql.get_latest_status()
            if student_id == status_result[1] and login_result is True:
                gpio_out = False
                mysql.insert_status(student_id,'shutdown')
                return render_template('login.html', host = OUT_HOST, port = PORT, student_id = student_id, password = password, shutdown = 'disabled', message = '無法操作：非當前使用者或機台尚未啟動')
        # 登出
        elif action == 'login out':
            status_result = mysql.get_latest_status()[3]
            if status_result == 'boot':
                return render_template('index.html', host = OUT_HOST, port = PORT, status = '(機器使用中)')
            else:
                return render_template('index.html', host = OUT_HOST, port = PORT, status = '(機器閒置中)')
        # 登入
        elif action == 'login':
            student_id = request.values.get('student_id').upper()
            password = request.values.get('password')
            login_result = mysql.login_verification(student_id, password)
            # 登入失敗
            if login_result is False:
                mysql.insert_status(student_id,'login fail')
                return render_template('index.html', host = OUT_HOST, port = PORT, error_message = '登入失敗：帳號或密碼錯誤')
            # 登入成功
            else:
                status_result = mysql.get_latest_status() # (datetime, student_id, card_id, status)
                # 當前使用者
                if status_result[1] == student_id:
                    mysql.insert_status(student_id.upper(),'login user')
                    if status_result[3] == 'boot':
                        return render_template('login.html', host = OUT_HOST, port = PORT, student_id = student_id, password = password, message = '操作警告：按下立即停機，需手動重啟')
                    else:
                        return render_template('login.html', host = OUT_HOST, port = PORT, student_id = student_id, password = password, shutdown = 'disabled', message = '無法操作：非當前使用者或機台尚未啟動')
                # 非當前使用者
                else:
                    mysql.insert_status(student_id,'login not user')
                    return render_template('login.html', host = OUT_HOST, port = PORT, student_id = student_id, shutdown = 'disabled', message = '無法操作：非當前使用者或機台尚未啟動')
    # GET 首頁
    status_result = mysql.get_latest_status()[3]
    if status_result == 'boot':
        return render_template('index.html', host = OUT_HOST, port = PORT, status = '(機器使用中)')
    else:
        return render_template('index.html', host = OUT_HOST, port = PORT, status = '(機器閒置中)')
        
@app.route('/api', methods=['POST'])
def api():
    global gpio_out
    action = request.values.get('action')
    if action == 'get_status':
        result = mysql.get_latest_status()
        return jsonify({'studio_id': result[1], 'status': result[3]})

    if action == 'login':
        student_id = request.values.get('student_id')
        password = request.values.get('password')
        login_result = mysql.login_verification(student_id, password)
        status_result = mysql.get_latest_status() # (datetime, student_id, card_id, status)
        if login_result is True:
            if status_result[1] == student_id:
                mysql.insert_status(student_id,'login user')
            else:
                mysql.insert_status(student_id,'login not user')
            return 'True'
        else:
            mysql.insert_status(student_id,'login fail')
            return 'False' 

    if action == 'shutdown':
        student_id = request.values.get('student_id')
        password = request.values.get('password')
        login_result = mysql.login_verification(student_id, password)
        status_result = mysql.get_latest_status()
        if student_id == status_result[1] and login_result is True:
            mysql.insert_status(student_id,'shutdown')
            return 'True'
        else:
            return 'False'

    if action == 'debug':
        key = request.values.get('key')
        if key == 'insert_status':
            student_id = request.values.get('student_id')
            status = request.values.get('status')
            if mysql.insert_status(student_id, status) is True:
                if status == 'boot':
                    gpio_out = True
                elif status == 'shutdown':
                    gpio_out = False
                return 'True'
        elif key == 'show_status':
            num = request.values.get('num')
            result = mysql.get_latest_status(num)
            str = '[datetime] student_id, card_id, status\n'
            for i in result: # (datetime, student_id, card_id, status)
                str += f'[{i[0]}] {i[1]}, {i[2]}, {i[3]}\n'
            return str
        elif key == 'insert_user':
            card_id = request.values.get('card_id')
            password = request.values.get('password')
            student_id = request.values.get('student_id')
            email = request.values.get('email')
            phone = request.values.get('phone')
            description = request.values.get('description')
            if mysql.insert_user(card_id, password, student_id, email, phone, description) is True:
                return 'True'
        elif key == 'show_user':
            result = mysql.get_users()
            print(result)
            str = 'creation_date, card_id, password, student_id, email, phone, description\n'
            for i in result:
                str += f'{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}, {i[5]}, {i[6]}\n'
            return str
        elif key == 'del_user':
            student_id = request.values.get('student_id')
            if mysql.del_users(student_id) is True:
                return 'True'
        return 'False'

@app.route('/stream')
def stream():
    def gen(video):
        while True:
            ret, img = video.read()
            ret, jpeg = cv2.imencode('.jpg', img)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(gen(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

# def job():
#     global gpio_out
#     import gpio
#     gpio.init()
#     gpio_temp = False
#     while True:
#         if gpio_out != gpio_temp:
#             gpio_temp = gpio_out
#             print(gpio_temp)
#             if gpio_temp == True:
#                 gpio.set_relay_on()
#             else:
#                 gpio.set_relay_off()
# threading.Thread(target = job).start()


def job():
    app.run(host = INSIDE_HOST, port = PORT)
threading.Thread(target = job).start()



try:
    gpio_out = False
    mysql.connect()
    gpio.init()
    gpio_temp = False
    while True:
        if gpio_out != gpio_temp:
            gpio_temp = gpio_out
            print(gpio_temp)
            if gpio_temp == True:
                gpio.set_relay_on()
            else:
                gpio.set_relay_off()
finally:
    print('end')
    cap.release()
    mysql.release()
    gpio.cleanup()