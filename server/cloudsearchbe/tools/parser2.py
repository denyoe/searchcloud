import itertools

import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import json

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

SearchResult = namedtuple("SearchResult", "link title desc rank origin")


# Function to use in the web API
def google_to_json(query):
    return export_results(google_search(query))


def google_search(query):
    html = google_fetch_results(query, 5)
    return google_parse_results(html)


def google_fetch_results(query, number_results):
    query = query.replace(' ', '+')

    url = 'https://www.google.com/search?q={}&num={}&hl=en'.format(query, number_results)
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()

    return response.text


def google_parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')

    result_list = []
    result_index = 1
    result_html_set = soup.find_all('div', attrs={'class': 'g'})
    for result_html in result_html_set:
        link = result_html.find('a', href=True)
        title = result_html.find('h3')
        description = result_html.find('span', attrs={'class': 'st'})
        if link and title and description:
            link = link['href']
            title = title.get_text()
            description = description.get_text()
            result_list.append(
                SearchResult(link=link, title=title, desc=description, rank=result_index, origin='GOOGLE'))
            result_index += 1
    return result_list


def scholar_to_json(query):
    return export_results(scholar_search(query))


def scholar_search(query):
    html = scholar_fetch_results(query, 5)
    return scholar_parse_results(html)


def scholar_fetch_results(query, number_results):
    query = query.replace(' ', '+')
    url = 'https://scholar.google.com/scholar?q={}&num={}&hl=en'.format(query, number_results)
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()

    return response.text


def scholar_parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')

    result_list = []
    result_index = 1
    result_html_set = soup.find_all('div', attrs={'class': 'gs_r gs_or gs_scl'})
    for result_html in result_html_set:
        link = result_html.find('a', href=True)
        title = result_html.find('h3')
        description = result_html.find('div', attrs={'class': 'gs_rs'})
        if link and title and description:
            link = link['href']
            title = title.get_text()
            description = description.get_text()
            result_list.append(
                SearchResult(link=link, title=title, desc=description, rank=result_index, origin='SCHOLAR'))
            result_index += 1
    return result_list


def youtube_to_json(query):
    return export_results(youtube_search(query))


def youtube_search(query):
    html = youtube_fetch_results(query)
    return youtube_parse_results(html, 5)


def youtube_fetch_results(query):
    query = query.replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query={}'.format(query)
    response = requests.get(url)
    response.raise_for_status()

    return response.text


def youtube_parse_results(html, number_results):
    soup = BeautifulSoup(html, 'html.parser')

    result_list = []
    result_index = 1
    result_html_set = soup.find_all('div',
                                    attrs={'class': 'yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix'})
    # Choosing first n results
    result_html_set = result_html_set[:number_results]
    for result_html in result_html_set:
        link = result_html.find('a', href=True)
        title = result_html.find('h3')
        description = result_html.find('div', attrs={'class': 'yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2'})
        if link and title and description:
            link = 'https://www.youtube.com' + link['href']
            title = title.get_text()
            description = description.get_text()
            result_list.append(
                SearchResult(link=link, title=title, desc=description, rank=result_index, origin='YOUTUBE'))
            result_index += 1

    return result_list


def image_to_json(query):
    return export_results(image_search(query))


def image_search(query):
    html = image_fetch_results(query)
    return image_parse_results(html, 5)


def image_fetch_results(query):
    query = query.replace(' ', '+')
    url = 'https://www.google.com/search?tbm=isch&source=lnms&q={}'.format(query)
    # url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()

    return response.text


def image_parse_results(html, number_results):
    soup = BeautifulSoup(html, 'html.parser')

    result_list = []
    result_index = 1
    result_html_set = soup.find_all('div', attrs={'class': 'rg_meta'})

    metadata_dicts = (json.loads(e.text) for e in result_html_set)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    images = itertools.islice(link_type_records, number_results)
    for i, (url, image_type) in enumerate(images):
        result_list.append(SearchResult(link=url, title='', desc='', rank=result_index, origin='IMAGE'))
        result_index += 1

    return result_list


def export_results(results):
    ans = '['
    length = len(results)
    inc = 1

    for result in results:
        if length == inc:
            ans += json.dumps(result._asdict())
        else:
            ans += json.dumps(result._asdict()) + ', '

        inc += 1

    ans += ']'
    print(ans)
    return ans


def get_search_fetch(keywords):
    keywords = keywords[0]
    ans = '['

    google_results = google_search(keywords)
    for result in google_results:
        ans += json.dumps(result._asdict()) + ', '

    scholar_results = scholar_search(keywords)
    for result in scholar_results:
        ans += json.dumps(result._asdict()) + ', '

    youtube_results = youtube_search(keywords)
    for i, result in enumerate(youtube_results):
        if i == 4:
            ans += json.dumps(result._asdict())
        else:
            ans += json.dumps(result._asdict()) + ', '
    ans += ']'
    return ans

# def get_search_fetch(keywords):
#     """
#     :param keywords: a list of keywords.
#     :return:
#     """
#     result = []
#     for el in keywords:
#         el_result = se_to_json("google_images", el["keyword"])
#         el_result += se_to_json("google", el["keyword"])
#         el_result += se_to_json("google_maps", el["keyword"])
#         el_result += se_to_json("google_scholar", el["keyword"])
#         #el_result += se_to_json("youtube", el["keyword"]) # link doesn't work, nor nb requests
#         result.append({"keyword": el["keyword"], "links": el_result})
#     return result



# def get_search_fetch(keywords):
#     keywords = keywords[0]
#     ans = '{"content":"' + str(keywords) + '", "links": ['
#
#     google_results = google_search(keywords)
#     for result in google_results:
#         ans += json.dumps(result._asdict()) + ', '
#
#     scholar_results = scholar_search(keywords)
#     for result in scholar_results:
#         ans += json.dumps(result._asdict()) + ', '
#
#     youtube_results = youtube_search(keywords)
#     for i, result in enumerate(youtube_results):
#         if i == 4:
#             ans += json.dumps(result._asdict())
#         else:
#             ans += json.dumps(result._asdict()) + ', '
#     ans += ']}'
#     return ans