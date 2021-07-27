import django
django.setup()

from bs4 import BeautifulSoup
import requests
from .models import Article
from django_rq import job


urls = [
    "https://www.bbc.com/news/world",
    'https://www.euronews.com/programs/world',
    'https://www.standard.co.uk/news/world,'
]

@job('default', timeout=3600)
def parse_urls():
    newsText = []
    newsTitles = []
    newsLinks = []
    allNews = []
    newsImages = []
    fullStates = []
    euronews = {}
    euronews_links = []
    standart = {}
    standart_urls = []
    for url in urls:
        if 'bbc' in url.split('.'):
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            allNewsText = soup.find_all('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m')
            allNewsTitle = soup.find_all('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
            pictures = soup.find_all('img', class_='qa-lazyload-image lazyload lazyautosizes')
            newsUrls = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
            for news in allNewsText[0:6]:
                newsText.append(news.text)
            for news in allNewsTitle[0:6]:
                newsTitles.append(news.text)
            for url in newsUrls[0:6]:
                result_url = 'https://www.bbc.com' + url.get('href')
                newsLinks.append(result_url)
        elif 'euronews' in url.split('.'):
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            allNewsTitle = soup.find_all('a', class_='m-object__title__link')
            for i in allNewsTitle:
                euronews[i.get('title')] = {}       
                euronews[i.get('title')]['url'] = 'https://www.euronews.com/' + i.get('href')
                euronews_links.append('https://www.euronews.com/' + i.get('href'))
            allNewsText = soup.find_all('a', class_='m-object__description__link')
            for i in allNewsText:
                euronews[i.get('title')]['descr'] = i.text
        elif 'standard' in url.split('.'):
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            allNewsTitle = soup.find_all('h2', class_='sc-paWCZ enCZIG headline')
            print(allNewsTitle)
            for i in allNewsTitle:
                title = i.find('a', class_='title').text
                link = 'https://www.standard.co.uk' + i.find('a', class_='title').get('href')
                standart[title] = {}
                standart[title]['url'] = link
                standart_urls.append(url)
                
           
    for url in euronews_links:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        allNewsImages = soup.find_all('img', class_='c-article-media__img u-max-height-full')
        allTextInfo = soup.find("div", class_="c-article-content").findAll('p')
        article_text = ''
        for element in allTextInfo:
            article_text += '\n' + ''.join(element.findAll(text = True))
        for k,v in euronews.items():
            if url == v['url']:
                v['image'] = (allNewsImages[0].get('src'))
                v['article'] = (article_text)
        
    for url in standart_urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        allTextInfo = soup.find("div", class_="sc-fzokvW dlhZxU").findAll('p')
        allNewsImages = soup.find_all('img', class_='i-amphtml-fill-content i-amphtml-replaced-content')
        article_text = ''
        for element in allTextInfo:
            article_text += '\n' + ''.join(element.findAll(text = True))
        for k,v in standart.items():
            if url == v['url']:
                v['image'] = (allNewsImages[0].get('src'))
                v['article'] = (article_text)


    for url in newsLinks:
        if 'bbc' in url.split('.'):
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            allNewsText = soup.find_all('p', class_='ssrcss-1q0x1qg-Paragraph eq5iqo00')
            allNewsImages = soup.find_all('img', class_='ssrcss-1drmwog-Image ee0ct7c0')
            article = []
            for p in allNewsText:
                article.append(p.text)
            full_state = '\n'.join(article[0:-3])
            fullStates.append(full_state)
            newsImages.append(allNewsImages[0].get('src'))

    print(standart)
    for k,v in standart.items():
        if k not in [i.title for i in Article.objects.all()]:
            new_article = Article(
                title=k,
                url=v['url'],
                description=k,
                article=v['article'],
                image=v['image'],
            )
            new_article.save()


    for k,v in euronews.items():
        if k not in [i.title for i in Article.objects.all()]:
            new_article = Article(
                title=k,
                url=v['url'],
                description=k,
                article=v['article'],
                image=v['image'],
            )
            new_article.save()     

    temp = zip(newsLinks, newsText, fullStates, newsImages)
    result = dict(zip(newsTitles, temp))

    for k,v in result.items():
        if k not in [i.title for i in Article.objects.all()]:
            new_article = Article(
                title=k,
                url=v[0],
                description=v[1],
                article=v[2],
                image=v[3],
            )
            new_article.save()
