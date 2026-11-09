import csv, random, re
O={"Nike":"https://www.nike.com","Adidas":"https://www.adidas.it","New Balance":"https://www.newbalance.it","ASICS":"https://www.asics.com","On":"https://www.on.com","Under Armour":"https://www.underarmour.it"}
RAW={}  # (brand, category_stratum) -> list of paths, as returned by category-page extraction on 2026-10-15
RAW[("Nike","W")]="""/it/t/scarpa-da-running-su-strada-nike-pegasus-plus-2-donna-MUQZWOKx/IM2543-310
/it/t/scarpa-da-gara-su-strada-nike-alphafly-4-donna-CyIf9r63/IZ9609-002
/it/t/scarpa-da-running-su-strada-nike-vomero-18-donna-q88GZuLG/HM6804-013
/it/t/scarpa-da-running-su-strada-nike-vomero-plus-donna-hJ7172Tr/HV8154-013
/it/t/scarpa-da-running-su-strada-nike-pegasus-42-donna-VNFFbZDe/IB1881-601
/it/t/scarpa-da-running-su-strada-nike-structure-26-donna-pDzPgBr0/HJ1101-005
/it/t/scarpa-da-gara-su-strada-nike-vaporfly-4-donna-nUJzqPSE/HF6412-602
/it/t/scarpa-da-running-su-strada-nike-zoom-fly-6-donna-9xSBuBQG/FN8455-603
/it/t/scarpa-da-running-su-strada-nike-run-defy-donna-QV95N6vi/HM9593-011
/it/t/scarpa-da-running-su-strada-nike-pegasus-premium-donna-ZIEXAQjZ/HQ2593-609
/it/t/scarpa-da-running-su-strada-nike-vomero-premium-donna-zBXYg7or/HM5973-004
/it/t/scarpa-da-running-su-strada-nike-structure-plus-donna-ncoiUSp0/HQ3049-102
/it/t/scarpa-impermeabile-da-running-su-strada-nike-pegasus-42-gore-tex-donna-lk7uZHe4/IQ1085-608
/it/t/scarpa-da-running-su-strada-nike-zoom-fly-6-donna-mJT9nctg/FN8455-100
/it/t/scarpa-da-running-su-strada-nike-quest-7-donna-aQTFQj4L/IM9291-102
/it/t/scarpa-impermeabile-da-running-su-strada-con-dettagli-dal-design-rifrangente-nike-vomero-18-gore-tex-donna-QiUtOUCa/HQ7002-004
/it/t/scarpa-da-gara-su-strada-nike-alphafly-3-donna-c0BiSuME/FD8315-105""".split()
RAW[("Nike","M")]="""/it/t/scarpa-da-running-su-strada-nike-pegasus-plus-2-uomo-bVq2jMv5/IM2541-101
/it/t/scarpa-da-gara-su-strada-nike-alphafly-4-uomo-nOHkKz9h/IU4686-002
/it/t/scarpa-da-running-su-strada-nike-vomero-plus-x-distance-uomo-XtKPbubh/IQ7318-100
/it/t/scarpa-da-gara-su-strada-vaporfly-4-x-distance-uomo-2fcW64jK/IQ7316-800
/it/t/scarpa-da-running-su-strada-nike-pegasus-42-uomo-M9ckDyR3/IB1873-402
/it/t/scarpa-impermeabile-da-running-su-strada-nike-pegasus-42-gore-tex-uomo-wwNioLDU/IQ0450-005
/it/t/scarpa-da-running-su-strada-nike-vomero-18-uomo-SMtmxlKz/HM6803-005
/it/t/scarpa-da-running-su-strada-nike-vomero-plus-run-in-berlin-uomo-ZaR7ZyEh/IU5067-068
/it/t/scarpa-da-running-su-strada-nike-vomero-premium-uomo-kcNbRx8a/HQ2050-003
/it/t/scarpa-da-running-su-strada-nike-quest-7-uomo-R6dnTZx6/IM6368-004
/it/t/scarpa-da-running-su-strada-nike-run-defy-uomo-015L9V/HM9594-201
/it/t/scarpa-da-running-su-strada-nike-structure-plus-uomo-rdhfPpo2/HQ3048-501
/it/t/scarpa-impermeabile-da-running-su-strada-con-dettagli-dal-design-rifrangente-nike-vomero-18-gore-tex-uomo-qGNBxvUb/HQ7001-005
/it/t/scarpa-da-running-su-strada-nike-pegasus-42-easyon-uomo-iqy42BYW/IM4110-001
/it/t/scarpa-da-running-su-strada-nike-structure-26-larga-uomo-97Z7BI0i/HQ2588-001
/it/t/scarpa-da-running-su-strada-nike-structure-26-uomo-DyK0ML90/HJ1102-008
/it/t/scarpa-da-running-su-strada-nike-pegasus-premium-uomo-vRcGAMSK/HQ2592-021
/it/t/scarpa-da-gara-su-strada-nike-zoom-fly-6-uomo-OHkLQ2uh/FN8454-404
/it/t/scarpa-da-gara-su-strada-nike-vaporfly-4-uomo-DeKC4kdI/IM8203-001
/it/t/scarpa-da-gara-su-strada-nike-alphafly-3-run-in-berlin-uomo-KnKE5jwD/IU5065-068""".split()
RAW[("Adidas","M")]="""/scarpe-adizero-adios-pro-5/KJ7040.html /scarpa-da-running-adizero-evo-sl-lightstrikepro/LM9021.html /scarpe-da-running-hyperboost-edge/KI4392.html /scarpe-adizero-evo-sl/JH6206.html /scarpe-adizero-boston-12/JI4476.html /scarpe-da-running-supernova-rise-3/KK1206.html /scarpe-supernova-ease/IH0796.html /scarpe-da-running-supernova-glide/KJ4421.html /scarpe-da-corsa-supernova-solution-3/JR7400.html /scarpe-adizero-evo-sl-exo/KI4764.html /scarpe-adizero-avanti/IG1989.html /scarpe-da-running-duramo-sl-2/IH8215.html /scarpe-galaxy-6/GW3848.html /scarpe-da-running-pureboost-5/JI0303.html /scarpe-da-running-runfalcon-5-tr/JI4084.html /scarpe-da-running-duramo-speed-2/JQ0625.html /scarpe-da-running-galaxy-8/KI7980.html /scarpe-da-running-runfalcon-5/IE8819.html /scarpe-da-running-ultrarun-5/IH2640.html /scarpe-da-running-galaxy-7/JQ3323.html /scarpe-da-running-duramo-rc2/JS0120.html""".split()
RAW[("Adidas","W")]="""/scarpa-adizero-evo-sl-w/LM9022.html /scarpe-da-running-adizero-adios-pro-5/KI8293.html /scarpe-adizero-evo-sl-exo/KJ0435.html /scarpe-hyperboost-gtx/KK2023.html /scarpe-da-running-supernova-rise-3/JR1613.html /scarpe-da-running-supernova-glide/KJ1862.html /scarpe-da-running-supernova-solution-3/JR7396.html /supernova-glide-running-shoes/KJ6591.html /scarpe-adizero-evo-sl/JH6208.html /scarpe-adizero-boston-13/JP9249.html /scarpe-adizero-avanti/IG1989.html /scarpe-hyperboost-atr-w/IH9459.html /scarpe-adizero-boston-12/JI4473.html /scarpe-adizero-distancestar/IF9390.html /scarpe-da-running-supernova-rise-2/JQ7697.html /scarpe-adizero-adios-pro-evo-2/JR7259.html /scarpe-adizero-evo-sl-adidas-by-stella-mccartney/KI6774.html /adizero-prime-sp-4/JI1212.html /scarpe-supernova-ease/IF9564.html /scarpe-da-running-duramo-sl-2/JP9217.html /scarpe-da-corsa-duramo-rc2/JR3236.html /scarpe-galaxy-6/GW3847.html /scarpe-duramo-rc2-running/JP9200.html /scarpe-da-running-hyperboost-edge/KI4392.html""".split()
RAW[("ASICS","M")]="""/it/it-it/versablast-4/p/1011B984-005.html /it/it-it/novablast-6/p/1011C243-102.html /it/it-it/gel-pulse-17/p/1011C153-403.html /it/it-it/gel-kayano-33/p/1011C167-101.html /it/it-it/sonicblast-2/p/1011C244-100.html /it/it-it/gt-2000-15/p/1011C235-800.html /it/it-it/gel-nimbus--28/p/1011C127-102.html /it/it-it/gel-cumulus--28/p/1011C143-101.html /it/it-it/gel-excite-11/p/1011C080-405.html /it/it-it/gel-nimbus--28-wide/p/1011C144-002.html /it/it-it/noosa-tri-16/p/1011B872-404.html""".split()
RAW[("ASICS","W")]="""/it/it-it/gel-nimbus--28/p/1012B899-002.html /it/it-it/gel-nimbus-28-x-nadia-battocletti/p/1012C055-100.html /it/it-it/gel-kayano-33/p/1012B939-101.html /it/it-it/novablast-6/p/1012C008-102.html /it/it-it/sonicblast-2/p/1012C009-100.html /it/it-it/gt-2000-15/p/1012B998-700.html /it/it-it/gel-cumulus--28/p/1012B916-103.html /it/it-it/gel-pulse--17/p/1012B930-250.html /it/it-it/gel-excite-11/p/1012B861-405.html /it/it-it/versablast-4/p/1012B775-503.html /it/it-it/gel-cumulus-27-gtx/p/1012B834-020.html""".split()
RAW[("On","M")]="""cloudmonster-3-m-3mg1005/mens/rock-silver-shoes-3MG10054857 cloudboom-volt-m-3mf3098/mens/celeste-isle-shoes-3MF30985531 cloudrunner-3-m-3mg1007/mens/agave-black-shoes-3MG10075016 cloudrunner-3-m-3mg3139/mens/ivory-flame-shoes-3MG31390849 cloudrunner-3-wide-m-3mg1009/mens/ghost-verdite-shoes-3MG10095248 cloudsurfer-max-m-3mf3043/mens/saffron-squash-shoes-3MF30435168 cloud-x-tempo-m-3mg3011/mens/bark-ivory-shoes-3MG30115115 cloudrunner-3-max-ln1-m-3mg3114/mens/fresco-gild-shoes-3MG31146224 cloudrunner-3-wp-m-3mg1010/mens/pollen-haze-shoes-3MG10106044 cloudrunner-3-max-m-3mg3020/mens/white-autumn-shoes-3MG30206061 cloudsoma-m-3mf3065/mens/urchin-agave-shoes-3MF30655314 cloudsurfer-2-3mf1012/mens/ore-white-shoes-3MF10125061 cloudboom-max-m-3mf3031/mens/white-flurry-shoes-3MF30315187 cloudmonster-3-wide-m-3mg1093/mens/brook-flurry-shoes-3MG10935256 cloudmonster-void-m-3mg1091/mens/wash-brook-shoes-3MG10915206 cloudmonster-1-m-3mf3074/mens/black-shoes-3MF30740553 cloudmonster-3-hyper-3mg1006/mens/black-ivory-shoes-3MG10061430 cloudflow-5-m-3mf1011/mens/alloy-rock-shoes-3MF10113295""".split()
RAW[("On","W")]="""cloudrunner-3-max-w-3wg3016/womens/frost-verbana-shoes-3WG30165399 cloudmonster-3-w-3wg1003/womens/brook-flurry-shoes-3WG10035256 cloudmonster-3-hyper-3wg1004/womens/ivory-flurry-shoes-3WG10045262 cloudsurfer-max-w-3wf3022/womens/foxglove-ivory-shoes-3WF30225073 cloudrunner-3-w-3wg1005/womens/squash-saffron-shoes-3WG10055156 cloudrunner-3-max-ln1-w-3wg3104/womens/fresco-gild-shoes-3WG31046224 cloudrunner-3-wp-w-3wg1008/womens/pollen-haze-shoes-3WG10086044 cloudsoma-w-3wf3037/womens/urchin-agave-shoes-3WF30375314 cloudmonster-3-wide-w-3wg1083/womens/frost-ivory-shoes-3WG10835236 cloudsurfer-2-3wf1010/womens/surf-flurry-shoes-3WF10105063 cloudboom-volt-w-3wf3074/womens/celeste-isle-shoes-3WF30745531 cloudboom-max-w-3wf3018/womens/white-celeste-shoes-3WF30185109 cloudflow-5-w-3wf1009/womens/flurry-wash-shoes-3WF10094946 cloudrunner-3-wide-w-3wg1007/womens/ghost-verdite-shoes-3WG10075248""".split()
RAW[("New Balance","M")]="""/it/pd/supercomp-elite-v6/MRCELV6_RU-FTW-878314.html /it/pd/supercomp-rebel-uomo/MREBXV1_RU-FTW-814193.html /it/pd/fuelcell-rebel-v5/MFCXV5-50690-AUG0.html /it/pd/fresh-foam-x-860-v15/M860V15_RU-FTW-802888.html /it/pd/fresh-foam-x-880v15/M880V15-48603.html /it/pd/1080v15-pykrete/M1080V15_RU-FTW-829191.html /it/pd/880v15-gore-tex/M880GV15-50385.html /it/pd/fresh-foam-680-v8-waterproof/M680WV8-51326.html /it/pd/fuelcell-supercomp-elite-v5/MRCELV5-50683.html /it/pd/fresh-foam-x-860v14/M860V14-45483.html""".split()
RAW[("New Balance","W")]="""/it/pd/fresh-foam-x-more-v6/WMORV6-50400.html /it/pd/supercomp-elite-v6/WRCELV6_RU-FTW-878315.html /it/pd/supercomp-rebel-donna/WREBXV1_RU-FTW-814192.html /it/pd/fresh-foam-x-860-v15/W860V15_RU-FTW-802889.html /it/pd/1080v15-pykrete/W1080V15_RU-FTW-829189.html /it/pd/fuelcell-rebel-v5/WFCXV5_RU-FTW-838114.html /it/pd/fresh-foam-x-880v15/W880V15-48604-AUG0.html /it/pd/880v15-gore-tex/W880GV15-50386.html /it/pd/fuelcell-propel-v5/WFCPRV5-49424.html /it/pd/fresh-foam-680-v8-waterproof/W680WV8-51327.html /it/pd/fresh-foam-arishi-v4/WARISV4-51303.html /it/pd/fuelcell-supercomp-trainer-v3/WRCXV4-50692.html /it/pd/fuelcell-rebel-v4/WFCXV4-50666.html""".split()
RAW[("Under Armour","M")]="""/it-it/p/ua-velociti-distance-storm/6013477.html /it-it/p/ua-charged%2B-chase/6014417.html /it-it/p/ua-turbulence-3/6006717.html /it-it/p/ua-charged%2B-assert-11/6006723.html /it-it/p/ua-hb-runner-2/6010212.html /it-it/p/ua-surge-5/6010459.html /it-it/p/ua-turbulence-3-storm/6017378.html /it-it/p/ua-halo-racer-2/6010214.html /it-it/p/ua-velociti-pace/6009107.html /it-it/p/ua-hb-runner-se-2/6013478.html /it-it/p/ua-velociti-elite-3-sharon-lokedi-pe/6005377.html /it-it/p/ua-surge-4/3027000.html /it-it/p/ua-infinite/3027523.html /it-it/p/ua-rogue-5/3028256.html /it-it/p/ua-velociti-spd/6000007.html /it-it/p/ua-pursuit-4-big-logo/6000597.html /it-it/p/ua-velociti-pro-2/6005378.html /it-it/p/ua-velociti-distance/6006030.html /it-it/p/ua-rogue-6/6006719.html /it-it/p/ua-halo-racer/6007639.html /it-it/p/ua-halo-runner-se/6008994.html /it-it/p/ua-halo-runner/6013164.html""".split()
RAW[("Under Armour","W")]="""/it-it/p/ua-charged%2B-assert-11/6006724.html /it-it/p/ua-rogue-6/6006720.html /it-it/p/ua-charged%2B-chase/6014418.html /it-it/p/ua-surge-5/6010460.html /it-it/p/ua-turbulence-3/6006718.html /it-it/p/ua-velociti-distance/6006031.html /it-it/p/ua-halo-racer-2/6010216.html /it-it/p/ua-velociti-pace/6009108.html /it-it/p/ua-hb-runner-2/6010213.html /it-it/p/ua-velociti-spd/6000017.html /it-it/p/ua-infinite/3027524.html /it-it/p/ua-rogue-5/3028262.html /it-it/p/ua-infinite-elite-2/3028178.html /it-it/p/ua-surge-4/3027007.html /it-it/p/ua-halo-racer/6007641.html /it-it/p/ua-pursuit-4/3028261.html /it-it/p/ua-halo-runner/6013165.html /it-it/p/ua-pursuit-4-big-logo/6000598.html /it-it/p/ua-velociti-distance-storm/6013477.html /it-it/p/ua-velociti-elite-3-sharon-lokedi-pe/6005377.html /it-it/p/ua-velociti-pro-2/6005378.html""".split()

