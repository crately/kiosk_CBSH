import serial
import time
import threading

# 시리얼 포트와 아두이노 연결
ser = serial.Serial('COM9', 9600, timeout=1)  # 포트 이름을 적절하게 수정하세요.
time.sleep(2)  # 아두이노가 리셋될 시간을 기다림

# 종료 플래그 설정
exit_flag = False

def read_from_serial():
    global exit_flag
    while not exit_flag:
        if ser.in_waiting > 0:  # 수신된 데이터가 있을 때
            line = ser.readline().decode('utf-8').strip()  # 시리얼로부터 한 줄 읽기
            print("Received:", line)

def user_input():
    global exit_flag
    while not exit_flag:
        user_input = input()
        if user_input.lower() == 'exit':
            exit_flag = True
            print("Exiting...")
            break

# 스레드 시작
serial_thread = threading.Thread(target=read_from_serial)
serial_thread.start()

# 사용자 입력 처리
user_input()

# 시리얼 포트 닫기
ser.close()
serial_thread.join()