# SDOL 爬蟲

----

## 主要功能

從SDOL上爬取論文資訊，並翻譯成中文：
主要爬取以下資訊，更多資訊可以參閱[ScienceDirect API](https://www.elsevier.com/solutions/sciencedirect/librarian-resource-center/api)
1. 標題
2. 摘要
3. 論文連結

爬取結束會產生CSV檔案供後續使用

----
## 使用
1. 申請API KEY，參閱[ScienceDirect API](https://www.elsevier.com/solutions/sciencedirect/librarian-resource-center/api)
2. 修改config.json
```
{
    "apikey": "API KEY",
    "search": "KeyWords",
    "startIndex": 0,
    "itemsPerPage": 5
}
```

