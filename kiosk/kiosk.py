import sqlite3

con = sqlite3.connect('/home/dhe/Desktop/kiosk/kioskDB', isolation_level=None)

cur = con.execute('SELECT * FROM students')
pur = con.execute('SELECT * FROM num')
tmp = pur.fetchone()
tmp1 = tmp[0]
tmp2 = tmp[1]
name = ""
uid = ""
borrowed = ""
left = 0
stu_num=0000
dec = 0

"""RFID"""
import serial
import time
import threading

# 시리얼 포트와 아두이노 연결
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # 포트 이름을 적절하게 수정하세요.
time.sleep(2)  # 아두이노가 리셋될 시간을 기다림

# 종료 플래그 설정
exit_flag = False
res = ""
def read_from_serial():
    global exit_flag
    global res
    while not exit_flag:
        if ser.in_waiting > 0:  # 수신된 데이터가 있을 때
            res = ser.readline().decode('utf-8').strip()  # 시리얼로부터 한 줄 읽기
            print("Received:", res)

def user_input():
    global exit_flag
    while not exit_flag:
        user_input = input()
        if user_input.lower() == 'exit':
            exit_flag = True
            print("Exiting...")
            break

# 스레드 시작
print("ready for serial")
res = read_from_serial
serial_thread = threading.Thread(target=read_from_serial)
serial_thread.start()

# 사용자 입력 처리
user_input()

# 시리얼 포트 닫기
ser.close()
serial_thread.join()

print(res, type(res))

cur = con.execute('SELECT * FROM students')

for row in cur:
    if row[2] == res:
        stu_num = row[0]
        name = row[1]
        borrowed = row[3]
        dec = 1
        break
    tmp1+=1
if(dec == 0):
    print("You need new account")
    name = str(input())
    stu_num = int(input())
    cur.execute('INSERT INTO students Values(?, ?, ?, ?);', (stu_num, name, res, "None"))

answer = str(input("borrow or return"))
    
"""tool borrow or return"""
if(answer == "borrow"):
    tool = "Arduino"
    ans = "Yes"

    cur = con.execute('SELECT * FROM tools')
    
    for row in cur:
        if row[0] == tool:
            cur.execute("""
                UPDATE tools
                SET borrow = ?, leave = ?
                WHERE name = ?""", (row[1]+1, row[2]-1, tool))
            cur.execute("""
                UPDATE students
                SET  borrowed = ?
                WHERE name = ?""", (borrowed+" "+tool, name))
        tmp2 += 1    
    tmp2 = tmp[1]
    
elif(answer == "return" and borrowed != 0):
    tool = " Arduino"

    cur = con.execute('SELECT * FROM tools')
    
    for row in cur:
        if row[0] == tool:
            cur.execute("""
                UPDATE tools
                SET borrow = ?, leave = ?
                WHERE name = ?""", (row[1]-1, row[2]+1, tool))
            for word in borrowed.strip(" "):
                
            cur.execute("""
                UPDATE students
                SET , borrowed = ?
                WHERE name = ?""", (borrowed[], name))
        tmp2 += 1    
    tmp2 = tmp[1]

else:
    print("Errno 4 : No exist module or No borrowed")