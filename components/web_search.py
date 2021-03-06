import streamlit as st
import nltk
nltk.download('punkt')

from newspaper import Article

from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup
import requests

def get_links(user_search):
    root = "https://www.google.com/"
    search_engine_string = 'search?q='
    search_engine_other_half = '&sxsrf=AOaemvIiKfd8dkMCkRXEhoZm3rjXFGMzCQ:1631931499445&source=lnms&tbm=nws&sa=X&ved=2ahUKEwikm8nKuofzAhUPElkFHVshBFUQ_AUoAnoECAEQBA&biw=1295&bih=697&dpr=2'
    link = root + search_engine_string + user_search + search_engine_other_half
    lst = []
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'lxml')
        for item in soup.find_all('div', attrs={'class':'kCrYT'}):
            try:
                try:
                    raw_link = (item.find('a', href=True)['href'])
                    link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
                    if not link in lst:
                        lst.append(link)
                    else:
                        pass
                except IndexError:
                    break
            except TypeError:
                pass
    return lst

def fetch_text_data(input_url):
    article = Article(input_url) 

    article.download()
    article.parse()
    article.nlp()
    print('\nTitle\n', article.title)
    print('\nSUMMARY\n', article.summary)
    print('\nKEYWORDS\n', article.keywords)
    return article

def app():
    st.markdown('## Article Summary via Search')

    st.write('Search the web for articles and output summaries')

    search_item = str(st.text_input('Enter Search Term(s)'))
    search_item = search_item.replace(' ', '')
    
    if (st.button('Search') and search_item != ''):
        links = get_links(search_item)

        link1 = str(links[0])
        link2 = str(links[1])

        other_links = links[2:]

        with st.empty():
            for i in range(1):
                st.caption('Evaluating...')
                processed_article1 = fetch_text_data(link1)
                processed_article2 = fetch_text_data(link2)
            st.caption('Done!')
        st.write('**Primary Article**')
        st.write('`Title: `', processed_article1.title)
        st.write('`URL: `', link1)
        st.write('`AI Generated Summary: `', processed_article1.summary)

        st.markdown('---')

        st.write('**Secondary Article**')
        st.write('`Title: `', processed_article2.title)
        st.write('`URL: `', link2)
        st.write('`AI Generated Summary: `', processed_article2.summary)

        st.markdown('---')
        st.write('**Related Articles**')
        for i in other_links:
            st.markdown(f'- {i}')