#tcp를 이용한, 동시성 있는 유니코드 변환 서버
#실행시 콘솔에서 이 파일을 실행새 서버 구동 후, 다른 콘솔에서 telnet localhost 2323에 접속해 클라이언트로서 접근
#!/usr/bin/env python3

# BEGIN TCP_CHARFINDER_TOP
import sys
import asyncio

from charfinder import UnicodeNameIndex  # <1>

CRLF = b'\r\n' #캐리지리턴
PROMPT = b'?> '

index = UnicodeNameIndex()  # <2>

async def handle_queries(reader, writer):  # <3> 인수는 asyncio.StreamReader와 asyncio.StreamWriter 객체
    while True:  # <4>
        writer.write(PROMPT)  # can't await!  # 해당 메서드는 코루틴이 아니다.
        await writer.drain()  # must await!  # 출력 버퍼 플러시. 해당 메서드는 코루틴이다.
        data = await reader.readline()  # bytes형이 반환된다.
        try:
            query = data.decode().strip() #바이트형을 unicode로 변환하고 앞뒤 공백을 제거(strip 인수 없을 시 공백제거)한다.
        except UnicodeDecodeError:  # 텔넷 클라이언트가 제어문자(U+0032 이전)를 보내면 해당 예외를 던지도록 되어 있다. 이를 처리한다. 편의상 None으로 둔다(25줄 참고)
            query = '\x00' #Null(편의를 위해)
        client = writer.get_extra_info('peername')  # 소켓이 연결된 원격 주소 반환
        print('Received from {}: {!r}'.format(client, query))  # <10>
        if query: #None이면 안 돈다
            if ord(query[:1]) < 32:  # 제어문자문자면 break
                break
            lines = list(index.find_description_strs(query)) # 유니코드포인트\t실제문자\t문자명 포맷의 스트링 이터레이터를 통으로 리스트로 변환해 받는다(편의상) #<-여기서 charfinder와 연결된다.
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines) # byte형 변환 후(기본으로 utf8을 쓴다) 캐리지리턴+라인피드를 추가해 전송
            writer.write(index.status(query, len(lines)).encode() + CRLF) # 상태 메시지 전송

            await writer.drain()  # 출력 버퍼 플러시.
            print('Sent {} results'.format(len(lines)))  # <16>

    print('Close the client socket')  # <17>
    writer.close()  # <18>
# END TCP_CHARFINDER_TOP

# BEGIN TCP_CHARFINDER_MAIN
def main(address='127.0.0.1', port=2323):  # <1>
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, address, port, loop=loop) 
    #start_server()의 첫 인자는 서버용 처리 코루틴. 반환값은 바로 사용가능한 서버를 제공하는 코루틴(어웨이터블)이다. 아래줄처럼 구동한다.(asyncio Stream API 참고)
    server = loop.run_until_complete(server_coro) # 서버 구동. 해당 반환값은 asyncio.Seerver 객체이다.

    host = server.sockets[0].getsockname()  # <4>
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # <5>
    try:
        loop.run_forever()  # <6> #<-실행시 여기서 블로킹되어 기다리게 된다.
    except KeyboardInterrupt:  # CTRL+C pressed
        pass

    print('Server shutting down.')
    server.close()  # <7>
    loop.run_until_complete(server.wait_closed())  # server.sait_close()는 닫히길 기다리는 퓨처 객체가 반환된다. 이를 run_until_complete로 돌려 닫힐때까지 기다리자.
    loop.close()  # <9>


if __name__ == '__main__':
    main(*sys.argv[1:])  # <10>
# END TCP_CHARFINDER_MAIN