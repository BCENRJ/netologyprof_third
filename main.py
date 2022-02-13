import requests
import bs4
import re
import tqdm

url = 'https://habr.com/ru/all/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/70.0.3538.77 Safari/537.36'}

# Request
response = requests.get(url=url, headers=headers)

# Soup
soup = bs4.BeautifulSoup(response.text, 'html.parser')
last_page = soup.find_all(class_="tm-articles-list__item")

# Re
my_re = (r'(\bдизайн\b|\bДизайн\b|\bДИЗАЙН\b)', r'(\bфото\b|\bФото\b|\bФОТО\b)',
         r'[^/](\bweb\b|\bWeb\b|\bWEB\b)[^/]', r'(\W[pythonPYTHON]{6}\W)')


# Checking text for words in re
def check_txt(txt: str, re_words: tuple):
    for word in re_words:
        check = re.search(word, txt)
        if check is not None:
            return True
        else:
            pass
    return False


# Looking for words within post-page
def further_post_check(link: str, user_agent: dict, re_words: tuple):
    r = requests.get(url=link, headers=user_agent)
    s = bs4.BeautifulSoup(r.text, 'html.parser')
    page = s.find(id="post-content-body").text
    return check_txt(page, re_words)


# Receiving data and presenting data in requested format
def formate_habr(page, re_words, url_headers):
    my_list = []
    with tqdm.tqdm(total=len(page)) as progress_bar:
        for elem in page:
            text = ' '.join(elem.text.split())
            main = elem.find(class_="tm-article-snippet__title tm-article-snippet__title_h2")
            link = 'https://habr.com' + main.a["href"]
            if check_txt(text, re_words) or further_post_check(link, url_headers, re_words):
                date = elem.find(class_="tm-article-snippet__datetime-published").time["title"]
                title = main.a.span.text
                my_list.extend([f'{date} - {title} - {link}'])
            progress_bar.update()
    return my_list


if __name__ == '__main__':
    print(*formate_habr(last_page, my_re, headers), sep='\n')
