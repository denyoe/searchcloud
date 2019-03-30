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
                SearchResult(link=link, title=title, desc=description, rank=result_index, origin='SCHOLAR'))
            result_index += 1

    return result_list


def export_results(results):
    ans = '['
    for result in results:
        ans += json.dumps(result._asdict()) + ', '

    ans += ']'
    print(ans)
    return ans



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
