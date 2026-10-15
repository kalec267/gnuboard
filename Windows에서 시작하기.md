# Windows에서 유어데이 실행하기

## 1. 준비 프로그램 설치

1. Docker Desktop for Windows: https://www.docker.com/products/docker-desktop/
   - 설치 안내에 따라 WSL 2를 활성화하고 필요하면 Windows를 재시작하세요.
   - Docker Desktop을 열고 Linux containers 모드에서 엔진 실행이 완료될 때까지 기다리세요.
2. Python 3.10 이상: https://www.python.org/downloads/windows/
   - 설치할 때 **Add python.exe to PATH**를 선택하세요.
   - Windows 10/11의 WSL 2 및 Docker Desktop 지원 사양이 필요합니다.

## 2. ZIP 압축 풀기

다운로드한 ZIP을 **모두 압축 풀기**로 해제하세요. 경로는 `C:\yourday-local`처럼 짧고 간단하게 지정하는 것이 좋습니다. ZIP 안에서 바로 실행하지 마세요.

파일 탐색기에 확장자가 숨겨져 있으면 **보기 → 표시 → 파일 확장명**을 켜세요.

## 3. 실행

압축을 푼 `yourday` 폴더에서 **유어데이 실행.cmd**를 더블클릭하세요.

첫 실행에는 인터넷 연결이 필요하며 Docker 이미지 다운로드와 PHP 확장 빌드 때문에 몇 분 이상 걸릴 수 있습니다. 창을 닫지 말고 완료될 때까지 기다리세요. 준비가 끝나면 브라우저가 열립니다.

- 쇼핑몰: 브라우저 주소창에 `http://localhost:8080`
- 관리자: `http://localhost:8080/adm/`
- 관리자 ID: `admin`
- 관리자 비밀번호: 같은 폴더의 `.env`를 메모장으로 열어 `SHOP_ADMIN_PASSWORD=` 오른쪽 문자열 확인

비밀번호는 PC 첫 실행 때 새로 생성합니다. `.env` 내용을 채팅이나 공개 저장소에 공유하지 마세요. `.env`를 편집하는 것만으로 기존 관리자 비밀번호가 바뀌지는 않습니다.

창이 바로 닫히면 해당 폴더에서 PowerShell을 열어 다음 명령을 실행하면 오류를 확인할 수 있습니다.

```powershell
py -3 dev/setup.py
```

Python 버전은 `py -3 --version`으로 확인할 수 있습니다.

## 4. 종료와 재실행

**유어데이 중지.cmd**를 더블클릭하면 서버만 중지됩니다. 다시 실행하려면 Docker Desktop을 실행한 뒤 **유어데이 실행.cmd**를 더블클릭하세요.

`.env`, `data` 폴더, Docker의 `yourday-shop` 데이터 볼륨을 유지하세요. Docker Desktop에서 볼륨을 삭제하거나 `docker compose down -v`를 실행하면 DB를 잃을 수 있습니다.

## 8080 포트 사용 오류가 날 때

`ports are not available`, `bind`, `forbidden by its access permissions`가 표시되면 Windows에서 해당 포트를 사용할 수 없는 상태입니다. 다른 프로그램의 점유 또는 Windows 예약 포트 범위 등이 원인일 수 있습니다. 관리자 권한이나 DB 재설치 없이 다른 포트로 실행하세요.

`yourday` 폴더의 빈 공간에서 마우스 오른쪽 버튼을 눌러 터미널 또는 PowerShell을 연 뒤 실행하세요.

```powershell
py -3 dev/setup.py --port 18080 --open
```

준비가 끝나면 `http://127.0.0.1:18080`이 열립니다. `--port` 값은 기존 `.env`의 비밀번호를 보존하면서 `SHOP_PORT`로 저장하므로 이후에는 실행 CMD를 더블클릭하면 됩니다. 18080도 사용할 수 없으면 28080처럼 다른 포트를 지정하세요.

포트 변경은 Docker 바인딩, Apache 내부 포트, 상품·로그인 링크, 준비 상태 검사, 브라우저 열기에 함께 적용됩니다. `compose.yaml`의 외부 포트만 바꾸면 내부 링크가 8080으로 돌아갈 수 있으므로 위 명령을 사용하세요.

`.env`, `data`와 DB 볼륨은 지우지 마세요. 이미 설치되었다면 기존 계정·상품·주문을 보존하고, 첫 설치가 미완료라면 이어서 설치합니다.

