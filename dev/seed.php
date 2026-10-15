<?php
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$root = dirname(__DIR__);
$marker = $root.'/data/yourday-seeded';
if (is_file($marker)) { echo "유어데이 초기 설정과 기존 상품을 보존합니다.\n"; exit; }
if (!is_file($root.'/data/dbconfig.php')) { fwrite(STDERR, "먼저 dev/install.php를 실행하세요.\n"); exit(1); }
$db = new mysqli(getenv('DB_HOST'), getenv('DB_USER'), getenv('DB_PASSWORD'), getenv('DB_NAME'));
$db->set_charset('utf8mb4');
$db->query("SET SESSION sql_mode = ''");
function query($sql, $args = array()) {
    global $db;
    $stmt = $db->prepare($sql);
    if ($args) $stmt->bind_param(str_repeat('s', count($args)), ...$args);
    $stmt->execute();
    return $stmt;
}
function insert($table, $values) {
    $columns = implode(',', array_map(function($s) { return '`'.$s.'`'; }, array_keys($values)));
    return query('INSERT INTO `'.$table.'` ('.$columns.') VALUES ('.implode(',', array_fill(0,count($values),'?')).')'.($table === 'g5_shop_category' ? ' ON DUPLICATE KEY UPDATE ca_id = ca_id' : ''), array_values($values));
}
// 실제 데이터가 있는 DB에 샘플 설정을 덮어쓰지 않는다.
if ((int)$db->query('SELECT COUNT(*) FROM g5_shop_item')->fetch_row()[0] > 0) {
    fwrite(STDERR, "상품이 이미 존재합니다. 샘플 초기화를 중단합니다.\n"); exit(1);
}
query("UPDATE g5_config SET cf_title = '유어데이', cf_theme = 'yourday', cf_email_use = 0, cf_use_email_certify = 0, cf_use_point = 0");
query("UPDATE g5_shop_default SET de_shop_skin = 'basic', de_shop_mobile_skin = 'basic', de_admin_company_name = '유어데이', de_admin_company_saupja_no = '', de_admin_company_owner = '', de_admin_company_addr = '', de_admin_company_tel = '', de_admin_company_fax = '', de_admin_tongsin_no = '', de_admin_info_name = '', de_admin_info_email = '', de_bank_use = 1, de_bank_account = '개발용 주문입니다. 실제 입금하지 마세요.', de_card_use = 0, de_vbank_use = 0, de_iche_use = 0, de_hp_use = 0, de_send_cost_case = '차등', de_send_cost_limit = '70000', de_send_cost_list = '3000', de_level_sell = 1, de_point_days = 0, de_rel_list_use = 0, de_shop_skin = 'basic'");
foreach (array('10'=>'아우터','20'=>'니트 · 탑','30'=>'팬츠','40'=>'원피스','50'=>'액세서리') as $id=>$name) {
    insert('g5_shop_category', array('ca_id'=>$id,'ca_name'=>$name,'ca_order'=>$id,'ca_use'=>1,'ca_skin'=>'list.10.skin.php','ca_img_width'=>280,'ca_img_height'=>350,'ca_list_mod'=>4,'ca_list_row'=>5,'ca_mobile_skin'=>'list.10.skin.php','ca_mobile_img_width'=>280,'ca_mobile_img_height'=>350,'ca_mobile_list_mod'=>2,'ca_mobile_list_row'=>5,'ca_stock_qty'=>100));
}
// DB 변경 전에 모든 샘플 이미지의 존재를 확인한다.
foreach (array('knit','blazer','pants','shirt','cardigan','dress','bag','coat') as $image) {
    if (!is_file($root.'/theme/yourday/assets/'.$image.'.png')) throw new RuntimeException('샘플 이미지 없음: '.$image);
}
$items = array(
    array('YD1001','20','소프트 라운드 니트','포근함을 담은 데일리 에센셜',39000,45000,'knit','오트밀','아크릴 50%, 울 30%, 나일론 20%'),
    array('YD1002','10','내추럴 싱글 블레이저','가볍게 걸치는 여유로운 실루엣',89000,99000,'blazer','베이지','폴리에스터 70%, 레이온 30%'),
    array('YD1003','30','데일리 와이드 슬랙스','편안하고 담백한 스트레이트 라인',49000,0,'pants','차콜','폴리에스터 80%, 레이온 20%'),
    array('YD1004','20','에센셜 코튼 셔츠','계절을 잇는 가장 기본적인 선택',42000,0,'shirt','아이보리','면 100%'),
    array('YD1005','20','릴렉스 브이넥 가디건','부드럽게 감싸는 차분한 컬러',54000,62000,'cardigan','세이지','아크릴 60%, 울 40%'),
    array('YD1006','40','플로우 롱 원피스','하루를 편안하게 채우는 한 벌',68000,0,'dress','그레이지','면 60%, 리넨 40%'),
    array('YD1007','50','미니멀 데일리 토트백','가벼운 외출에 함께하는 작은 여유',36000,42000,'bag','브라운','합성피혁'),
    array('YD1008','10','클래식 롱 코트','오래도록 곁에 두고 싶은 클래식',149000,0,'coat','카멜','울 50%, 폴리에스터 50%')
);
@mkdir($root.'/data/item', 0700, true);
foreach ($items as $n=>$item) {
    list($id,$cat,$name,$basic,$price,$original,$image,$color,$material)=$item;
    if (!copy($root.'/theme/yourday/assets/'.$image.'.png', $root.'/data/item/'.$id.'.png')) throw new RuntimeException('상품 이미지 복사 실패');
    $description='<div style="max-width:760px;margin:40px auto;text-align:center;line-height:2;padding:20px"><p>YOURDAY EVERYDAY COLLECTION</p><h2>'.htmlspecialchars($name).'</h2><p>'.htmlspecialchars($basic).'</p><p>차분한 일상에 자연스럽게 스며드는 유어데이의 선택입니다.</p><hr><p><strong>샘플 상품 안내</strong><br>이 상품은 쇼핑몰 기능 확인용이며 실제 판매 상품이 아닙니다.<br>이미지는 일러스트이며 소재·사이즈·가격은 예시입니다.</p><p>색상: '.$color.'<br>소재: '.$material.'<br>사이즈: S / M / L (샘플)'.($cat=='50'?'':'<br>케어: 소재에 맞춘 전문 세탁 권장').'</p><p>배송비 3,000원 / 70,000원 이상 무료 (예시 정책)</p></div>';
    insert('g5_shop_item', array('it_id'=>$id,'ca_id'=>$cat,'it_name'=>$name,'it_basic'=>$basic,'it_1'=>$color,'it_1_subj'=>'색상','it_option_subject'=>($cat==='50'?'':'사이즈'),'it_price'=>$price,'it_cust_price'=>$original,'it_use'=>1,'it_stock_qty'=>100,'it_buy_min_qty'=>1,'it_buy_max_qty'=>10,'it_order'=>$n,'it_type3'=>($n<4?1:0),'it_type4'=>1,'it_explan'=>$description,'it_explan2'=>strip_tags($description),'it_mobile_explan'=>$description,'it_img1'=>$id.'.png','it_time'=>date('Y-m-d H:i:s'),'it_update_time'=>date('Y-m-d H:i:s'),'it_skin'=>'basic','it_sc_type'=>0));
    if ($cat !== '50') {
        foreach (array('S','M','L') as $size) insert('g5_shop_item_option', array('it_id'=>$id,'io_id'=>$size,'io_type'=>0,'io_price'=>0,'io_stock_qty'=>30,'io_use'=>1));
    }
}
query("UPDATE g5_content SET co_subject = '유어데이 이야기', co_html = 1, co_content = ? WHERE co_id = 'company'", array('<h2>YOURDAY — 당신의 하루를 입다.</h2><p>빠르게 바뀌는 유행보다, 오래 함께할 수 있는 옷을 생각합니다. 부드러운 촉감, 자연스러운 실루엣, 편안한 색으로 당신의 평범한 하루를 채웁니다.</p><p>현재 사이트는 개발 중인 샘플 쇼핑몰입니다. 실제 판매 및 결제는 제공하지 않습니다.</p>'));
foreach (array('provision'=>'이용약관','privacy'=>'개인정보처리방침') as $id=>$subject) {
    query('UPDATE g5_content SET co_subject = ?, co_html = 1, co_content = ? WHERE co_id = ?', array($subject,'<h2>'.$subject.' — 개발용 초안</h2><p>이 사이트는 기능 확인을 위한 개발용 쇼핑몰입니다. 실제 개인정보나 결제정보를 입력하지 마세요.</p><p>운영 전 사업자, 수집 항목, 이용 목적, 보유 기간, 위탁 업체, 이용자 권리와 연락처 등 실제 운영에 맞는 문서를 등록해야 합니다.</p>',$id));
}
$faqs = array('배송은 얼마나 걸리나요?'=>'샘플 배송 정책: 결제 확인 후 영업일 기준 2~5일 이내 출고합니다. 실제 운영 전 배송 정책을 확정해 주세요.', '교환·반품은 어떻게 하나요?'=>'마이페이지의 1:1 문의로 접수할 수 있습니다. 현재는 개발용 쇼핑몰이므로 실제 주문·배송을 진행하지 않습니다.', '배송비는 얼마인가요?'=>'샘플 정책은 기본 3,000원이며 상품 합계 70,000원 이상은 무료입니다. 실제 운영 전 도서산간 지역의 추가 비용을 설정해 주세요.', '지금 구매할 수 있나요?'=>'현재 상품은 기능 확인을 위한 샘플입니다. 실제 입금이나 구매를 진행하지 마세요.');
$fm_id = 1;
query("UPDATE g5_faq_master SET fm_subject = '쇼핑 가이드' WHERE fm_id = 1");
foreach ($faqs as $subject=>$content) insert('g5_faq', array('fm_id'=>$fm_id,'fa_subject'=>$subject,'fa_content'=>'<p>'.$content.'</p>'));
insert('g5_write_notice', array('wr_num'=>-1,'wr_reply'=>'','wr_parent'=>0,'wr_is_comment'=>0,'wr_subject'=>'유어데이에 오신 것을 환영합니다','wr_content'=>'차분한 일상을 위한 옷, 유어데이입니다. 현재는 개발용 샘플 쇼핑몰이며 실제 주문·입금은 진행하지 않습니다.','mb_id'=>'admin','wr_name'=>'유어데이','wr_datetime'=>date('Y-m-d H:i:s'),'wr_last'=>date('Y-m-d H:i:s'),'wr_ip'=>'127.0.0.1'));
$notice_id = $db->insert_id;
query('UPDATE g5_write_notice SET wr_parent = ? WHERE wr_id = ?', array($notice_id,$notice_id));
query("UPDATE g5_board SET bo_count_write = 1, bo_write_level = 10 WHERE bo_table = 'notice'");
file_put_contents($marker, "유어데이 샘플 데이터 초기화 완료\n");
echo "유어데이 테마·5개 분류·8개 샘플 상품·브랜드 소개·FAQ 설정 완료.\n";
