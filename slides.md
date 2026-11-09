---
theme: ./theme
title: 老鋪還在嗎？跟著洪愛珠走大稻埕
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
---

# 老鋪還在嗎？

洪愛珠《老派少女購物路線》× 大稻埕

<!--
【講者：董兆陽】
大家好，我們走的是洪愛珠《老派少女購物路線》裡的大稻埕。先問大家一個問題：一本五年前的書寫到的老店，現在還剩幾家？
TODO(組別)：封面的「第 X 組」要換成真正的組別，i-learning 上查不到。
TODO(確認)：N5 建議說「書出版五年後」較精確（文章 2018 年得獎，書 2021 年出版）。
-->

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
    <text x="21" y="25.4" text-anchor="middle" class="donut-small">各 25%</text>
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
.contrib .donut-small { font-size: 3px; fill: var(--google-muted); }
.contrib-list { list-style: none; margin: 0; padding: 0; flex: 1; }
.contrib-list li { display: grid; grid-template-columns: 1rem 4.5rem 3.5rem 1fr; align-items: center; gap: .6rem; padding: .7rem 0; border-bottom: 1px solid var(--google-border); font-size: 20px; }
.contrib-list li:last-child { border-bottom: none; }
.contrib-list .dot { width: .85rem; height: .85rem; border-radius: 50%; }
.contrib-list .pct { color: var(--google-muted); font-variant-numeric: tabular-nums; }
.contrib-list .tasks { color: var(--google-ink); font-size: 18px; text-align: left; }
</style>

<!--
【講者：董兆陽】
這是我們的分工，四個人各負責兩項，比例平均。
-->

---
layout: quote
---

# 「但只要老鋪猶在，民生氣息仍厚，就不至於弄得太面目全非。」

洪愛珠〈老派少女購物路線〉

<!--
【講者：董兆陽】
書裡有一句話，成了我們這趟的主軸：「但只要老鋪猶在，民生氣息仍厚，就不至於弄得太面目全非。」這是作者的外婆、媽媽和她自己，三代人一起採買的路。十月二十六號，我們拿著書去對答案。
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
【講者：董兆陽】
為什麼選大稻埕？老師的清單裡，這條路線最貼近日常：買菜、吃東西，一家人的採買，不是名勝。我們在國家文化記憶庫找到這張城隍廟的老明信片，還有郭雪湖一九三〇年的〈南街殷賑〉，畫的就是這一帶的熱鬧。
TODO(組員補充)：如果有組員自己選這條路線的理由（例如長輩常去迪化街），放進來，比「清單裡最貼近日常」有力。
備註：〈南街殷賑〉圖像標示「僅限公開瀏覽」，不可放圖，只在口頭提到名稱。
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
【講者：鄭宇晨】
出發前，我們請 AI 幫忙整理資料、排路線：永泰食品行、民樂街青草店、永樂市場、小藝埕、生記藥行，最後是霞海城隍廟，預估走四十到五十分鐘。每一站它都附了書裡的故事，看起來很完整。接下來就一站一站對照。
TODO(確認)：「探勘地點清單」（10/21）是否真的是 AI 產出？若是半人工整理，改說「我們用 AI 協助整理」。
備註：點擊六次，每次點出一站。
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
【講者：鄭宇晨】
第一站。書裡說，這個像隧道的巷口，「今僅存一家『永泰食品行』」，外婆在這裡買甘納豆，作者愛吃蛋酥花生。出發前我們查到，永泰九月二十六號歇業了，我們晚了剛好一個月。現場一整排施工圍籬，已經找不到永泰的影子。我想把書裡的畫面疊上去，卻怎麼也拼不回來。
TODO(鄭宇晨)：可以加一句屬於自己的話，約 30 字，例如「我家也有一家這樣的店或一種味道」。
備註：永泰 9/26 歇業，來源 TVBS 2026-09-09。
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
【講者：陳煇勝】
書上接著寫：「穿出隧道右轉，喝民樂街的涼茶。」兩家青草店，作者「全憑位置或人臉辨識」，通常認有老太太顧店的那家，也就是滋生。我們停下來的，卻是另一家姚德和，已經換成賣茶包的新樣子。我點了一杯苦茶，第一口就苦到胃裡，沒有回甘，就是純苦。
備註：只拍到姚德和（55 號），沒拍到滋生。年份不要念，各來源說法不一。
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
【講者：李亦宸】
書裡最痛的一段在永樂市場：「沒忘記今日來，是為媽媽買潤餅皮。」林良號的阿姨問她：「恁阿嬤閣佇咧無？」她只能說：「無佇咧啊。」我們在市場裡拍到的，卻是二樓滿滿的布；書裡那一攤，我們的照片裡一張也沒有。
TODO(確認)：鄭宇晨的心得寫「林良號仍手工抹出薄透潤餅皮，顏記冰飲店卻已收攤」。照片無法佐證，請他確認是否親眼看到。有看到：最後一句改成「宇晨在一樓有看到林良號還在抹餅皮，可惜我們沒有拍下來」。沒看到：維持現在講法。
TODO(確認)：顏記是否已收攤只有 TVBS「預計 2 月底收攤」的報導，沒有人現場看到就不要講。
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
【講者：李亦宸】
接著是小藝埕的洋樓，和生記藥行。書裡寫，就算只買一包滷包，店家也會拉開木抽屜，用砝碼現秤。可是我們在生記門口拍完招牌就走了。老鋪還在，是我們自己沒走進去。
TODO(確認)：生記的木抽屜與砝碼是書中內容，還是當天有看到？
TODO(選用)：N2 若時間允許可加一句「老師講義裡穿旗袍的那張照片，就是在這棟樓前拍的。」
-->

