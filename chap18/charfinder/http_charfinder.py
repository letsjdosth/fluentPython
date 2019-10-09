#!/usr/bin/env python3
#참고: 실제로 안 돌아감. aiohttp가 버전이 올라가며 Requests 클래스 구성이 달라진 듯(54번째 줄 문제)

import sys
import asyncio
from aiohttp import web

from charfinder import UnicodeNameIndex

TEMPLATE_NAME = 'http_charfinder.html'
CONTENT_TYPE = 'text/html; charset=UTF-8'
SAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit'
                ' Roman face Ethiopic black mark symbol dot'
                ' operator Braille hexagram').split()

ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'
LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in
                       sorted(SAMPLE_WORDS, key=str.upper))


index = UnicodeNameIndex()
with open(TEMPLATE_NAME) as tpl:
    template = tpl.read()
template = template.replace('{links}', LINKS_HTML) #<-tamplate 사용법.. 이렇다..

# BEGIN HTTP_CHARFINDER_HOME

async def home(request):  # <1> 인수로는 aiohttp.web.Request 객체를 받게 된다. #<-처리기는 코루틴이 아니어도 괜찮다(aiohttp가 알아서 코루틴으로 변환한다고 함)
    query = request.GET.get['query'].strip() # <2> #<-기존 코드는 문제가 있음. request에 GET이 없다고 함. (뜯어고치려면 init/main의 코드를 새로운 방식의 라우팅에 적합하도록 뜯어고쳐야 할 듯 함)
    print('Query: {!r}'.format(query))  # <3>
    if query:  # <4>
        descriptions = list(index.find_descriptions(query)) #<-여기서 charfinder.py와 연결된다.
        res = '\n'.join(ROW_TPL.format(**descr._asdict())
                        for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'

    html = template.format(query=query, result=res,  # <5> <-tamplate 사용법2. html 코드를 스트링으로 읽어놨으므로 스트링의 방식으로 처리하면 된다.
                           message=msg)
    print('Sending {} results'.format(len(descriptions)))  # <6>
    return web.Response(content_type=CONTENT_TYPE, text=html) # <7>
# END HTTP_CHARFINDER_HOME


# BEGIN HTTP_CHARFINDER_SETUP
async def init(loop, address, port):  # <1> 이벤트 루트가 구동시킬 서버 생성
    app = web.Application(loop=loop)  # <2>
    app.router.add_route('GET','/', home)  # <3> GET /(root) 요청은 home 함수가 처리하도록
    handler = app.make_handler()  # <4> 설정 라우트에 따라 http 요청을 처리하는 핸들러(aiohttp.web.RequestHandler 객체)를 반환한다.
    server = await loop.create_server(handler, address, port)  # <5> 핸들러, 주소, 포트가 바인딩된 asyncio.Server 객체를 반환한다.
    return server.sockets[0].getsockname()  # <6>

def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))  # <7> init 자체가 코루틴이므로, 이러한 방식으로 실행한다.
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()  # <8>
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
    print('Server shutting down.')
    loop.close()  # <9>


if __name__ == '__main__':
    main(*sys.argv[1:])
# END HTTP_CHARFINDER_SETUP