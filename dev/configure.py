"""로컬 개발 전용 비밀번호를 생성한다. 기존 .env는 보존한다."""
from pathlib import Path
import secrets
import os
root = Path(__file__).resolve().parent.parent
path = root / '.env'
if path.exists():
    print('기존 .env를 사용합니다.')
else:
    names = ('DB_ROOT_PASSWORD', 'DB_PASSWORD', 'SHOP_ADMIN_PASSWORD')
    content = ''.join(
        '{}={}\n'.format(name, secrets.token_hex(10 if name == 'SHOP_ADMIN_PASSWORD' else 24))
        for name in names
    )
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write(content)
    print('.env에 로컬 개발용 비밀번호를 생성했습니다. 관리자 ID: admin')
(root / 'data').mkdir(exist_ok=True, mode=0o700)
