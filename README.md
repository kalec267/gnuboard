# 유어데이 · YOURDAY

그누보드5 **5.6.43**와 영카트를 기반으로 만든 차분한 분위기의 의류 쇼핑몰입니다. 아이보리·웜그레이·세이지 톤의 반응형 테마, 브랜드 화보, 상품 탐색과 영카트의 구매·관리 기능을 연결했습니다.

## Windows에서 실행

Docker Desktop과 Python 3.10 이상을 설치한 뒤 `유어데이 실행.cmd`를 더블클릭하세요. 자세한 절차는 [Windows에서 시작하기](Windows에서%20시작하기.md)를 참고하세요.

## 실행

Docker Engine과 Docker Compose v2, Python 3이 필요합니다. 이 클라우드 작업에서는 `/workspace/gnuboard` 체크아웃을 사용합니다. 새 Git worktree는 만들지 않습니다.

```bash
cd /workspace/gnuboard
python3 dev/setup.py
```

처음 실행하면 PHP 8.3/Apache 이미지와 MariaDB 11.4를 준비하고 신규 DB에 그누보드·영카트를 설치합니다. 이미 설치한 환경의 설정과 상품은 보존합니다. 기본 서비스 포트는 **8080**이며 개발 서버는 로컬 인터페이스에만 바인딩됩니다. 외부 공개 배포는 수행하지 않습니다.

```bash
python3 dev/setup.py --start  # 준비된 이미지로 다시 시작
python3 dev/setup.py --port 18080 --open  # Windows 포트 제한 우회 및 브라우저 열기
docker compose stop         # 서비스 중지 (DB 보존)
```

포트를 변경하면 `.env`의 `SHOP_PORT`에 저장되고 서버·내부 링크·다음 실행에도 적용됩니다. 기존 비밀번호와 DB는 유지합니다.

- 메인: `/`
- 상품: `/shop/search.php`, `/shop/list.php?ca_id=10`
- 장바구니: `/shop/cart.php`
- 주문 조회: `/shop/orderinquiry.php`
- 공지사항: `/bbs/board.php?bo_table=notice`
- 관리자: `/adm/` (ID `admin`)

관리자 비밀번호는 기본 로그인 폼의 길이 제한에 맞춰 첫 실행 때 20자로 임의 생성되며 **Git에서 제외한 로컬 `.env`의 `SHOP_ADMIN_PASSWORD`**에 보관합니다. 채팅이나 커밋에 비밀번호를 붙이지 마세요. `.env` 변경만으로 기존 DB의 관리자 비밀번호가 바뀌지는 않습니다. 로그인한 뒤 회원 관리에서 변경할 수 있습니다.

## 기능

- 유어데이 전용 PC·모바일 홈, 의류 카테고리 필터, 검색, 신상품·인기상품 목록
- 5개 카테고리, 8개 샘플 상품, 의류 사이즈 S/M/L과 옵션별 재고
- 상품 상세·수량·장바구니·주문서·무통장 개발용 주문
- 영카트 회원가입·로그인·마이페이지·위시리스트·주문 조회와 관리자 기능
- 브랜드 소개, 공지사항, FAQ, 1:1 문의

현재 상품·가격·소재·사이즈·배송 정책은 **샘플**입니다. 상품 이미지는 자체 일러스트, 메인 화보는 AI 생성 이미지입니다. 실제 상품 사진과 정확한 상품 정보로 교체해야 합니다. 포인트와 발신 메일은 개발 환경에서 꺼져 있습니다.

## 파일과 데이터

- `theme/yourday/`: 사용자 정의 테마. 영카트 결제·주문 코어와 분리했습니다.
- `dev/`: Docker 환경, CLI 전용 설치·샘플 초기화·기능 검사
- `data/`: DB 연결 설정·업로드·세션·개발용 DB 백업 (Git 제외)
- Docker `database` 볼륨: MariaDB 데이터. `docker compose down -v`는 DB를 삭제하므로 사용하지 마세요.

`dev/setup.py`는 정상 시작 후 `data/development-backup.sql`을 갱신합니다. 클라우드 재시작에서 볼륨이 누락되면 이 백업으로 복원합니다. 운영 백업 정책을 대신하지 않습니다. `.env`, `data/`와 DB 볼륨은 함께 보존하세요. DB가 남아 있는데 연결 설정이 없거나, 연결 설정은 있지만 복원할 DB가 없으면 재설치하지 않고 중단합니다.

## 검증

실행 중인 개발 서버에 Chromium과 Python Playwright로 검사합니다.

```bash
python3 dev/tests/browser.py
python3 dev/tests/browser.py --place-order  # 실제 결제 없이 자동검증용 샘플 주문 저장
python3 dev/tests/http_smoke.py
python3 -m unittest discover -s dev/tests -p "test_local_port.py"
```

홈·카테고리 필터·검색·상품 이미지·사이즈·장바구니·주문서·모바일 레이아웃을 실제 PHP/MariaDB에서 확인합니다. 다른 포트에서 검사하려면 `YOURDAY_BASE_URL`을 해당 주소로 설정하세요. 테스트용 주문을 생성하는 경우 명확히 표시하며 실제 PG를 호출하지 않습니다. 브라우저 검사에는 `/usr/bin/chromium`이 필요하고 `CHROMIUM_PATH`로 경로를 변경할 수 있습니다. 결과 화면은 `/tmp/yourday-*.png`에 저장합니다.

## 실제 판매 전 필요한 설정

관리자에서 사업자·통신판매업·연락처, 실제 상품과 재고, 배송·교환·반품 조건, 이용약관·개인정보처리방침을 등록하세요. 실제 결제에는 PG 계약과 발급된 상점 정보, HTTPS 도메인 및 결제사 테스트가 필요합니다. 현재 무통장 계좌는 **입금 금지를 안내하는 개발용 문구**이며 실제 계좌가 아닙니다. 이메일과 주소 검색 등 외부 서비스의 연결도 운영 환경에서 확인해야 합니다.

공개 배포는 별도 웹 서버·HTTPS·DB 백업·접근 제어를 갖춘 환경에서 진행하세요. `dev/apache.conf`는 설치 경로, 개발 도구, 숨김 파일, SQL 및 data 하위 실행 파일의 HTTP 접근을 차단합니다.

## 원본과 라이선스

공식 소스: https://github.com/gnuboard/gnuboard5

도입 커밋: `f8059c231a9377b69bc594f42836463c27fa9df6` (5.6.43). 그누보드·영카트의 라이선스와 고지를 `LICENSE.txt` 및 각 구성요소에 보존했습니다. 원본 설치 안내는 `docs/gnuboard-upstream.md`를 참고하세요.
