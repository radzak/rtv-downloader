javascript:(function () {
    if (location.href.match(/^http[s]?:\/\/vod\.pl\//)) {
        m = dataLayer[0].mvpID;
        url = "aHR0cHM6Ly9wbGF5ZXItYXBpLmRyZWFtbGFiLnBsLz9ib2R5W2lkXT0rbSsmYm9keVtqc29ucnBjXT0yLjAmYm9keVttZXRob2RdPWdldF9hc3NldF9kZXRhaWwmYm9keVtwYXJhbXNdW0lEX1B1Ymxpa2FjamldPSttKyZib2R5W3BhcmFtc11bU2VydmljZV09dm9kLm9uZXQucGwmY29udGVudC10eXBlPWFwcGxpY2F0aW9uL2pzb25wJngtb25ldC1hcHA9cGxheWVyLmZyb250Lm9uZXRhcGkucGwmY2FsbGJhY2s9";
        url = (atob(url)).replace(/\+m\+/g, m);
        xhr = new XMLHttpRequest();
        xhr.open('GET', url, false);
        xhr.send(null);
        v = JSON.parse(xhr.responseText);
        vc = v.result[0].formats.wideo.mp4;
        title = v.result[0].meta.title;
        if (!vc) {
            alert('materia\u0142 z drm');
            return;
        }
        ;
        for (var i = -1, cc = [], dd = [], l = vc.length >>> 0; ++i !== l; null) {
            dd[i] = cc[i] = vc[i].video_bitrate;
        }
        ;
        dd.sort(function (a, b) {
            return b - a;
        });
        myWindow = window.open("", "MsgWindow");
        myWindow.document.write("<p>Tytuł: " + title + "</p>");
        for (var j = 0, len = dd.length; j < len; j = j + 1) {
            dlurl = vc[cc.indexOf(dd[j])].url;
            bitrate = vc[cc.indexOf(dd[j])].video_bitrate;
            vertical_resolution = vc[cc.indexOf(dd[j])].vertical_resolution;
            myWindow.document.write("<p>Bitrate: " + bitrate + " - Rozdzielczość pionowa: " + vertical_resolution + "</p>");
            myWindow.document.write("<p>Link do materiału: " + dlurl + "</p>");
        }
        ;
    } else if (location.href.match(/^http[s]?:\/\/vod\.tvp\.pl\/[\d]{0,8}/)) {
        i = document.body.innerHTML;
        m = i.match(/object_id=([\d]{0,8})/);
        i = document.querySelector('.movieWrapper').querySelector('iframe').contentWindow.document.head.innerHTML;
        st = i.match(/\{name: \x22SeriesTitle\x22\, value: \x22(.*)\x22\},/)[1];
        tt = i.match(/\{name: \x22Title\x22\, value: \x22(.*)\x22\},/)[1];
        title = st + " - " + tt;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open('GET', 'https://www.tvp.pl/shared/cdn/tokenizer_v2.php?object_id=' + m[1], false);
        xmlhttp.send();
        o = JSON.parse(xmlhttp.responseText);
        v = o.formats;
        for (var i = -1, vc = [], l = v.length >>> 0; ++i !== l; null) {
            if (v[i].adaptive == false) {
                vc.push(v[i]);
            }
            ;
        }
        ;
        if (vc.length == 0) {
            alert('materia\u0142 z drm');
            return;
        }
        ;
        for (var i = -1, cc = [], dd = [], l = vc.length >>> 0; ++i !== l; null) {
            dd[i] = cc[i] = vc[i].totalBitrate;
        }
        ;
        dd.sort(function (a, b) {
            return b - a;
        });
        myWindow = window.open("", "MsgWindow");
        myWindow.document.write("<p>Tytuł: " + title + "</p>");
        for (var j = 0, len = dd.length; j < len; j = j + 1) {
            dlurl = vc[cc.indexOf(dd[j])].url;
            bitrate = vc[cc.indexOf(dd[j])].totalBitrate;
            myWindow.document.write("<p>Bitrate: " + bitrate + "</p>");
            myWindow.document.write("<p>Link do materiału: " + dlurl + "</p>");
        }
        ;
    } else if (location.href.match(/^http[s]?:\/\/(?:w{3}\.)?(?:tvn)?player\.pl\//)) {
        try {
            n = document.querySelector("#detailEpisode").getAttribute("data-article-id");
            xmlhttp = new % 20
            XMLHttpRequest();
            xmlhttp.open("GET", "/api/?platform=ConnectedTV&terminal=Panasonic&format=json&authKey=064fda5ab26dc1dd936f5c6e84b7d3c2&v=3.1&m=getItem&id=" + n, false);
            xmlhttp.send();
            o = JSON.parse(xmlhttp.responseText);
            lt = o.item.videos.main.video_content_license_type;
            dd = o.item.videos.main.video_content;
            title = o.item.serie_title + "%20-%20S" + o.item.season + "E" + o.item.episode;
            if (lt !== null) {
                alert('materia\u0142%20z%20drm');
                return;
            }
            ;
            myWindow = window.open("", "MsgWindow");
            myWindow.document.write("<p>Tytu%C5%82:%20" + title + "</p>");
            for (var %20
            j = 0, len = dd.length;
            j < len;
            j = j + 1
        )
            {
                dlurl = dd[j].url;
                pn = dd[j].profile_name;
                myWindow.document.write("<p>Jako%C5%9B%C4%87%20materia%C5%82u:%20" + pn + "</p>");
                myWindow.document.write("<p>Link%20do%20materia%C5%82u:%20" + dlurl + "</p>");
            }
        } catch (e) {
        }
        ;
    } else%
    20
    if (location.href.match(/^http[s]?:\/\/www\.ipla\.tv\//)) {
        mid = document.querySelector("#vod-player").getAttribute("data-vod-json");
        idn = JSON.parse(mid).mid;
        document.location.href = 'http://getmedia.redefine.pl/vods/get_vod/?cpid=1&ua=mipla_ios/122&media_id=' + idn;
    } else%
    20
    if (location.href.match(/^http[s]?:\/\/getmedia\.redefine\.pl\//)) {
        nn = document.querySelector("pre").textContent;
        v = JSON.parse(nn);
        if (v.vod.drm == true) {
            alert('materia\u0142%20z%20drm');
            return;
        }
        ;
        vc = v.vod.copies;
        title = v.vod.title;
        for (var %20
        i = -1, cc = [], dd = [], l = vc.length >>> 0;
        ++i !== l;
        null
    )
        {
            dd[i] = cc[i] = vc[i].bitrate;
        }
        ;
        dd.sort(function (a, b) {
            return
            %
            20
            b - a;
        });
        myWindow = window.open("", "MsgWindow");
        myWindow.document.write("<p>Tytu%C5%82:%20" + title + "</p>");
        for (var %20
        j = 0, len = dd.length;
        j < len;
        j = j + 1
    )
        {
            dlurl = vc[cc.indexOf(dd[j])].url;
            bitrate = vc[cc.indexOf(dd[j])].bitrate;
            quality_p = vc[cc.indexOf(dd[j])].quality_p;
            myWindow.document.write("<p>Bitrate:%20" + bitrate + "%20-%20Rozdzielczo%C5%9B%C4%87%20pionowa:%20" + quality_p + "</p>");
            myWindow.document.write("<p>Link%20do%20materia%C5%82u:%20" + dlurl + "</p>");
        }
        ;
    } else%
    20
    if (location.href.match(/^http[s]?:\/\/(?:w{3}\.)?(?:eska|eskago|fokus|nowa)\.(?:tv|pl)\//)) {
        for (const %20
        script % 20
        of % 20
        document.querySelectorAll('script')
    )
        {
            if (script.textContent.includes("episodeId")) {
                i = script.textContent;
            }
        }
        ;
        if (i.match(/languagesList.*[;,]\s/)) {
            l = 10
        } else {
            l = 0
        }
        ;
        title = i.match(/(?:programName|title)[\s:=]+['"]?([^"']*)['"]?[;,]\s/)[1];
        url = "http://bazavod.eska.pl/playlist.m3u8?i=" + i.match(/episodeId[\s:=]+['"]?([^"';,]*)['"]?[;,]\s/)[1] + "&t=hls&l=" + l;
        title = title.replace(/(\?)/g, "_").replace(/(\?|\*|\")/g, "%27").replace(/(\/|\\|\:)/g, "%20-%20").replace(/(\')/g, "`");
        prefix = "d:\\";
        xhr = new % 20
        XMLHttpRequest();
        xhr.open('GET', url, false);
        xhr.send(null);
        nn = xhr.responseText;
        vc = nn.match(/#EXT-X-STREAM-INF.*\s.*/g);
        for (var %20
        i = -1, cc = [], dd = [], l = vc.length >>> 0;
        ++i !== l;
        null
    )
        {
            dd[i] = cc[i] = vc[i].match(/BANDWIDTH=(\d+),/)[1];
        }
        ;
        dd.sort(function (a, b) {
            return
            %
            20
            b - a;
        });
        myWindow = window.open("", "MsgWindow");
        myWindow.document.write("<p>Tytu%C5%82:%20" + title + "</p>");
        for (var %20
        j = 0, len = dd.length;
        j < len;
        j = j + 1
    )
        {
            dlurl = vc[cc.indexOf(dd[j])].match(/(http:\/\/.*)/)[1];
            bitrate = vc[cc.indexOf(dd[j])].match(/BANDWIDTH=(\d+),/)[1];
            quality_p = vc[cc.indexOf(dd[j])].match(/NAME="(.+)"/)[1];
            res = vc[cc.indexOf(dd[j])].match(/RESOLUTION=(\w+),/)[1];
            myWindow.document.write("<p>Jako%C5%9B%C4%87:%20" + quality_p + "%20-%20Bitrate:%20" + bitrate + "%20-%20Rozdzielczo%C5%9B%C4%87:%20" + res + "</p>");
            myWindow.document.write("<p>Link%20do%20materia%C5%82u:%20" + dlurl + "</p>");
        }
        ;
    }
})()