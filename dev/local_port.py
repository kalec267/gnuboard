"""개발 서버의 공개 포트를 선택하고 다른 로컬 설정은 보존한다."""
import os
from pathlib import Path
import re
import tempfile


def parse_port(value):
    text = str(value)
    if not re.fullmatch(r'[0-9]{1,5}', text) or not 1024 <= int(text) <= 65535:
        raise ValueError('포트는 1024~65535 사이의 숫자로 지정하세요.')
    return int(text)


def select_port(env_path: Path, requested=None):
    content = env_path.read_text(encoding='utf-8')
    pattern = re.compile(r'^\s*(?:export\s+)?SHOP_PORT\s*=.*$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    saved = '8080'
    if matches:
        saved = matches[-1].group().split('=', 1)[1].strip()
        saved = saved.split(' #', 1)[0].strip().strip('\"\'')
    value = requested if requested is not None else os.environ.get('SHOP_PORT', saved)
    port = parse_port(value)
    if requested is not None:
        # 비밀번호를 재생성하지 않고 이 설정 한 줄만 갱신한다.
        line = 'SHOP_PORT=' + str(port)
        if matches:
            updated = pattern.sub(line, content)
        else:
            updated = content + ('' if not content or content.endswith('\n') else '\n') + line + '\n'
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='',
                                             dir=env_path.parent, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(updated)
            temporary.replace(env_path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    # Compose와 설치·시작 프로세스가 모두 같은 값을 사용한다.
    os.environ['SHOP_PORT'] = str(port)
    return port
