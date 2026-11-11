---
theme: ./theme
title: 跟著洪愛珠走大稻埕
colorSchema: light
aspectRatio: 16/9
canvasWidth: 980
exportFilename: dadaocheng-walk
layout: cover
kicker: 文學經典閱讀・期中報告
team: 第 X 組
members:
  - 董兆陽
  - 鄭宇晨
  - 陳煇勝
  - 李亦宸
topics:
  - label: 洪愛珠《老派少女購物路線》
    color: red
  - label: 大稻埕
    color: blue
meta: 2026.11.11
qr: https://nath.tw/dadaocheng-walk-slides/
qrLabel: 掃描看簡報
---

# 老鋪還在嗎？

洪愛珠《老派少女購物路線》× 大稻埕

---
layout: default
---

# 組員貢獻

<div class="contrib">
  <svg class="donut" viewBox="0 0 42 42" role="img" aria-label="四位組員各占 25%">
    <circle v-for="(m, i) in members" :key="m.name" cx="21" cy="21" r="15.9155" fill="none"
      :stroke="m.color" stroke-width="7" :stroke-dasharray="`24.6 75.4`"
      :stroke-dashoffset="25 - i * 25 - 0.2" />
    <text x="21" y="20.2" text-anchor="middle" class="donut-big">4 人</text>
    <text x="21" y="25.4" text-anchor="middle" class="donut-small">我們合作無間！</text>
  </svg>
  <ul class="contrib-list">
    <li v-for="m in members" :key="m.name">
      <span class="dot" :style="{ background: m.color }" />
      <b>{{ m.name }}</b>
      <span class="pct">25%</span>
      <span class="tasks">{{ m.tasks.join('、') }}</span>
    </li>
  </ul>
</div>

<script setup>
const members = [
  { name: '董兆陽', color: 'var(--google-blue)', tasks: ['簡報製作與排版', 'AI 內容查核'] },
  { name: '鄭宇晨', color: 'var(--google-red)', tasks: ['文本精讀與引文摘錄', '走讀路線規劃'] },
  { name: '陳煇勝', color: 'var(--google-yellow)', tasks: ['現場拍照紀錄', '講稿撰寫與彩排'] },
  { name: '李亦宸', color: 'var(--google-green)', tasks: ['景點資料蒐集', '老照片與授權查找'] },
]
</script>

<style>
.contrib { display: flex; align-items: center; gap: 3rem; margin-top: 2.2rem; }
.contrib .donut { flex: none; width: 15rem; height: 15rem; }
.contrib .donut-big { font-size: 5px; font-weight: 700; fill: var(--google-ink); }
.contrib .donut-small { font-size: 2.6px; fill: var(--google-muted); }
.contrib-list { list-style: none; margin: 0; padding: 0; flex: 1; }
.contrib-list li { display: grid; grid-template-columns: 1rem 4.5rem 3.5rem 1fr; align-items: center; gap: .6rem; padding: .7rem 0; border-bottom: 1px solid var(--google-border); font-size: 20px; }
.contrib-list li:last-child { border-bottom: none; }
.contrib-list .dot { width: .85rem; height: .85rem; border-radius: 50%; }
.contrib-list .pct { color: var(--google-muted); font-variant-numeric: tabular-nums; }
.contrib-list .tasks { color: var(--google-ink); font-size: 18px; text-align: left; }
</style>

---
layout: book
image: /images/book-cover-3d.jpg
clicks: 1
---

# 《老派少女購物路線》

洪愛珠｜遠流，2021

::quote::

# 「當親人已無法好起來，你還能為她做什麼？」

<!--
- 洪愛珠的媽媽已經病得很重
- 女兒想透過準備媽媽願意吃的東西，與她多保留一些交流
- 當一個人已經無法讓親人的病好起來，「今天還能替她做什麼」就會變得非常具體。準備一道她想吃的菜，是女兒此刻還能做的事
- 有一天，媽媽想吃炸春捲，於是她去找新鮮潤餅皮，回來現做。這就是她前往大稻埕的原因
-->

---
layout: quote
---

# 「但只要老鋪猶在，民生氣息仍厚，就不至於弄得太面目全非。」

洪愛珠〈老派少女購物路線〉

<!--
- 對洪愛珠來說，大稻埕也不只是一個他母親病重時想買春捲的地方
- 這裡是他小時候，外婆會帶她來一起買東西的地方，
  - 在這裡，他被帶進了外婆的生活
  - 在這裡，記住了他以前是怎麼被照顧的
  - 今天，輪到他照顧別人