## 컨테이너는 정상인데 DB 상태 확인에 실패할 때

같은 프로젝트 폴더에서 다음 명령으로 실제 DB 오류를 확인하세요. 이 명령은 테이블을 설치하거나 DB를 복원하지 않습니다.

```powershell
py -3 dev/setup.py --start --port 8097 --check-db
```

`ERROR 1045 ... Access denied`가 나타나면 DB 볼륨의 계정 비밀번호와 현재 `.env`가 일치하는지 확인하세요. MariaDB의 초기 비밀번호는 DB 볼륨을 처음 만들 때만 적용됩니다. `.env`를 다시 만들거나 폴더를 새로 다운로드해도 기존 볼륨의 비밀번호는 바뀌지 않습니다. 컨테이너의 `Healthy` 표시는 앱 계정으로 접속할 수 있다는 의미가 아닙니다.

프로젝트 경로를 옮겼다면 이전 폴더에서 실행하거나 이전 `.env`와 `data`를 함께 보존해 새 폴더로 옮기세요. `.env`의 내용을 채팅에 붙이지 마세요. 기존 데이터가 남아 있는지 확인하기 전에는 볼륨 삭제나 DB 초기화를 하지 마세요.

여러 폴더에서 같은 `yourday-shop` 컨테이너·볼륨 이름을 공유하므로 한 폴더에서만 실행해야 합니다. 위 조치 후에도 실패하면 비밀번호를 제외한 `ERROR ...` 줄을 알려주세요.

### 이전 폴더의 .env로 접속 정보 복구

이전 `.env`로 DB 접속이 되던 환경에서는 그 파일을 유지해야 합니다. 아래 두 경로를 실제 이전·현재 프로젝트 폴더로 바꿔 실행하세요. 현재 `.env`는 Git에서 제외된 `data` 아래에 먼저 백업하며 DB 볼륨은 삭제하지 않습니다.

```powershell
& {
    $ErrorActionPreference = "Stop"
    $old = "C:\yourday-old"
    $new = "C:\yourday-local\yourday"
    if (!(Test-Path "$old\.env" -PathType Leaf)) {
        throw "이전 .env 파일 경로를 확인하세요."
    }
    if (!(Test-Path "$new\dev\configure.py" -PathType Leaf)) {
        throw "전체 프로젝트 폴더 경로를 확인하세요."
    }
    New-Item -ItemType Directory -Path "$new\data" -Force | Out-Null
    if (Test-Path "$new\.env" -PathType Leaf) {
        Copy-Item "$new\.env" "$new\data\.env-backup-$(Get-Date -Format yyyyMMddHHmmss)"
    }
    Copy-Item "$old\.env" "$new\.env" -Force
    py -3 "$new\dev\setup.py" --start --port 8097 --open
}
```

이전 폴더에서 설치를 완료했다면 `data/dbconfig.php`와 업로드 파일 등 기존 `data`도 함께 보존해야 합니다. DB가 이미 설치되었는데 설정 파일이 없다는 메시지가 나오면 이전 `data`를 복원하세요. 브라우저에 `data/dbconfig.php`가 없다는 안내만 나타날 때는 PowerShell 설치 명령의 마지막 오류부터 확인하세요.

수정 파일 ZIP은 전체 프로젝트에 덮어써야 합니다. `yourday-db-fix`처럼 수정 파일만 있는 폴더에서는 서버를 실행할 수 없습니다.

## 그 밖에 접속이 안 될 때

- Docker Desktop이 실행 중인지, Linux containers 모드인지 확인하세요.
- 명령 창에서 설치·빌드가 끝났는지 확인하세요.
- 첫 실행의 이미지 다운로드가 실패하면 인터넷 연결과 Docker Desktop의 네트워크 설정을 확인하세요.
- 프로젝트가 다른 위치에도 있으면 같은 Docker 프로젝트 이름을 공유하므로 한 위치에서만 실행하세요.

## 포함된 데이터

PC용 ZIP은 소스와 디자인, 샘플 상품 이미지만 포함합니다. 클라우드의 비밀번호·DB 연결 정보·세션·주문 기록은 포함하지 않습니다. PC에서 신규 DB와 샘플 상품 8개를 생성합니다.

상품과 이미지는 샘플이며 실제 결제는 연결되어 있지 않습니다. 무통장 주문은 개발용으로만 확인하고 실제 입금하지 마세요.
