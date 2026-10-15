"""실제 PHP·MariaDB에 대해 홈·검색·상품·장바구니·주문서와 모바일을 검증한다."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import os
import re
import sys
BASE = os.environ.get('YOURDAY_BASE_URL', 'http://127.0.0.1:8080').rstrip('/')
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':1440,'height':1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    response = page.goto(BASE, wait_until='networkidle')
    assert response.status == 200
    assert page.evaluate('g5_url') == BASE, '그누보드 내부 URL 포트 불일치'
    assert page.locator('.yd-product').count() == 8
    assert page.locator('.yd-product-image img').evaluate_all('(images) => images.every(i => i.complete && i.naturalWidth > 0)')
    page.screenshot(path='/tmp/yourday-desktop.png', full_page=True)
    page.get_by_role('button',name='아우터',exact=True).click()
    assert page.locator('.yd-product:visible').count() == 2
    page.get_by_role('button',name='전체',exact=True).click()
    assert page.locator('.yd-product:visible').count() == 8
    page.locator('#yd-search').fill('니트')
    page.locator('.yd-search button').click()
    page.wait_for_load_state('networkidle')
    assert '소프트 라운드 니트' in page.locator('body').inner_text()
    page.goto(BASE+'/shop/item.php?it_id=YD1001',wait_until='networkidle')
    page.screenshot(path='/tmp/yourday-item.png',full_page=True)
    assert page.locator('#sit_pvi_big img').first.evaluate('(i) => i.complete && i.naturalWidth > 0')
    page.locator('#it_option_1').select_option(index=2)
    page.locator('#it_option_1').press('Enter')
    assert page.locator('#sit_opt_added').inner_text().find('M') >= 0
    page.on('dialog', lambda d: d.accept())
    page.locator('#sit_ov_btn .sit_btn_cart').click()
    page.wait_for_url('**/shop/cart.php')
    page.wait_for_load_state('networkidle')
    assert '소프트 라운드 니트' in page.locator('#sod_bsk').inner_text()
    assert '39,000' in page.locator('#sod_bsk').inner_text()
    page.screenshot(path='/tmp/yourday-cart.png',full_page=True)
    page.get_by_role('button',name='주문하기',exact=True).click()
    page.wait_for_url(re.compile(r'/(bbs/login|shop/orderform)\.php'))
    page.wait_for_load_state('networkidle')
    if '/bbs/login.php' in page.url:
        page.locator('label[for=agree]').click()
        page.get_by_text('비회원으로 구매하기',exact=True).click()
        page.wait_for_url('**/shop/orderform.php')
        page.wait_for_load_state('networkidle')
    assert page.locator('#od_name').count() == 1
    assert page.locator('input[name=od_price]').input_value() == '39000'
    page.locator('label[for=od_settle_bank]').click()
    assert '실제 입금하지 마세요' in page.locator('body').inner_text()
    page.screenshot(path='/tmp/yourday-order.png',full_page=True)
    if '--place-order' in sys.argv:
        for prefix in ('od_', 'od_b_'):
            for key, value in {'name':'개발자동검증','tel':'0000000000','hp':'0000000000', 'zip':'00000','addr1':'개발용 가상주소 (배송금지)','addr2':'자동검증'}.items():
                page.locator('#'+prefix+key).fill(value)
        page.locator('#od_pwd').fill('YourdayTestOnly42')
        page.locator('#od_email').fill('shop-test@example.invalid')
        page.locator('#od_memo').fill('[자동검증] 개발용 샘플 주문입니다. 실제 배송·입금 금지.')
        page.locator('#od_deposit_name').fill('개발자동검증')
        page.locator('#display_pay_button input[type=button]').click()
        page.wait_for_url('**/shop/orderinquiryview.php?**',timeout=20000)
        page.wait_for_load_state('networkidle')
        assert '소프트 라운드 니트' in page.locator('body').inner_text()
        assert '42,000' in page.locator('body').inner_text()
        page.screenshot(path='/tmp/yourday-order-complete.png',full_page=True)
        print('PASS: 개발용 무통장 주문 저장·완료 화면 (실제 결제 없음)')
    print(json.dumps({'order_ready':True,'errors':errors},ensure_ascii=False))
    mobile = browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    mobile.goto(BASE,wait_until='networkidle')
    assert mobile.locator('.yd-product').count() == 8
    assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'), '홈 모바일 가로 넘침'
    mobile.screenshot(path='/tmp/yourday-mobile.png',full_page=True)
    mobile.goto(BASE+'/shop/item.php?it_id=YD1001',wait_until='networkidle')
    assert mobile.locator('#sit_ov_btn .sit_btn_cart').is_visible()
    assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'), '상세 모바일 가로 넘침'
    assert mobile.locator('#sit_inf_explan').bounding_box()['width'] >= 280
    assert mobile.locator('#sit_title').bounding_box()['height'] < 100
    mobile.screenshot(path='/tmp/yourday-mobile-item.png',full_page=True)
    settings = dict(line.split('=',1) for line in (Path(__file__).resolve().parents[2]/'.env').read_text().splitlines() if '=' in line)
    admin = browser.new_page(viewport={'width':1440,'height':1000})
    admin.goto(BASE+'/bbs/login.php?url='+BASE+'/adm/',wait_until='networkidle')
    admin.locator('#login_id').fill('admin')
    admin.locator('#login_pw').fill(settings['SHOP_ADMIN_PASSWORD'])
    admin.locator('#login_fs button[type=submit]').click()
    admin.wait_for_url(lambda url: url.split('?')[0].startswith(BASE+'/adm/'))
    admin.wait_for_load_state('networkidle')
    admin.screenshot(path='/tmp/yourday-admin.png',full_page=True)
    assert admin.locator('#gnb').count() > 0
    print('PASS: 관리자 로그인')
    assert not errors, errors
    print('PASS: 홈·필터·검색·상품·사이즈·장바구니·주문서·모바일')
    browser.close()
