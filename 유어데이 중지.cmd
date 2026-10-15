@echo off
chcp 65001 >nul
cd /d "%~dp0"
docker compose stop
if errorlevel 1 (
    echo Docker Desktop이 실행 중인지 확인해 주세요.
    pause
    exit /b 1
)
echo 유어데이 서버를 중지했습니다. 상품과 주문 데이터는 보존됩니다.
pause