---
layout: default
---

# 替 AI 改作業

<div class="paper">
  <div class="line">
    <p>延平北路 → 民樂街 → 永樂市場 → 迪化街 → 生記藥行 → <span v-mark="{ at: 1, color: '#d93025', type: 'circle' }">霞海城隍廟</span></p>
    <div class="pen" v-click="1">路線走得通</div>
  </div>
  <div class="line">
    <p>第三代姚勝雄……<span v-mark="{ at: 2, color: '#d93025', type: 'strike-through' }">在父親原本不贊成的情況下</span>推動2017年店面改造</p>
    <div class="pen" v-click="2">這是建翔蔬菜的故事</div>
  </div>
  <div class="line">
    <p>位置：迪化街一段21號；林良號史料位置為<span v-mark="{ at: 3, color: '#d93025', type: 'underline' }">一樓1506號攤</span></p>
    <div class="pen" v-click="3">門牌在，人呢？</div>
  </div>
  <div class="src">摘自出發前 AI 整理的〈探勘地點清單〉（10/21）</div>
</div>

<style>
.paper { margin-top: 32px; padding: 20px 32px 20px; background: #fffdf7; border: 1px solid var(--google-border); border-radius: 6px; box-shadow: var(--google-shadow); font-family: 'Noto Serif TC Deck', serif; }
.paper .line { display: flex; align-items: baseline; justify-content: space-between; gap: 24px; padding: 24px 0; border-bottom: 1px dashed #e6dfcf; }
.paper .line:last-of-type { border-bottom: none; }
.paper p { margin: 0; font-size: 19px; white-space: nowrap; color: var(--google-ink); }
.paper .pen { flex: none; font-size: 19px; color: #d93025; transform: rotate(-3deg); white-space: nowrap; }
.paper .src { margin-top: 10px; font-family: 'Google Sans', sans-serif; font-size: 12px; color: var(--google-muted); }
</style>

<!--
【講者：董兆陽】
回頭替 AI 打分數。路線排得順，書裡的故事也抓到大概，這是它做對的；但它也會自己加油添醋。做錯的是張冠李戴：它把市場裡另一家菜攤「父親反對」的故事，安到青草店頭上。它最不知道的，是今天誰還開著。作者認的是人臉，AI 給的是門牌。
備註：點擊三次，紅筆依序畫上（圈、刪、底線）。
備註：AI 行程清單確實寫了姚德和第三代在父親原本不贊成下推動 2017 年改造，所以「它說」是準確的；經查，父親反對的故事屬於建翔蔬菜（王建翔與父親），來源為市場處原文。
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
【講者：陳煇勝】
最後一站。書裡只寫了一句：「不遠處霞海城隍廟的香火，也嗅得一點。」那是作者陪病兩年，一到迪化街，覺得自己還紮實活著的時刻。我們到的時候廟前擠滿了人，說實話，大家都不知道拜拜的順序，只好看人流，前面的人拜哪裡就跟著拜。有點手忙腳亂，但心意到了。
-->

---
layout: quote
---

# 「恍惚間她們鬆手，長長的百年的大街上，四顧僅餘我一人。」

洪愛珠〈老派少女購物路線〉

<!--
【講者：鄭宇晨】
書的最後一句是：「恍惚間她們鬆手，長長的百年的大街上，四顧僅餘我一人。」外婆走了，媽媽也在告別。走完這一趟，我們發現連老鋪也開始鬆手：有的收了，有的換了樣子，有的還守著原樣。
【講者：董兆陽】
TODO(董兆陽心得)：約 60 字，請董兆陽用自己的話補一段，不要由別人代寫。方向：這趟路有沒有讓你想到自己家裡長輩常去的某家店、某條路或某個味道？
-->

---
layout: reflection
kicker: 組員心得
---

::name::

# 鄭宇晨

::default::

跟著洪愛珠走大稻埕，我原以為在尋找舊時光，實際卻像在追趕一段正在遠去的記憶。延平北路二段三十六巷裡，永泰食品行舊址仍在，店卻已歇業，只剩賣烏魚子的攤子。我站在巷口，試著把書中外婆買甘納豆、作者買蛋酥花生的畫面疊上眼前冷清，卻怎麼也拼不回來。我發現走讀不是朝聖打卡，而是走到書中發生過的地方，看它如今變成什麼模樣。

民樂街兩家青草店，一家保留老門面，一家把青草茶做成茶包、藥浴包。我也買了一杯。入口先苦後甘，涼意慢慢壓下身體的燥熱。青草茶退的不只是人體的火，也退了街上的煙火氣：迪化街的叫賣、貨車、香火仍熱鬧，口中的苦甘卻讓城市暫時降溫，也讓我在匆忙裡安靜下來。

永樂市場裡，林良號仍手工抹出薄透潤餅皮，顏記冰飲店卻已收攤；生記藥行拉開木藥櫃、以砝碼秤藥，讓我看到上一代人對生活的講究。走到霞海城隍廟，香火混著乾貨氣味，我終於不再執著找齊每家店。有些消失，有些轉型，有些仍守著原樣。

這條路線其實是一條告別的路線。我們無法阻止老店歇業，卻能在消失之前走進巷弄，記住一塊招牌、一種氣味，和有人生活過的證明。

<!--
組員心得全文（取自「文學走讀作業 - 心得」Google Doc）。可依時間決定是否朗讀，或只停留讓老師閱讀。
-->

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

<!--
組員心得全文（取自「文學走讀作業 - 心得」Google Doc）。
-->

---
layout: reflection
kicker: 組員心得
---

::name::

# 李亦宸

::default::

進到大稻埕好像時間暫停一樣，那邊賣得食物都很有古早味，像青草茶、苦茶和一些果乾。大稻埕的建築風格也很古早，騎樓非常寬，地板為紅磚所構成。我印象最深刻的景點是永樂市場，那邊的攤位非常靠近，行走非常困難，都被各種的布所堆滿。永樂市場有賣各式各樣的布，是平常不會看到的，非常的新奇。

<!--
組員心得全文（取自「文學走讀作業 - 心得」Google Doc）。
-->

---
layout: reflection
kicker: 組員心得
---

::name::

# 董兆陽

::default::

<p class="pending">（撰寫中）</p>

<!--
TODO(董兆陽心得)：Google Doc 裡董兆陽標題下仍是空的，寫好後貼到這裡，取代「撰寫中」。
-->

---
layout: photo
image: /images/06-xiahai-temple-04-group-selfie.jpg
position: 50% 45%
caption: 臺北霞海城隍廟　2026.10.26
scrim: light
---

<!--
【講者：董兆陽】
這是我們在城隍廟前的合照。老店會關，但那杯苦茶有多苦，我們會記得。謝謝大家。
TODO(合照)：合照只有 4 人。作業要求全組到此一遊，若有第五位組員，請找他入鏡的照片或準備一句說明。
TODO(同意)：上台前確認 4 位組員都同意自己的臉出現在公開網站上。
-->
