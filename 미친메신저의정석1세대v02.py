#집가고싶다 inc. 미친메신저의정석 클라이언트 (1세대)
#특정 인물들만 이해할수 있는 미친 메신저

import socket
import threading
import sys
import time

version="AM102"

while True:
    decision=input("\n[1] 메인 서버로 접속\n[2] 외부 서버로 접속\n> ")
    if decision=="1":
        HOST="messenger.iwanttogohome.net"
        break
    elif decision=="2":
        HOST=input("\n접속할 서버의 주소를 입력하세요.\n> ")
        break
    else:
        print("\n잘못된 값을 입력했습니다.\n 다시 입력하세요.")

while True:
    decision = input("\n[1] 메인 서버포트로 접속\n[2] 개발 서버포트로 접속(서버가 열려있지 않을수도 있음)\n[3] 외부 서버포트로 접속\n> ")
    if decision == "1":
        PORT = 887
        break
    elif decision == "2":
        PORT = 888
        break
    elif decision == "3":
        while True:
            try:
                PORT = int(input("\n접속할 서버의 포트를 입력하세요.\n> "))
                break
            except:
                print("\n값을 정수형으로 입력해주세요.")
        break
    else:
        print("\n잘못된 값을 입력했습니다.\n다시 입력하세요.")

name=input("\n이름을 입력하세요.\n> ")

def receive():
    while True:
        rcvdMsg=clientSocket.recv(1024).decode()
        if rcvdMsg == "name?":
            clientSocket.sendall(name.encode())
        elif rcvdMsg == "info?":
            clientSocket.sendall(version.encode())
        else:
            if not rcvdMsg:
                print("\n\n서버가 닫혔거나 네트워크에 문제가 있는 것 같습니다.", file=sys.stderr)
                time.sleep(1)
                sys.exit(1)
            print(f"\r{rcvdMsg}", end="")

receiving=threading.Thread(target=receive)

clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((HOST, PORT))
except Exception as e:
    print(f"\n서버가 열려있지 않은것 같습니다.\n오류 로그 : {e}\n", file=sys.stderr)
    time.sleep(1)
    sys.exit(1)

receiving.start()

print(f"\n집가고싶다 inc.\n미친메신저의정석 (1세대) ({version})\n\n서버주소 : {HOST}\n서버포트 : {PORT}\n이 클라이언트의 이름 : {name}\n\n", end="")

while True:
    message=input()
    clientSocket.sendall(message.encode())
