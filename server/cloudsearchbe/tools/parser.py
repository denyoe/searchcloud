import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import json
import itertools

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

SearchResult = namedtuple("SearchResult", "link title desc rank origin")


# Function to use in the web API
def google_to_json(query):
    """ Return most relevant websites given keywords, using google search. As a list of jsons
    :param request:
    :return:
    """
    return json.loads(export_results(google_search(query)))


def google_search(query):
    html = google_fetch_results(query, 5)
    return google_parse_results(html)


def google_fetch_results(query, number_results):
    query = query.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl=en'.format(query, number_results)
    response = requests.get(google_url, headers=USER_AGENT)
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
    scholar_url = 'https://scholar.google.com/scholar?q={}&num={}&hl=en'.format(query, number_results)
    response = requests.get(scholar_url, headers=USER_AGENT)
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
    youtube_url = 'https://www.youtube.com/results?search_query={}'.format(query)
    response = requests.get(youtube_url)
    response.raise_for_status()

    return response.text


def youtube_parse_results(html, number_results):
    soup = BeautifulSoup(html, 'html.parser')

    result_list = []
    result_index = 1
    result_html_set = soup.find_all('div', attrs={'class': 'yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix'})
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
    return ans


"""------------ 2nd version for query to results. More general --------------"""

se_url_stems = {
    "google": 'https://www.google.com/search?q={}&num={}&hl=en',
    "youtube": 'https://www.youtube.com/results?search_query={}',
    "google_scholar": 'https://scholar.google.com/scholar?q={}&num={}&hl=en',
    "google_images": 'https://www.google.com/search?tbm=isch&source=lnms&q={}',
    "google_maps": "https://www.google.fr/maps/dir//"
}


def se_parse_results(se, html):
    result_list = []
    result_index = 1

    """Big specificity: google images"""
    if se == "google_images":
        number_results = 5
        soup = BeautifulSoup(html, 'html.parser')
        result_html_set = soup.find_all('div', attrs={'class': 'rg_meta'})
        metadata_dicts = (json.loads(e.text) for e in result_html_set)
        link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
        images = itertools.islice(link_type_records, number_results)
        for i, (url, image_type) in enumerate(images):
            result_list.append(SearchResult(link=url, title='', desc='', rank=result_index, origin='IMAGE'))
            result_index += 1
    else:
        """1/ Specificities"""
        soup_class = ''
        result_class = ''
        origin = ''
        span_or_div = 'div'
        if se == "google_scholar":
            soup_class = 'gs_r gs_or gs_scl'
            result_class = "gs_rs"
            origin = 'SCHOLAR'
        elif se == "google":
            soup_class = 'g'
            result_class = "st"
            origin = 'GOOGLE'
            span_or_div = 'span'
        elif se == "youtube":
            soup_class = 'yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix'
            result_class = "yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"
            origin = 'YOUTUBE'
        else:  # But no time for google_maps and so
            soup_class = 'g'
            result_class = "st"
            origin = 'GOOGLE'
        print('soup_class:', soup_class)
        """2/ Generalities"""
        soup = BeautifulSoup(html, 'html.parser')
        result_html_set = soup.find_all('div', attrs={'class': soup_class})
        for result_html in result_html_set:
            link = result_html.find('a', href=True)
            title = result_html.find('h3')
            description = result_html.find(span_or_div, attrs={'class': result_class})
            if link and title and description:
                link = link['href']
                title = title.get_text()
                description = description.get_text()
                result_list.append(
                    SearchResult(link=link, title=title, desc=description, rank=result_index, origin=origin))
                result_index += 1
    return result_list


def se_to_json(se, query):
    """
    :param se: Search Engine name
    :param query: 1 query term
    :return: a list of jsons which are the websites info
    """
    print("query:", query)
    query = query.replace(' ', '+') # there may be composed words, eg 'Persona 4'
    nb_results = 5
    #print("se_url_stems[se]:", se_url_stems[se])
    response = requests.get(se_url_stems[se].format(query,nb_results))
    response.raise_for_status()
    html = response.text
    parsed = se_parse_results(se, html)
    print("parsed:", parsed)
    json_res = json.loads(export_results(parsed))
    return json_res


def keep_wiki_links(el_result_google):
    """
    :param el_result_google: a list of link info
    :return: a similar array with only the wikipedia links
    """
    el_result_wiki = []
    for ln in el_result_google:
        if "wikipedia" in ln['link']:
            el_result_wiki.append(ln)
    return el_result_wiki


def get_search_fetch(keywords):
    """
    :param keywords: a list of keywords.
    :return:
    """
    result = []
    for el in keywords:
        el_result = se_to_json("google_images", el["keyword"])
        el_result += se_to_json("google", el["keyword"])
        el_result += se_to_json("google_maps", el["keyword"])
        el_result += se_to_json("google_scholar", el["keyword"])
        result.append({"keyword": el["keyword"], "links": el_result})
    return result


def get_search_fetch_by_types(keywords_with_type):
    """
    :param keywords_with_type: a list of jsons. One json = {'keyword': 'kw1', 'type': 'person'}
    :return:
    """
    print("keywords_with_type:", keywords_with_type)
    result = []
    for el in keywords_with_type:
        if el["type"].lower() == "person":
            el_result = se_to_json("google_images", el["keyword"])
            el_result_google = se_to_json("google", el["keyword"])
            el_result += keep_wiki_links(el_result_google)
        elif el["type"].lower() == "place":
            el_result = se_to_json("google_maps", el["keyword"])
            el_result_google = se_to_json("google", el["keyword"])
            el_result += keep_wiki_links(el_result_google)
        else:
            el_result = se_to_json("google", el["keyword"])
            el_result += se_to_json("google_scholar", el["keyword"])
            se_to_json("google_images", el["keyword"])
        result.append({"keyword": el["keyword"], "links":el_result})
    return result






if __name__ == '__main__':
    google_results = google_search('denis trystram publication google scholar')
    for result in google_results:
        print(result)
        print('-------')

    scholar_results = scholar_search('natural language processing')
    export_results(scholar_results)
    for result in scholar_results:
        print(result)
        print('-------')

    youtube_results = youtube_search('natural language processing')
    export_results(youtube_results)
    for result in youtube_results:
        print(result)
        print('-------')
		

# New PART IMAGES



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
# New PART IMAGES
