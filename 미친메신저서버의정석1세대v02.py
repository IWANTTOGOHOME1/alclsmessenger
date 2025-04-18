#집가고싶다 inc. 미친메신저서버의정석 (1세대)
#특정 인물들만 이해할수 있는 미친 메신저 의 서버
#미친메신저의정석 1세대 버전0.2 에 추가된 신기능 : 클라이언트 정보확인기능, 커맨드 시스템 삭제, 

import socket
import threading
import datetime
import time

HOST="0.0.0.0"
PORT=888

clients=[]
ip="211.195.116.187"
maxUser=10
version = "AMS102" #미친메신저서버의정석 1세대 v0.2
availableClientVersion = ["AM102", "COS202"]

def check(item, clientSocketCH):
    if item == "INFO":
        send(clientSocketCH, "info?")
        rcvdMsg = clientSocketCH.recv(1024).decode()
        return rcvdMsg
    elif item == "NAME":
        send(clientSocketCH, "name?")
        rcvdMsg = clientSocketCH.recv(1024).decode()
        return rcvdMsg

def send(clientSocketS, messageS):
    try:
        clientSocketS.sendall(messageS.encode())
        log("SERVER", f": \"{messageS}\"")
    except Exception as e:
        log("SYSTEM", e)

def everyone(messageE):
    for clientE in clients:
        try:
            clientE.sendall(messageE.encode())
        except Exception as e:
            log("SYSTEM", e)        
    log("SERVER", f": \"{messageE}\"")

def log(adrL, messageL):
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\r[{timestamp}] ({adrL}) {messageL}")
    with open("log.txt", "a", encoding="utf-8") as logFile:
        logFile.write(f"[{timestamp}] ({adrL}) {messageL}\n")

def communication(clientSocketC, adrC):
    log(adrC, "서버에 접속했습니다.")
    available=False
    cName = check("NAME", clientSocketC)
    cInfo = check("INFO", clientSocketC)
    for v in availableClientVersion:
        if cInfo == v:
            available=True
    if available == True:
        log(adrC, f"서버의 인증과정을 통과하였습니다. (이름 : {cName}, 클라이언트정보 : {cInfo})")
        clients.append(clientSocketC)
        everyone(f"{cName}님이 서버에 접속했습니다.\n>>> ")

        while True:
            try:
                rcvdMsg=clientSocketC.recv(1024).decode()
                if not rcvdMsg:
                    break
                log(adrC, f": \"{rcvdMsg}\"")

                everyone(f"[{cName}] : {rcvdMsg}\n>>> ")
            except Exception as e:
                log("SYSTEM", e)
                break
    
        log(adrC, "서버와 연결이 끊겼습니다.")
        everyone(f"{cName}님이 서버와 연결이 끊겼습니다.\n>>> ")
        clients.remove(clientSocketC)
        clientSocketC.close()
    else:
        send(clientSocketC, "\n지원되지 않는 클라이언트 같습니다.\nhttps://www.iwanttogohome.net/ 에서 최신 클라이언트를 다운로드하세요.\n\n3초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocketC, "2초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocketC, "1초후에 연결을 끊습니다.")
        time.sleep(1)
        log(adrC, "서버의 인증과정을 실패하여 연결을 끊었습니다.")
        clientSocketC.close()

serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(maxUser)

print(f"\n집가고싶다 inc.\n미친메신저서버의정석 (1세대) ({version})\n\n서버주소 : {ip}\n서버포트 : {PORT}\n서버 최대 인원 : {maxUser}\n\n", end="")
timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("log.txt", "a", encoding="utf-8") as logFile:
    logFile.write(f"[{timestamp}] (SYSTEM) {ip}:{PORT}에서 서버를 시작했습니다.\n")

while True:
    clientSocket, adr=serverSocket.accept()
    communicationing=threading.Thread(target=communication, args=(clientSocket, adr))
    communicationing.start()
