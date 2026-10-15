<?php
if (!defined('_GNUBOARD_')) exit;
include_once G5_THEME_PATH.'/head.sub.php';
$q = isset($_GET['q']) && is_string($_GET['q']) ? get_text($_GET['q']) : '';
$categories = sql_query("SELECT ca_id, ca_name FROM {$g5['g5_shop_category_table']} WHERE ca_use = 1 AND LENGTH(ca_id) = 2 ORDER BY ca_order, ca_id");
?>
<a class="yd-skip" href="#container">본문 바로가기</a>
<div class="yd-announcement">일상의 모든 순간, 나다운 편안함 <span>YOURDAY COLLECTION</span></div>
<header class="yd-header">
    <div class="yd-header-main">
        <a class="yd-logo" href="<?php echo G5_URL; ?>/" aria-label="유어데이 홈">YOURDAY<span>wear your own day</span></a>
        <form class="yd-search" action="<?php echo G5_SHOP_URL; ?>/search.php" role="search">
            <label for="yd-search" class="sound_only">상품 검색</label>
            <input id="yd-search" name="q" type="search" minlength="2" maxlength="100" required placeholder="오늘의 취향을 찾아보세요" value="<?php echo $q; ?>">
            <button aria-label="검색" type="submit"><i class="fa fa-search" aria-hidden="true"></i></button>
        </form>
        <div class="yd-utilities">
            <?php if ($is_member) { ?><a href="<?php echo G5_BBS_URL; ?>/logout.php">로그아웃</a><?php } else { ?><a href="<?php echo G5_BBS_URL; ?>/login.php">로그인</a><?php } ?>
            <a href="<?php echo G5_SHOP_URL; ?>/mypage.php" aria-label="마이페이지"><i class="fa fa-user-o" aria-hidden="true"></i><span>마이페이지</span></a>
            <a href="<?php echo G5_SHOP_URL; ?>/cart.php" aria-label="장바구니"><i class="fa fa-shopping-bag" aria-hidden="true"></i><span>장바구니</span> <b><?php echo (int)get_boxcart_datas_count(); ?></b></a>
        </div>
    </div>
    <nav class="yd-nav" aria-label="쇼핑몰 메뉴">
        <a href="<?php echo G5_SHOP_URL; ?>/search.php">ALL</a>
        <a href="<?php echo shop_type_url(3); ?>">NEW</a>
        <a href="<?php echo shop_type_url(4); ?>">BEST</a>
        <span class="yd-nav-divider" aria-hidden="true"></span>
        <?php while ($category = sql_fetch_array($categories)) { ?>
        <a href="<?php echo G5_SHOP_URL.'/list.php?ca_id='.urlencode($category['ca_id']); ?>"><?php echo get_text($category['ca_name']); ?></a>
        <?php } ?>
        <a class="yd-community" href="<?php echo G5_BBS_URL; ?>/board.php?bo_table=notice">NOTICE</a>
        <a href="<?php echo G5_BBS_URL; ?>/faq.php">HELP</a>
    </nav>
</header>
<main id="container" class="yd-main <?php echo defined('_INDEX_') ? 'yd-home' : 'yd-inner'; ?>">
<?php if (!defined('_INDEX_')) { ?><div class="yd-breadcrumb"><a href="<?php echo G5_URL; ?>/">HOME</a> / <?php echo htmlspecialchars(html_entity_decode($g5['title'], ENT_QUOTES, 'UTF-8'), ENT_QUOTES, 'UTF-8'); ?></div><h1 class="yd-page-title"><?php echo htmlspecialchars(html_entity_decode($g5['title'], ENT_QUOTES, 'UTF-8'), ENT_QUOTES, 'UTF-8'); ?></h1><?php } ?>
<div class="shop-content">
