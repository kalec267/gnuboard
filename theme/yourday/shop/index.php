<?php
if (!defined('_GNUBOARD_')) exit;
if (!defined('_INDEX_')) define('_INDEX_', true);
$g5['title'] = '유어데이 · 당신의 하루를 입다';
include G5_THEME_SHOP_PATH.'/shop.head.php';
$items = sql_query("SELECT it_id, it_name, it_basic, it_price, it_cust_price, it_img1, it_type3, it_1, ca_id FROM {$g5['g5_shop_item_table']} WHERE it_use = 1 AND it_soldout = 0 ORDER BY it_order, it_id LIMIT 8");
?>
<section class="yd-hero" aria-labelledby="hero-title">
    <img class="yd-hero-photo" src="<?php echo G5_THEME_URL; ?>/assets/hero.png" alt="차분한 뉴트럴 컬러의 유어데이 가을 스타일링" fetchpriority="high">
    <div class="yd-hero-content"><p class="yd-eyebrow">THE EVERYDAY COLLECTION</p><h1 id="hero-title">당신의 하루를,<br>자연스럽게.</h1><p class="yd-hero-description">가장 나다운 편안함이 머무는 옷.<br>유어데이와 함께하는 새로운 계절.</p><a class="yd-button" href="<?php echo shop_type_url(3); ?>">새로운 컬렉션 만나기 <span aria-hidden="true">↗</span></a></div>
    <div class="yd-hero-caption"><span>YOUR DAY, YOUR WAY.</span><span>01 — EVERYDAY ESSENTIALS</span></div>
</section>
<div class="yd-value-strip"><span>Thoughtfully selected.</span><p>빠르게 바뀌는 유행보다, 오래도록 손이 가는 취향을 제안합니다.</p><span>Made for your everyday.</span></div>
<section class="yd-products" id="collection" aria-labelledby="collection-title">
    <div class="yd-section-heading"><div><p class="yd-eyebrow">CURATED FOR YOU</p><h2 id="collection-title">오늘의 유어데이</h2><p>매일의 옷장에 더하고 싶은, 편안한 선택.</p></div><a href="<?php echo G5_SHOP_URL; ?>/search.php">전체 상품 보기 <span aria-hidden="true">↗</span></a></div>
    <div class="yd-filters" role="group" aria-label="상품 카테고리 필터"><button class="is-active" data-category="all" aria-pressed="true">전체</button><button data-category="10" aria-pressed="false">아우터</button><button data-category="20" aria-pressed="false">니트 · 탑</button><button data-category="30" aria-pressed="false">팬츠</button><button data-category="40" aria-pressed="false">원피스</button><button data-category="50" aria-pressed="false">액세서리</button></div>
    <div class="yd-product-grid">
    <?php $count = 0; while ($item = sql_fetch_array($items)) { $count++; ?>
        <article class="yd-product" data-category="<?php echo get_text(substr($item['ca_id'], 0, 2)); ?>">
            <a class="yd-product-image" href="<?php echo shop_item_url($item['it_id']); ?>">
                <?php if ($item['it_type3']) { ?><span class="yd-label">NEW</span><?php } ?>
                <?php echo get_it_image($item['it_id'], 600, 750, '', '', get_text($item['it_name'])); ?>
                <span class="yd-view">자세히 보기 ↗</span>
            </a>
            <div class="yd-product-meta"><span class="yd-color-name"><?php echo get_text($item['it_1']); ?></span><span>YOURDAY</span></div>
            <h3><a href="<?php echo shop_item_url($item['it_id']); ?>"><?php echo get_text($item['it_name']); ?></a></h3>
            <p><?php echo get_text($item['it_basic']); ?></p>
            <div class="yd-price"><?php if ($item['it_cust_price'] > $item['it_price']) { ?><span class="yd-discount"><?php echo round((1 - $item['it_price'] / $item['it_cust_price']) * 100); ?>%</span><?php } ?><strong><?php echo number_format($item['it_price']); ?><small>원</small></strong><?php if ($item['it_cust_price'] > $item['it_price']) { ?><del><?php echo number_format($item['it_cust_price']); ?></del><?php } ?></div>
        </article>
    <?php } ?>
    </div>
    <p class="yd-empty" role="status" <?php if ($count) echo 'hidden'; ?>>아직 준비 중인 컬렉션입니다. 곧 새로운 상품으로 만나요.</p>
    <p class="yd-sample-note">현재 전시 상품은 기능 확인을 위한 샘플이며, 상품 이미지는 일러스트입니다.</p>
</section>
<section class="yd-editorial"><div class="yd-editorial-art" aria-hidden="true"><span>less,<br>but better.</span><img src="<?php echo G5_THEME_URL; ?>/assets/knit.svg" alt="" loading="lazy"></div><div class="yd-editorial-copy"><p class="yd-eyebrow">THE YOURDAY EDIT</p><h2>옷장에 남는 건,<br>결국 편안한 것.</h2><p>부드러운 촉감, 여유로운 실루엣,<br>그리고 어디에나 어울리는 차분한 색감.<br>유어데이가 생각하는 좋은 옷의 기준입니다.</p><a href="<?php echo get_pretty_url('content', 'company'); ?>">우리의 이야기 <span aria-hidden="true">↗</span></a></div></section>
<section class="yd-help"><div><p class="yd-eyebrow">WE ARE HERE FOR YOU</p><h2>오래 입을 수 있도록, 함께할게요.</h2></div><a href="<?php echo G5_BBS_URL; ?>/faq.php">배송 · 교환 · 반품 안내 ↗</a></section>
<script>
document.querySelectorAll('.yd-filters button').forEach(function(button) {
    button.addEventListener('click', function() {
        document.querySelectorAll('.yd-filters button').forEach(function(b) {
            var selected = b === button;
            b.classList.toggle('is-active', selected);
            b.setAttribute('aria-pressed', String(selected));
        });
        var visible = 0;
        document.querySelectorAll('.yd-product').forEach(function(card) {
            card.hidden = button.dataset.category !== 'all' && card.dataset.category !== button.dataset.category;
            if (!card.hidden) visible++;
        });
        document.querySelector('.yd-empty').hidden = visible > 0;
    });
});
</script>
<?php include G5_THEME_SHOP_PATH.'/shop.tail.php'; ?>
