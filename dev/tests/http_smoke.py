"""실제 개발 서버의 주요 경로와 비공개 파일 접근을 검증한다."""
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from html.parser import HTMLParser
import os
BASE = os.environ.get('YOURDAY_BASE_URL', 'http://127.0.0.1:8080').rstrip('/')


class LocalLinks(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name not in ('href', 'src', 'action') or not value:
                continue
            url = urlsplit(value)
            if url.hostname in ('localhost', '127.0.0.1'):
                assert url.port == urlsplit(BASE).port, ('내부 링크 포트 불일치', value)


checks = [('/', 'YOURDAY'), ('/shop/', '오늘의 유어데이'),
          ('/shop/list.php?ca_id=10', '내추럴 싱글 블레이저'),
          ('/shop/listtype.php?type=3', '소프트 라운드 니트'),
          ('/shop/search.php?q='+quote('니트'), '소프트 라운드 니트'),
          ('/shop/search.php?q=zzzzunmatched', '없습니다'),
          ('/shop/item.php?it_id=YD1001', 'it_option_1'),
          ('/shop/cart.php', '장바구니'),
          ('/bbs/login.php', '로그인'),
          ('/bbs/board.php?bo_table=notice', '유어데이에 오신 것을 환영합니다'),
          ('/bbs/faq.php', '교환·반품은 어떻게 하나요?'), ('/bbs/content.php?co_id=company', '당신의 하루를 입다'),
          ('/bbs/content.php?co_id=privacy', '개발용 초안')]
for path, expected in checks:
    with urlopen(BASE+path, timeout=15) as response:
        content = response.read().decode('utf-8')
        assert response.status == 200, (path,response.status)
        assert expected in content, (path,expected)
        assert 'Fatal error:' not in content and 'Warning:' not in content, path
        LocalLinks().feed(content)
for path in ('/.env','/.git/config','/compose.yaml','/dev/install.php','/install/install_db.php','/data/dbconfig.php','/data/development-backup.sql','/data/session/'):
    try:
        urlopen(BASE+path, timeout=15)
        raise AssertionError('비공개 경로에 접근 가능: '+path)
    except HTTPError as error:
        assert error.code in (403,404), (path,error.code)
print(f'PASS: 주요 경로 {len(checks)}개, 비공개 경로 9개')
