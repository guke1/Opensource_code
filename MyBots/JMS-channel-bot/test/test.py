from lxml import etree
text = """
<div id="info">
        <span ><span class='pl'>导演</span>: <span class='attrs'><a href="/celebrity/1028333/" rel="v:directedBy">丹尼斯·维伦纽瓦</a></span></span><br/>
        <span ><span class='pl'>编剧</span>: <span class='attrs'><a href="/celebrity/1009628/">汉普顿·范彻</a> / <a href="/celebrity/1339873/">迈克尔·格林</a> / <a href="/celebrity/1036650/">菲利普·K·迪克</a></span></span><br/>
        <span class="actor"><span class='pl'>主演</span>: <span class='attrs'><a href="/celebrity/1012531/" rel="v:starring">瑞恩·高斯林</a> / <a href="/celebrity/1009238/" rel="v:starring">哈里森·福特</a> / <a href="/celebrity/1045259/" rel="v:starring">安娜·德·阿玛斯</a> / <a href="/celebrity/1018643/" rel="v:starring">西尔维娅·侯克斯</a> / <a href="/celebrity/1002676/" rel="v:starring">罗宾·怀特</a> / <a href="/celebrity/1013764/" rel="v:starring">杰瑞德·莱托</a> / <a href="/celebrity/1014003/" rel="v:starring">戴夫·巴蒂斯塔</a> / <a href="/celebrity/1326533/" rel="v:starring">麦肯兹·戴维斯</a> / <a href="/celebrity/1337333/" rel="v:starring">卡拉·朱里</a> / <a href="/celebrity/1031917/" rel="v:starring">爱德华·詹姆斯·奥莫斯</a> / <a href="/celebrity/1335066/" rel="v:starring">巴克德·阿巴蒂</a> / <a href="/celebrity/1337583/" rel="v:starring">大卫·达斯马齐连</a> / <a href="/celebrity/1036728/" rel="v:starring">西娅姆·阿巴斯</a> / <a href="/celebrity/1027381/" rel="v:starring">连尼·詹姆斯</a> / <a href="/celebrity/1057556/" rel="v:starring">马克·阿诺德</a> / <a href="/celebrity/1041118/" rel="v:starring">肖恩·杨</a></span></span><br/>
        <span class="pl">类型:</span> <span property="v:genre">剧情</span> / <span property="v:genre">动作</span> / <span property="v:genre">科幻</span> / <span property="v:genre">悬疑</span> / <span property="v:genre">惊悚</span><br/>
        <span class="pl">官方网站:</span> <a href="http://bladerunnermovie.com" rel="nofollow" target="_blank">bladerunnermovie.com</a><br/>
        <span class="pl">制片国家/地区:</span> 美国 / 英国 / 匈牙利 / 加拿大 / 西班牙<br/>
        <span class="pl">语言:</span> 英语 / 芬兰语 / 日语 / 匈牙利语 / 俄语 / 西班牙语<br/>
        <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2017-10-27(中国大陆)">2017-10-27(中国大陆)</span> / <span property="v:initialReleaseDate" content="2017-10-06(美国)">2017-10-06(美国)</span><br/>
        <span class="pl">片长:</span> <span property="v:runtime" content="163">163分钟</span> / 162分钟(中国大陆)<br/>
        <span class="pl">又名:</span> 银翼杀手2 / Blade Runner 2<br/>
        <span class="pl">IMDb链接:</span> <a href="https://www.imdb.com/title/tt1856101" target="_blank" rel="nofollow">tt1856101</a><br>

</div>
"""
html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))