from translate import Translate
from urllib.parse import quote

import pandas as pd
import googletrans
import requests
import json
import time

# translator = googletrans.Translator()
translator = Translate()
# #translator = Translator(to_lang='zh')

def scrapy(kwen, st, count, api_key, total):
    xml_to_json = {'Accept': 'application/json'}

    url = f'https://api.elsevier.com/content/search/sciencedirect?query={kwen}&start={st}&count={count}&apiKey={api_key}'

    res = requests.get(url)
    raw_data = json.loads(res.text)
    print(raw_data)
    if not total:
        total = int(raw_data['search-results']['opensearch:totalResults'])

    article_count = len(raw_data['search-results']['entry'])

    article_links = []

    for item in range(article_count):
        article_links += {(raw_data['search-results']['entry'][item]['prism:url'])}

    description = []
    title = []
    href = []

    for indx, link in enumerate(article_links):
        print(f'Scrapy {indx + 1 + st} / {st + article_count}')
        url_2 = link + "?apikey=" + api_key
        result2 = requests.get(url_2, headers=xml_to_json)
        article = json.loads(result2.text)
        d_text = article["full-text-retrieval-response"]["coredata"]["dc:description"]
        t_text = article["full-text-retrieval-response"]["coredata"]["dc:title"]
        d_zh_text = translator.en2ch(d_text)
        t_zh_text = translator.en2ch(t_text)
        description.append(f'{d_zh_text} / {d_text}')
        title.append(f'{t_zh_text} / {t_text}')
        href.append(article["full-text-retrieval-response"]['coredata']['link'][-1]['@href'])
        print(f"    Title:{t_zh_text} / {t_text}")
        print(f"    Description:{d_zh_text} / {d_text}")
    df = pd.DataFrame({
        'Title': title,
        'Description': description,
        'Href': href,
    })
    df.to_csv(f'datas/{config["search"]}_data.csv', mode='a', index=False, header=False, encoding='utf-8-sig')
    print("Writing CSV...")
    total -= article_count
    st += count
    if total > 0:
        return scrapy(kwen=kwen, st=st, count=count, api_key=api_key, total=total)


if __name__ == '__main__':
    # Load configuration
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()

    # Initialize client
    kwen = quote(config['search'].encode('utf-8'))
    count = config['itemsPerPage']
    api_key = config['apikey']
    st = config['startIndex']

    scrapy(kwen=kwen, st=st, count=count, api_key=api_key, total=None)
