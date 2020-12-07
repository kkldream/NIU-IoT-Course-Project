import pymysql
import threading
import time
db_settings = {
    "host": "120.101.8.240",
    "port": 3308,
    "user": "kk",
    "password": "12332162",
    "db": "3d_printing"
}
conn = None
over = False

def connect():
    global conn
    conn = pymysql.connect(**db_settings)
    start_time = time.time()
    def job():
        while not over:
            print(f'Time: {int(time.time() - start_time)}, Status: {get_latest_status()}')
            time.sleep(3600)
    threading.Thread(target = job).start()

def release():
    global over
    over = True

def login_verification(student_id, password):
    try:
        with conn.cursor() as cursor:
            command = f'SELECT * FROM users WHERE student_id="{student_id}"'
            cursor.execute(command)
            result = cursor.fetchall()
            for i in result:
                if i[2] == password:
                    return True
            return False
    except Exception as ex:
        # print(ex)
        return False

def get_latest_status(num = 1):
    try:
        with conn.cursor() as cursor:
            # command = 'SELECT * FROM `status` ORDER BY `creation_date` DESC LIMIT 1'
            command = f'SELECT * FROM `status` WHERE `status` = "boot" OR `status` = "shutdown" ORDER BY `creation_date` DESC LIMIT {num}'
            cursor.execute(command)
            result = cursor.fetchall()
            if num == 1:
                return result[0]
            else:
                return result
    except Exception as ex:
        print(ex)
        return False

def insert_status(student_id, status):
    try:
        with conn.cursor() as cursor:
            command = f'SELECT * FROM users WHERE student_id="{student_id}"'
            cursor.execute(command)
            result = cursor.fetchall()
            if len(result) == 0:
                result = 'Not registered'
            else:
                result = result[0][1]
            command = f"INSERT INTO `status` (`creation_date`, `student_id`, `card_id`, `status`) VALUES (CURRENT_TIMESTAMP, '{student_id}', '{result}', '{status}');"
            cursor.execute(command)
            conn.commit()
            return True
    except Exception as ex:
        print(ex)
        return False

def insert_user(card_id, password, student_id, email = '', phone = '', description = ''):
    try:
        with conn.cursor() as cursor:
            command = f"INSERT INTO `users` (`creation_date`, `card_id`, `password`, `student_id`, `email`, `phone`, `description`) VALUES (CURRENT_TIMESTAMP, '{card_id}', '{password}', '{student_id}', '{email}', '{phone}', '{description}')"
            cursor.execute(command)
            conn.commit()
            return True
    except Exception as ex:
        print(ex)
        return False

def get_users():
    try:
        with conn.cursor() as cursor:
            command = 'SELECT * FROM `users` ORDER BY `creation_date` DESC'
            cursor.execute(command)
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print(ex)
        return False
        
def del_users(student_id):
    try:
        with conn.cursor() as cursor:
            command = f'DELETE FROM `users` WHERE `student_id` = "{student_id}"'
            cursor.execute(command)
            conn.commit()
            return True
    except Exception as ex:
        print(ex)
        return False



if __name__ == "__main__":
    release()
    connect()
    print(del_users('3'))
    # insert_status('B0742033','boot')