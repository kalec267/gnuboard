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

## 접속이 안 될 때

- Docker Desktop이 실행 중인지, Linux containers 모드인지 확인하세요.
- 명령 창에서 설치·빌드가 끝났는지 확인하세요.
- 8080 포트를 다른 프로그램이 사용 중이면 그 프로그램을 종료한 후 다시 실행하세요.
- 첫 실행의 이미지 다운로드가 실패하면 인터넷 연결과 Docker Desktop의 네트워크 설정을 확인하세요.
- 프로젝트가 다른 위치에도 있으면 같은 Docker 프로젝트 이름을 공유하므로 한 위치에서만 실행하세요.

## 포함된 데이터

PC용 ZIP은 소스와 디자인, 샘플 상품 이미지만 포함합니다. 클라우드의 비밀번호·DB 연결 정보·세션·주문 기록은 포함하지 않습니다. PC에서 신규 DB와 샘플 상품 8개를 생성합니다.

상품과 이미지는 샘플이며 실제 결제는 연결되어 있지 않습니다. 무통장 주문은 개발용으로만 확인하고 실제 입금하지 마세요.
