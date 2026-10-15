<?php if (!defined('_GNUBOARD_')) exit; ?>
</div></main>
<footer class="yd-footer">
    <div class="yd-footer-top"><div><a class="yd-logo" href="<?php echo G5_URL; ?>/">YOURDAY</a><p>자연스러운 실루엣, 오래 함께할 옷.<br>당신의 평범한 하루를 조금 더 특별하게.</p></div>
    <div><h2>CUSTOMER CARE</h2><a href="<?php echo G5_BBS_URL; ?>/qalist.php">1:1 문의하기 ↗</a><p>배송 · 교환 · 반품에 대해 궁금하신가요?</p><a href="<?php echo G5_BBS_URL; ?>/faq.php">자주 묻는 질문</a></div>
    <div><h2>INFORMATION</h2><a href="<?php echo G5_SHOP_URL; ?>/orderinquiry.php">주문 · 배송 조회</a><a href="<?php echo G5_BBS_URL; ?>/board.php?bo_table=notice">공지사항</a><a href="<?php echo get_pretty_url('content', 'company'); ?>">브랜드 소개</a></div></div>
    <div class="yd-footer-bottom"><span>© <?php echo date('Y'); ?> YOURDAY. All rights reserved.</span><div><a href="<?php echo get_pretty_url('content', 'provision'); ?>">이용약관</a><a href="<?php echo get_pretty_url('content', 'privacy'); ?>">개인정보처리방침</a><?php if ($is_admin === 'super') { ?><a href="<?php echo G5_ADMIN_URL; ?>/">관리자</a><?php } ?></div></div>
    <?php if (!empty($default['de_admin_company_saupja_no'])) { ?><p class="yd-business">상호: <?php echo get_text($default['de_admin_company_name']); ?> · 대표: <?php echo get_text($default['de_admin_company_owner']); ?> · 사업자등록번호: <?php echo get_text($default['de_admin_company_saupja_no']); ?><br><?php echo get_text($default['de_admin_company_addr']); ?> · 통신판매업신고: <?php echo get_text($default['de_admin_tongsin_no']); ?></p><?php } ?>
</footer>
<script src="<?php echo G5_JS_URL; ?>/sns.js"></script>
<?php include G5_THEME_PATH.'/tail.sub.php'; ?>
