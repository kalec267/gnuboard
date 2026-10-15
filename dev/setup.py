"""개발 환경 설치·시작. python3 dev/setup.py [--start]"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
os.environ.setdefault('BUILDX_CONFIG', str(Path(tempfile.gettempdir()) / 'yourday-buildx'))

def compose(*args, **kwargs):
    return subprocess.run(['docker', 'compose', *args], check=True, **kwargs)

subprocess.run([sys.executable, 'dev/configure.py'], check=True)
command = ['up', '-d', '--wait', '--wait-timeout', '120']
if '--start' not in sys.argv:
    command.append('--build')
compose(*command)
# DB는 컨테이너 볼륨, 업로드·설정은 data/에 보관한다.
# 클라우드 스냅샷에서 Docker 볼륨이 복원되지 않았다면 로컬 백업을 사용한다.
probe = subprocess.run(['docker','compose','exec','-T','db','sh','-c',
    'MYSQL_PWD="$MARIADB_PASSWORD" mariadb -u"$MARIADB_USER" "$MARIADB_DATABASE" -N -e "SHOW TABLES LIKE \'g5_config\'"'],
    check=True, capture_output=True, text=True)
installed = bool(probe.stdout.strip())
config = ROOT / 'data/dbconfig.php'
backup = ROOT / 'data/development-backup.sql'
if config.exists() and not installed:
    if not backup.exists():
        raise SystemExit('DB 볼륨이 비어 있습니다. data/development-backup.sql 또는 별도 DB 백업을 복원하세요. 기존 설정은 보존했습니다.')
    with backup.open('rb') as stream:
        compose('exec','-T','db','sh','-c',
                'MYSQL_PWD="$MARIADB_PASSWORD" exec mariadb -u"$MARIADB_USER" "$MARIADB_DATABASE"', stdin=stream)
    print('개발용 DB 백업을 복원했습니다.')
elif installed and not config.exists():
    raise SystemExit('DB는 이미 설치되어 있지만 data/dbconfig.php가 없습니다. 기존 설정 파일을 복원하세요. 재설치하지 않았습니다.')
compose('exec','-T','--user','1000:1000','web','php','dev/install.php')
compose('exec','-T','--user','1000:1000','web','php','dev/seed.php')
with urlopen('http://127.0.0.1:8080/', timeout=15) as response:
    body = response.read().decode('utf-8')
    if response.status != 200 or 'yd-hero' not in body or 'YOURDAY' not in body:
        raise SystemExit('홈페이지 준비 상태 확인 실패. docker compose logs web을 확인하세요.')
# 인증 정보를 출력하거나 추적 파일에 저장하지 않는다.
temporary = backup.with_suffix('.sql.tmp')
fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
try:
    with os.fdopen(fd, 'wb') as stream:
        compose('exec','-T','db','sh','-c',
                'MYSQL_PWD="$MARIADB_PASSWORD" exec mariadb-dump --lock-tables -u"$MARIADB_USER" "$MARIADB_DATABASE"', stdout=stream)
    temporary.replace(backup)
finally:
    temporary.unlink(missing_ok=True)
print('유어데이 개발 서버 준비 완료: 포트 8080. 관리자 ID: admin. 비밀번호는 로컬 .env에서 확인하세요.')
