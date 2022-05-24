import pandas as pd
import googletrans
import requests
import json

from urllib.parse import quote

translator = googletrans.Translator()


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
    creator = []
    href = []

    for indx, link in enumerate(article_links):
        print(f'Scrapy {indx + 1 + st} / {st + article_count}')
        url_2 = link + "?apikey=" + api_key
        result2 = requests.get(url_2, headers=xml_to_json)
        article = json.loads(result2.text)
        d_text = article["full-text-retrieval-response"]["coredata"]["dc:description"]
        t_text = article["full-text-retrieval-response"]["coredata"]["dc:title"]
        d_zh_text = translator.translate(d_text, dest='zh-tw').text
        t_zh_text = translator.translate(t_text, dest='zh-tw').text
        description.append(f'{d_text} / {d_zh_text}')
        title.append(f'{t_text} / {t_zh_text}')
        href.append(article["full-text-retrieval-response"]['coredata']['link'][-1]['@href'])

    df = pd.DataFrame({
        'Title': title,
        'Description': description,
        'Href': href,
    })
    df.to_csv('datas/data.csv', mode='a', index=False, header=False, encoding='utf_8')
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