- 當然在他再次到訪時，大稻埕已經變了很多
- 大家在回到自己國小時應該也會有同樣的感覺
-->

---
layout: image-right
image: /images/tcmb-xiahai-postcard.jpg
backgroundSize: contain
kicker: 選定景點
---

# 為何是大稻埕

三代女性的採買路線

<div class="credit">臺北霞海城隍廟全景（日治時期明信片）｜國立臺灣歷史博物館／文化部典藏網，CC BY 3.0 TW，via 國家文化記憶庫</div>

<style>
.credit { position: absolute; left: 4.4rem; bottom: 2rem; max-width: 24rem; font-size: 13px; line-height: 1.5; color: var(--google-muted); }
</style>

<!--
那所以，我們選的地點就是大稻埕啦
-->

---
layout: figure
kicker: 預估走 40–50 分鐘
clicks: 6
---

# AI 排的六站

::figure::

<div class="stop-split">
  <div class="stop-map"><RouteMap :active="$clicks" draw labels="active" /></div>
  <div class="stop-panel">
    <template v-for="(s, i) in [
      { img: '/images/web/1-yongtai.jpg', name: '永泰食品行', credit: '圖／TVBS 新聞（2026.9）' },
      { img: '/images/web/2-zisheng.jpg', name: '滋生青草店', credit: '圖／Openbook 閱讀誌（2021）' },
      { img: '/images/web/3-yongle-market.jpg', name: '永樂市場', credit: '毛貓大少爺／Wikimedia Commons, CC BY-SA 2.0' },
      { img: '/images/web/4-watsons.jpg', name: '小藝埕（原屈臣氏大藥房）', credit: 'Chi-Hung Lin／Wikimedia Commons, CC BY-SA 2.0' },
      { img: '/images/web/5-shengji.jpg', name: '生記藥行', credit: '圖／Openbook 閱讀誌（2021）' },
      { img: '/images/web/6-xiahai.jpg', name: '臺北霞海城隍廟', credit: 'nakashi／Wikimedia Commons, CC BY-SA 2.0' },
    ]" :key="i">
      <figure v-if="$clicks === i + 1" class="stop-card">
        <img :src="base + s.img.replace(/^\//, '')" :alt="s.name" />
        <figcaption><b>{{ String(i + 1).padStart(2, '0') }}</b> {{ s.name }}</figcaption>
        <div class="stop-credit">{{ s.credit }}</div>
      </figure>
    </template>
    <div v-if="$clicks === 0" class="stop-hint">事前資料・網路照片</div>
  </div>
</div>

<script setup>
// Dynamic :src isn't rewritten by Vite, so prefix the deploy base (ends with '/') ourselves.
const base = import.meta.env.BASE_URL
</script>

