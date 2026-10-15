"""개발 환경 설치·시작. python3 dev/setup.py [--start] [--port 18080] [--open]"""
from pathlib import Path
import argparse
import os
import subprocess
import sys
import tempfile
from urllib.request import urlopen
import webbrowser

from local_port import parse_port, select_port

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
os.environ.setdefault('BUILDX_CONFIG', str(Path(tempfile.gettempdir()) / 'yourday-buildx'))

def compose(*args, **kwargs):
    return subprocess.run(['docker', 'compose', *args], check=True, **kwargs)

def port_argument(value):
    try:
        return parse_port(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def main():
    parser = argparse.ArgumentParser(description='유어데이 개발 서버 설치·시작')
    parser.add_argument('--start', action='store_true', help='기존 이미지로 시작')
    parser.add_argument('--port', type=port_argument, help='로컬 포트 변경 및 .env에 저장 (예: 18080)')
    parser.add_argument('--open', action='store_true', help='준비 완료 후 PC 브라우저 열기')
    args = parser.parse_args()

    subprocess.run([sys.executable, 'dev/configure.py'], check=True)
    port = select_port(ROOT / '.env', args.port)
    base_url = 'http://127.0.0.1:' + str(port)
    command = ['up', '-d', '--wait', '--wait-timeout', '120']
    if not args.start:
        command.append('--build')
    try:
        compose(*command)
    except subprocess.CalledProcessError:
        raise SystemExit(
            'Docker 실행에 실패했습니다. 위 오류를 확인하세요.\n'
            'Windows 포트 사용 오류라면 py -3 dev/setup.py --port 18080 --open 으로 다시 실행하세요.\n'
            '18080도 사용할 수 없으면 28080처럼 다른 포트를 지정하세요. 기존 DB는 보존됩니다.'
        ) from None
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
    with urlopen(base_url + '/', timeout=15) as response:
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
    print('유어데이 개발 서버 준비 완료: ' + base_url)
    print('관리자 ID: admin. 비밀번호는 로컬 .env에서 확인하세요.')
    if args.open:
        webbrowser.open(base_url)


if __name__ == "__main__":
    main()
