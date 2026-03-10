window.HORMUZ_FLOW_DATA = {
  "generatedAt": "2026-03-10T03:38:00Z",
  "source": {
    "name": "Windward + 第三方监测数据",
    "url": "https://windward.ai/blog/",
    "method": "Windward 日报用于历史序列；第三方监测数据用于滚动24小时补点"
  },
  "summary": {
    "latestArticleDate": "2026-03-09",
    "latestTrafficDate": "2026-03-10",
    "latestCrossings": 2.0,
    "previousTrafficDate": "2026-03-08",
    "previousCrossings": 2.0,
    "dayOverDayPct": 0.0,
    "sevenDayAverage": 60.0,
    "gapToWeekAveragePct": -96.66666666666667,
    "collapseFromStartPct": -97.97979797979798,
    "status": "通行量仍处于冻结区间",
    "latestReportDate": "2026-03-10",
    "latestReportTitle": "第三方监测数据 Realtime Dashboard",
    "latestSourceName": "第三方监测数据",
    "latestSourceUrl": "",
    "latestSourceType": "realtime",
    "latestIsRolling24h": true
  },
  "contextSignals": {
    "affectedVessels": 1650,
    "injectedZones": 44,
    "denialAreas": 92,
    "confirmedStrikes": 8
  },
  "realtimeSignals": {
    "lastUpdated": "2026-03-10T02:56:56.434Z",
    "sourceName": "第三方监测数据",
    "status": "CLOSED",
    "statusDescription": "Strait declared closed by IRGC on March 2, 2026. Iran threatening any ship attempting to pass. De-facto closure with near-zero commercial shipping traffic; only rare vessels with transponders off attempting transit. Some selective Chinese and non-Western flagged vessels occasionally passing.",
    "shipCountLast24h": 2,
    "shipCountCurrentTransits": 0,
    "shipCountNormalDaily": 60,
    "shipCountPercentOfNormal": 3.3,
    "strandedVesselsTotal": 157,
    "strandedVesselsChangeToday": 12,
    "brentPrice": 91.47,
    "brentChangePct24h": 4.36,
    "insuranceMultiplier": 6.67,
    "throughputPercentOfNormal": 1.7,
    "referenceSources": [
      "第三方监测数据"
    ]
  },
  "commodityExposure": {
    "stressPct": 96.7,
    "stressBasis": "按最新通行 2 对比 7 日均值 60 计算",
    "topRiskCommodity": "甲醇",
    "topRiskScore": 99.0,
    "note": "品种流量与全球占比为行业公开估算口径（用于监控霍尔木兹重要性），不等同于实时海关结算。",
    "referenceSources": [
      "EIA",
      "IEA",
      "IGU",
      "Argus",
      "Vortexa",
      "IAI",
      "FAO",
      "OICA"
    ],
    "items": [
      {
        "id": "methanol",
        "name": "甲醇",
        "flowValue": 2000.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 60,
        "sourceHubs": "伊朗、沙特、阿联酋",
        "majorDestinations": "中国、欧洲、东南亚",
        "riskScore": 99.0,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 1933.33,
        "estimatedAtRiskUnit": "万吨/年"
      },
      {
        "id": "crude_and_products",
        "name": "原油及成品油",
        "flowValue": 2100.0,
        "flowUnit": "万桶/日",
        "globalSeaborneSharePct": 30,
        "sourceHubs": "沙特、伊拉克、阿联酋、伊朗",
        "majorDestinations": "东亚、印度、欧洲",
        "riskScore": 99.0,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 2030.0,
        "estimatedAtRiskUnit": "万桶/日"
      },
      {
        "id": "lpg",
        "name": "液化石油气（LPG）",
        "flowValue": 5000.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 30,
        "sourceHubs": "沙特、卡塔尔、阿联酋、科威特",
        "majorDestinations": "东亚",
        "riskScore": 99.0,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 4833.33,
        "estimatedAtRiskUnit": "万吨/年"
      },
      {
        "id": "fertilizers",
        "name": "化肥（尿素及磷肥）",
        "flowValue": 1800.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 25,
        "sourceHubs": "卡塔尔、沙特、阿联酋",
        "majorDestinations": "印度、南美、美国",
        "riskScore": 98.2,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 1740.0,
        "estimatedAtRiskUnit": "万吨/年"
      },
      {
        "id": "lng",
        "name": "液化天然气（LNG）",
        "flowValue": 1100.0,
        "flowUnit": "亿立方米/年",
        "globalSeaborneSharePct": 20,
        "sourceHubs": "卡塔尔、阿联酋",
        "majorDestinations": "东亚、欧洲",
        "riskScore": 98.0,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 1063.33,
        "estimatedAtRiskUnit": "亿立方米/年"
      },
      {
        "id": "aluminum",
        "name": "铝及铝制品",
        "flowValue": 700.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 15,
        "sourceHubs": "阿联酋、卡塔尔、阿曼、巴林",
        "majorDestinations": "全球制造中心",
        "riskScore": 94.2,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 676.67,
        "estimatedAtRiskUnit": "万吨/年"
      },
      {
        "id": "autos",
        "name": "汽车（核心为进口）",
        "flowValue": 300.0,
        "flowUnit": "万辆/年",
        "globalSeaborneSharePct": 5,
        "sourceHubs": "日本、韩国、德国、中国",
        "majorDestinations": "沙特、阿联酋",
        "riskScore": 89.2,
        "riskLevel": "极高",
        "estimatedAtRiskFlow": 290.0,
        "estimatedAtRiskUnit": "万辆/年"
      }
    ]
  },
  "points": [
    {
      "trafficDate": "2026-03-01",
      "reportDate": "2026-03-01",
      "reportTitle": "48 Hours Into the Iran War: The Maritime Impact",
      "sourceUrl": "https://windward.ai/blog/48-hours-into-the-iran-war/",
      "crossings": 99,
      "exact": false,
      "note": "过去24小时过境量约为 100 艘附近，Windward 表述为“just under 100”，这里按 99 记为近似值。",
      "sevenDayAverage": null,
      "inbound": null,
      "outbound": null,
      "other": null,
      "sourceType": "windward",
      "isRolling24h": false
    },
    {
      "trafficDate": "2026-03-02",
      "reportDate": "2026-03-03",
      "reportTitle": "March 3, 2026: Iran War Maritime Intelligence Daily",
      "sourceUrl": "https://windward.ai/blog/march-3-iran-war-maritime-intelligence-daily/",
      "crossings": 7.0,
      "exact": true,
      "note": "Traffic data confirms the impact. Only seven total crossings were recorded on March 2 – three inbound, three outbound, and one additional transit – representing a 61.11% decrease from the previous day and dramatically below the 7-day moving average of 79 crossings. Commercial tan",
      "sevenDayAverage": 79.0,
      "inbound": 3,
      "outbound": 3,
      "other": 1,
      "sourceType": "windward",
      "isRolling24h": false
    },
    {
      "trafficDate": "2026-03-03",
      "reportDate": "2026-03-04",
      "reportTitle": "March 4, 2026: Iran War Maritime Intelligence Daily",
      "sourceUrl": "https://windward.ai/blog/march-4-iran-war-maritime-intelligence-daily/",
      "crossings": 4.0,
      "exact": true,
      "note": "Maritime traffic through the Strait of Hormuz declined further on March 3 as the closure declared by Iran’s Revolutionary Guards continued to deter most commercial movement through the world’s most critical energy chokepoint. Only four vessels crossed the Strait during the day, r",
      "sevenDayAverage": 77.0,
      "inbound": null,
      "outbound": null,
      "other": null,
      "sourceType": "windward",
      "isRolling24h": false
    },
    {
      "trafficDate": "2026-03-04",
      "reportDate": "2026-03-05",
      "reportTitle": "March 5, 2026: Iran War Maritime Intelligence Daily",
      "sourceUrl": "https://windward.ai/blog/march-5-iran-war-maritime-intelligence-daily/",
      "crossings": 5.0,
      "exact": true,
      "note": "Crossings through the Strait of Hormuz remained extremely limited on March 4 following the closure declared by Iran’s Revolutionary Guards . Only five vessel crossings were recorded (four inbound and one outbound), representing no change compared to the previous day and remaining",
      "sevenDayAverage": 27.0,
      "inbound": 4,
      "outbound": 1,
      "other": null,
      "sourceType": "windward",
      "isRolling24h": false
    },
    {
      "trafficDate": "2026-03-07",
      "reportDate": "2026-03-08",
      "reportTitle": "March 8, 2026: Iran War Maritime Intelligence Daily",
      "sourceUrl": "https://windward.ai/blog/march-8-maritime-intelligence-daily/",
      "crossings": 3.0,
      "exact": true,
      "note": "Strait of Hormuz Traffic Crossings through the Strait of Hormuz remained extremely limited on March 7. A total of three crossings were recorded, including one inbound and two outbound movements, representing a 25% decrease from the previous day and remaining significantly below t",
      "sevenDayAverage": 13.43,
      "inbound": 1,
      "outbound": 2,
      "other": null,
      "sourceType": "windward",
      "isRolling24h": false
    },
    {
      "trafficDate": "2026-03-08",
      "reportDate": "2026-03-09",
      "reportTitle": "March 9, 2026: Iran War Maritime Intelligence Daily",
      "sourceUrl": "https://windward.ai/blog/march-9-maritime-intelligence-daily/",
      "crossings": 2.0,
      "exact": true,
      "note": "Strait of Hormuz Traffic Transit activity through the Strait of Hormuz reached its lowest daily level since the start of the conflict. Only two crossings were recorded on March 8 , both outbound, representing a 33% decrease compared with the previous day and far below the seven-d",
      "sevenDayAverage": 5.88,
      "inbound": null,
      "outbound": null,
      "other": null,
      "sourceType": "windward",
      "isRolling24h": false
    },
    {
      "trafficDate": "2026-03-10",
      "reportDate": "2026-03-10",
      "reportTitle": "第三方监测数据 Realtime Dashboard",
      "sourceUrl": "",
      "crossings": 2.0,
      "exact": true,
      "note": "第三方监测数据显示过去24小时通行为 2，当前在途 0，常态日均约 60。",
      "sevenDayAverage": 60.0,
      "inbound": null,
      "outbound": null,
      "other": null,
      "sourceType": "realtime",
      "isRolling24h": true
    }
  ],
  "timeline": [
    {
      "trafficDate": "2026-03-01",
      "reportDate": "2026-03-01",
      "title": "99 次通行",
      "note": "过去24小时过境量约为 100 艘附近，Windward 表述为“just under 100”，这里按 99 记为近似值。",
      "sourceUrl": "https://windward.ai/blog/48-hours-into-the-iran-war/",
      "exact": false
    },
    {
      "trafficDate": "2026-03-02",
      "reportDate": "2026-03-03",
      "title": "7 次通行，对比 7 日均值 79",
      "note": "Traffic data confirms the impact. Only seven total crossings were recorded on March 2 – three inbound, three outbound, and one additional transit – representing a 61.11% decrease from the previous day and dramatically below the 7-day moving average of 79 crossings. Commercial tan",
      "sourceUrl": "https://windward.ai/blog/march-3-iran-war-maritime-intelligence-daily/",
      "exact": true
    },
    {
      "trafficDate": "2026-03-03",
      "reportDate": "2026-03-04",
      "title": "4 次通行，对比 7 日均值 77",
      "note": "Maritime traffic through the Strait of Hormuz declined further on March 3 as the closure declared by Iran’s Revolutionary Guards continued to deter most commercial movement through the world’s most critical energy chokepoint. Only four vessels crossed the Strait during the day, r",
      "sourceUrl": "https://windward.ai/blog/march-4-iran-war-maritime-intelligence-daily/",
      "exact": true
    },
    {
      "trafficDate": "2026-03-04",
      "reportDate": "2026-03-05",
      "title": "5 次通行，对比 7 日均值 27",
      "note": "Crossings through the Strait of Hormuz remained extremely limited on March 4 following the closure declared by Iran’s Revolutionary Guards . Only five vessel crossings were recorded (four inbound and one outbound), representing no change compared to the previous day and remaining",
      "sourceUrl": "https://windward.ai/blog/march-5-iran-war-maritime-intelligence-daily/",
      "exact": true
    },
    {
      "trafficDate": "2026-03-07",
      "reportDate": "2026-03-08",
      "title": "3 次通行，对比 7 日均值 13.43",
      "note": "Strait of Hormuz Traffic Crossings through the Strait of Hormuz remained extremely limited on March 7. A total of three crossings were recorded, including one inbound and two outbound movements, representing a 25% decrease from the previous day and remaining significantly below t",
      "sourceUrl": "https://windward.ai/blog/march-8-maritime-intelligence-daily/",
      "exact": true
    },
    {
      "trafficDate": "2026-03-08",
      "reportDate": "2026-03-09",
      "title": "2 次通行，对比 7 日均值 5.88",
      "note": "Strait of Hormuz Traffic Transit activity through the Strait of Hormuz reached its lowest daily level since the start of the conflict. Only two crossings were recorded on March 8 , both outbound, representing a 33% decrease compared with the previous day and far below the seven-d",
      "sourceUrl": "https://windward.ai/blog/march-9-maritime-intelligence-daily/",
      "exact": true
    },
    {
      "trafficDate": "2026-03-10",
      "reportDate": "2026-03-10",
      "title": "2 次通行，对比 7 日均值 60",
      "note": "第三方监测数据显示过去24小时通行为 2，当前在途 0，常态日均约 60。",
      "sourceUrl": "",
      "exact": true
    }
  ],
  "caveats": [
    "最新可量化点来自第三方监测数据，更新日期 2026-03-10，过去24小时通行为 2。",
    "该值是截至抓取时点的过去24小时滚动口径，不等同于自然日结算值。",
    "2026-03-01 的起始点来自 Windward 对“过去24小时”过境量的近似描述，不是完整日终结算值。"
  ]
};