<style>
.stop-split { display: flex; gap: 1.2rem; width: 100%; height: 100%; }
.stop-map { flex: 1.35; min-width: 0; height: 100%; }
.stop-panel { flex: 1; min-width: 0; height: 100%; display: flex; align-items: center; }
.stop-card { margin: 0; width: 100%; animation: stop-in .35s ease; }
.stop-card img { width: 100%; height: 15.5rem; object-fit: cover; border-radius: 12px; box-shadow: var(--google-shadow); display: block; }
.stop-card figcaption { margin-top: .6rem; font-size: 1.15rem; font-weight: 600; color: var(--google-ink); }
.stop-card figcaption b { color: var(--google-blue); margin-right: .35rem; }
.stop-credit { margin-top: .15rem; font-size: 11px; color: var(--google-muted); }
.stop-hint { width: 100%; text-align: center; color: var(--google-muted); font-size: .95rem; }
@keyframes stop-in { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
</style>

<!--
- 我們把書的整篇內文和背景資料喂給 AI（非常尊重著作權 :D）
- 給他指示做出我們的路線，他給了我們這坨
- 大致就是：
  1. 永泰食品行
  2. 滋生青草店
  3. 永樂市場
  4. 小藝程
  5. 生記藥行
  6. 霞海城隍廟
-->

---
layout: book-vs-now
quote: 今僅存一家『⁠永⁠泰⁠食⁠品⁠行⁠』
label: 01 永泰食品行舊址
image: /images/01-yongtai-03-construction-hoarding.jpg
position: 72% 50%
---

現場：永泰不見了

<!--
- 洪愛珠小時候被外婆帶來買時會在路上買零食
- 永泰食品行是他再次來訪時所剩的一家
- 如今也不見蹤影，sad
-->

---
layout: book-vs-now
quote: 穿出隧道右轉，喝民樂街的涼茶。
label: 02 民樂街青草店
image: /images/02-minle-herbal-07-tea-stand-prices.jpg
position: 40% 50%
caption: 苦茶，就是純苦
---

現場：換了新樣子

<!--
- 在消失的永泰食品行後，是一家青草茶店
- 這是同一段路，但這裡有個有趣的點
  - 原文中洪愛珠沒有寫出店名，只是說「民樂街的涼茶」
  - 他是用掌店的老太太認出店家的，後才發現店名
- 我們也實際喝了
  - 陳輝勝：苦茶，就是純苦
  - 鄭宇晨：青草茶，前面還有青草味，後面就是純苦

我想我們還是不太適合那個時代的飲料
-->

---
layout: book-vs-now
quote: 沒忘記今日來，是為⁠媽⁠媽⁠買⁠潤⁠餅⁠皮⁠。
label: 03 永樂市場
image: /images/03-yongle-market-11-fabric-hall-corridor.jpg
position: 50% 55%
---

現場：二樓滿滿是布

<!--
- 他前面寫了許多採買的回憶，但這邊把我們帶回主線任務
- 接著他終於進到正事了，買餅皮，他說他到了一家叫做「林良號」的店買餅皮、還聊了好一段時間
- 在我們到的時候，賣餅皮的店家也已經找不到了
-->

---
layout: mosaic
photos:
  - src: /images/04-xiaoyiyicheng-02-artyard-facades.jpg
    label: 04 小藝埕
  - src: /images/05-shengji-04-shengji-storefront.jpg
    label: 05 生記藥行
---

# 生記還在

<!--
- 倒是幾個書中有提到的，生記藥行和小藝程都還在，不過都淹沒在機車和連鎖店之間了
-->

---
layout: photo
image: /images/06-xiahai-temple-01-temple-front.jpg
position: 50% 40%
label: 06 霞海城隍廟
caption: 不知道順序，看人流跟著拜
map: 6
scrim: strong
---

<!--
- 那我們最後也到了大稻埕著名的霞海城隍廟
- 這裡的月老據說挺靈的，可以給這幾位（組員們）期待一下
-->

---
layout: quote
---

# 「恍惚間她們鬆手，長長的百年的大街上，四顧僅餘我一人。」

洪愛珠〈老派少女購物路線〉

<!--
- 在洪愛珠的路程最後，有店家問起家人的近況
- 外婆離世、媽媽病重
- 在路上的這整篇回憶裡，外婆與媽媽好像一直陪著她；到了結尾，她重新感覺到，自己正在失去這份陪伴
- 這也是這篇散文的結尾
-->

---
layout: reflection
kicker: 組員心得
---

::name::

# 鄭宇晨

::default::

<v-switch unmount>
<template #0>

跟著洪愛珠走大稻埕，我原以為在尋找舊時光，實際卻像在追趕一段正在遠去的記憶。延平北路二段三十六巷裡，永泰食品行舊址仍在，店卻已歇業，只剩賣烏魚子的攤子。我站在巷口，試著把書中外婆買甘納豆、作者買蛋酥花生的畫面疊上眼前冷清，卻怎麼也拼不回來。我發現走讀不是朝聖打卡，而是走到書中發生過的地方，看它如今變成什麼模樣。

民樂街兩家青草店，一家保留老門面，一家把青草茶做成茶包、藥浴包。我也買了一杯。入口先苦後甘，涼意慢慢壓下身體的燥熱。青草茶退的不只是人體的火，也退了街上的煙火氣：迪化街的叫賣、貨車、香火仍熱鬧，口中的苦甘卻讓城市暫時降溫，也讓我在匆忙裡安靜下來。

</template>
<template #1>

永樂市場裡，林良號仍手工抹出薄透潤餅皮，顏記冰飲店卻已收攤；生記藥行拉開木藥櫃、以砝碼秤藥，讓我看到上一代人對生活的講究。走到霞海城隍廟，香火混著乾貨氣味，我終於不再執著找齊每家店。有些消失，有些轉型，有些仍守著原樣。

這條路線其實是一條告別的路線。我們無法阻止老店歇業，卻能在消失之前走進巷弄，記住一塊招牌、一種氣味，和有人生活過的證明。

</template>
</v-switch>

---
layout: reflection
kicker: 組員心得
---

::name::

# 陳煇勝

::default::

這次旅程比起單純逛街，我覺得更多了一份「對照現實與書中記憶」的新鮮感。雖然整趟走讀的時間不長，但實地走過一趟，還是留下許多很深刻的瞬間。

最讓我印象深刻的，莫過於在民樂街買的那杯苦茶，喝完只覺得味道很單純且天然，喝下第一口的瞬間，真的苦到胃裡！那種完全不加調味、鋪天蓋地的純粹苦味，才配得起「苦茶」這個名字。

另一個很有感的時刻，是我們來到最後一個行程「霞海城隍廟」。說實話，我和組員其實都不太清楚正確的拜拜路線與順序，最後大家完全是看著現場滿滿的人流，憑著腦海裡殘存的拜拜記憶跟著拜。雖然過程有點手忙腳亂，但大家都很恭敬、很認真，我覺得只要心意到了，其實就已經足夠了。

這趟走讀雖然沒有刻意走完所有景點，但在這條新舊交融的街區裡，透過這些歷史建築以及傳統工藝產品，讓我對大稻埕這片土地的歷史與人情味有了更真實的感受。

---
layout: reflection
kicker: 組員心得
---

::name::

# 李亦宸

::default::

進到大稻埕好像時間暫停一樣，那邊賣得食物都很有古早味，像青草茶、苦茶和一些果乾。大稻埕的建築風格也很古早，騎樓非常寬，地板為紅磚所構成。我印象最深刻的景點是永樂市場，那邊的攤位非常靠近，行走非常困難，都被各種的布所堆滿。永樂市場有賣各式各樣的布，是平常不會看到的，非常的新奇。

---
layout: reflection
kicker: 組員心得
---

::name::

# 董兆陽

::default::

<v-switch unmount>
<template #0>

在準備這次走讀時，我對大稻埕的印象，主要是迪化街的紅磚老屋和傳統商店，原本以為只要沿著洪愛珠的《老派少女購物路線》找幾家老店，就能看見書裡的風景。真正走進延平北路二段的巷子，眼前卻是機車、老住宅和施工圍籬，完全不像我想像中整齊的懷舊街景。書中提到，作者小時候和外婆、媽媽會從這裡穿過，順路到永泰食品行買甘納豆、蛋酥花生；如今那家老店已經歇業，我們只能試著從眼前的街道想像她當年的記憶。原來走讀不一定是找到書裡描述的東西，有時反而是發現它已經不在了。

走到民樂街時，我們看見青草店裡各種茶飲和草藥，組員還買了青草茶與苦茶試喝。洪愛珠在書裡提到，自己小時候認得的不是店名，而是站在店裡的老太太。我以前不太會注意這種細節，但這次才發現，老店不只是建築或招牌，也是人與人長期建立的熟悉感。接著走進永樂市場，攤位之間擺滿布料，走道裡不斷有人穿梭。這裡看起來就是一座忙碌的市場，可是想到作者曾為生病的母親回來尋找潤餅皮，才明白同一個地方，對不同人可能有完全不同的意義。

</template>
<template #1>

這次我也拍了不少照片。回頭整理時才注意到，鏡頭裡不只有古老的街屋，還有新大樓、機車、店家重新整理過的門面，以及沒有特別裝飾的巷弄。它們未必符合大家想像中的「復古」，卻讓我感覺大稻埕不是停在過去的景點，而是一個仍然有人生活、做生意，也持續改變的地方。

最後走到霞海城隍廟，和組員留下合照。這一趟最讓我有感的，其實不是走過多少個景點，而是開始理解洪愛珠為什麼能從日常採買寫出一整篇故事。對她而言，購物路線連著家人的記憶；對我們而言，這次走訪也讓原本只是地圖上幾條街的地方，多了可以記住的畫面與故事。

</template>
</v-switch>

---
layout: photo
image: /images/06-xiahai-temple-04-group-selfie.jpg
position: 50% 45%
caption: 臺北霞海城隍廟　2026.10.26
scrim: light
---

---
layout: default
---

# 關於這份簡報

<div class="google-qr-row">
  <QrCode url="https://github.com/Nat1anWasTaken/dadaocheng-walk-slides" label="GitHub Repo" size="12rem" />
  <QrCode url="https://sli.dev/" label="Slidev" size="12rem" />
</div>

<!--
（剛剛我的敘述中其實有一個很大的邏輯滑坡，有人注意到就注意到，沒有注意到就算了，嘻嘻）

- 這份簡報是寫程式生出來的
- 左邊是原始碼、右邊是我們使用的叫做 Slidev 的簡報框架
- 搭配一些小小的網頁開發知識，會比起讓 AI 直接操作 Canva / Google Slides / PowerPoint 等為人類設計的簡報軟體來得高效很多，推薦大家試試
- 你也可以把這兩個連結丟個自己的 AI 問問怎麼做
-->