def url(b,p):
    if b=="On": return O[b]+"/it-it/products/"+p
    return O[b]+p
def code(b,p): return re.sub(r"\.html$","",p.rstrip("/").split("/")[-1]) if b!="On" else p.split("-")[-1]
rows=[]; 
for b in O:
    cm={code(b,p):p for p in RAW[(b,"M")]}; cw={code(b,p) for p in RAW[(b,"W")]}
    for s in "MW":
        for p in RAW[(b,s)]:
            c=code(b,p); st="eligible"; why=""
            if b in("Adidas","Under Armour") and c in (cw if s=="M" else set(cm)): st="excluded"; why="same product code listed in both men and women categories (unisex)"
            rows.append(dict(brand=b,stratum=s,product_code=c,url=url(b,p),frame_status=st,reason=why))
# Adidas duplicate-model dedupe (same model, different slugs/codes)
def norm(b,u):
    s=u.split("/")[3] if b=="Adidas" else ""
    for t in ("scarpe","scarpa","da","running","corsa","shoes","w","adidas"): s="-".join(x for x in s.split("-") if x!=t)
    return s
seen=set()
for r in rows:
    if r["brand"]=="Adidas" and r["frame_status"]=="eligible":
        k=(r["stratum"],norm("Adidas",r["url"]))
        if k in seen: r["frame_status"]="excluded"; r["reason"]="duplicate model (same model, different slug/colour)"
        seen.add(k)
with open("frame_manifest.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# seeded sample
rng=random.Random(20261015); sample=[]
for b in O:
    for s in "MW":
        el=sorted([r for r in rows if r["brand"]==b and r["stratum"]==s and r["frame_status"]=="eligible"],key=lambda r:r["url"])
        k=min(10,len(el)); ch=rng.sample(el,k)
        print(b,s,"eligible",len(el),"sampled",k)
        sample+=ch
with open("sample_manifest.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["brand","url","gender_stratum"]); w.writeheader()
    for r in sample: w.writerow(dict(brand=r["brand"],url=r["url"],gender_stratum=r["stratum"]))
print(len(sample))
