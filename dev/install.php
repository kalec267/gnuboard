<?php
// 개발 전용 CLI 설치. 웹에서는 Apache 설정과 아래 검사로 차단한다.
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$root = dirname(__DIR__);
if (is_file($root.'/data/dbconfig.php')) {
    echo "기존 설치를 보존합니다.\n";
    exit(0);
}
$password = getenv('SHOP_ADMIN_PASSWORD');
if (!$password || (strlen($password) < 16 || strlen($password) > 20)) { fwrite(STDERR, "관리자 비밀번호는 로그인 폼에 맞춰 16~20자로 설정해야 합니다.\n"); exit(1); }
$port = (int) (getenv('SHOP_PORT') ?: 8080);
$_SERVER = array_merge($_SERVER, array(
    'SERVER_PORT' => (string) $port, 'SERVER_NAME' => 'localhost', 'HTTP_HOST' => 'localhost:'.$port,
    'REMOTE_ADDR' => '127.0.0.1', 'REQUEST_URI' => '/install/install_db.php',
    'SCRIPT_NAME' => '/install/install_db.php', 'SCRIPT_FILENAME' => $root.'/install/install_db.php',
    'DOCUMENT_ROOT' => $root, 'REQUEST_METHOD' => 'POST'
));
$_POST = array('mysql_host'=>getenv('DB_HOST'), 'mysql_user'=>getenv('DB_USER'),
    'mysql_pass'=>getenv('DB_PASSWORD'), 'mysql_db'=>getenv('DB_NAME'), 'table_prefix'=>'g5_',
    'admin_id'=>'admin', 'admin_pass'=>$password, 'admin_name'=>'유어데이 관리자',
    'admin_email'=>'admin@yourday.example', 'g5_install'=>1,
    'g5_shop_prefix'=>'g5_shop_', 'g5_shop_install'=>1);
chdir($root.'/install');
ob_start();
register_shutdown_function(function () use ($root) {
    $output = ob_get_clean();
    if (!is_file($root.'/data/dbconfig.php') || strpos($output, '설치가 완료되었습니다') === false) {
        // 비밀번호가 포함될 수 있는 설치 출력은 표시하지 않는다.
        fwrite(STDERR, "설치 실패. PHP/DB 로그를 확인하세요.\n");
        exit(1);
    }
    chmod($root.'/data/dbconfig.php', 0600);
    echo "그누보드5·영카트 신규 설치 완료.\n";
});
require './install_db.php';
