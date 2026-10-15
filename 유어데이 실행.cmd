@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 유어데이 개발 서버를 준비합니다. Docker Desktop을 먼저 실행해 주세요.
where docker >nul 2>&1
if errorlevel 1 (
    echo Docker Desktop을 설치하고 실행한 후 다시 시도해 주세요.
    pause
    exit /b 1
)
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker Desktop이 아직 준비되지 않았습니다. Engine running 상태를 확인해 주세요.
    pause
    exit /b 1
)
py -3 --version >nul 2>&1
if not errorlevel 1 (
    py -3 dev\setup.py --open
    goto result
)
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.10 이상을 설치해 주세요. 설치할 때 Add python.exe to PATH를 선택해 주세요.
    pause
    exit /b 1
)
python dev\setup.py --open
:result
if errorlevel 1 (
    echo 실행에 실패했습니다. 위 오류 내용을 확인해 주세요.
    pause
    exit /b 1
)
echo 실행을 완료했습니다. 접속 주소는 위 완료 메시지를 확인하세요.
pause
