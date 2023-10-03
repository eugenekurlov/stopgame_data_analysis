# data on 18.09.2023
# import required libraries
import requests, re, datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS

# prepare column names for future dataframe
sgdf = pd.DataFrame(columns = ['Title', 'Genre', 'Platfrom', 'Release_date', 'Review_date', 'Comments_amount', 'Views',
                               'Author', 'Platform_played','User_score', 'Score_amount', 'Sg_score'])

# getting access to the first page of website for finding number of last page
r = requests.get('https://stopgame.ru/vreview/p1')
# read the content of page code
reviewhtml = BS(r.content, 'lxml')
# find the list of page's numbers
pagecount = reviewhtml.find_all('div', {'class':'_container_1mcqg_1'})[0]
# get the number of last page
last_page = int(re.findall('\w+',pagecount.text, re.MULTILINE)[-1])

page = 1

# calculate total time of computing
start = datetime.datetime.now()

# wrap execution code in try-except clause to handle issues with web site connection
try:
    # get access to the page
    for i in range(page, last_page+1):
        r = requests.get('https://stopgame.ru/vreview/p'+str(i))
        html = BS(r.content, 'lxml')
        link = html.find_all('a',{'class':'_card__title_givrd_1'})
        print(i)
        review_num_on_page = 1
        
        # follow the link to a video in a page
        for el in link:
            
            print(f'review № {review_num_on_page}')
            review_num_on_page += 1
            # get review title
            review = el['href']
            title = re.sub('^\s+', '', el.text)
            title = title.replace(': Видеообзор','')
            
            # follow review link
            review_url = 'https://stopgame.ru/'+review
            rr = requests.get(review_url)
            
            # get HTML content
            reviewhtml = BS(rr.content, 'lxml')
            review_info = reviewhtml.find_all('div',{'class':'_top-info_a3368_495'})
            
            # extract info about review
            for re_day in review_info:
                s = re.sub('^\s+', '', re_day.text, flags=re.MULTILINE)
                s = re.sub('\s+$', '', s, flags=re.MULTILINE)
                review_date = re.findall('^\w.+', s, re.MULTILINE)[1]
                comments = re.findall('^\w.*', s, re.MULTILINE)[2]
                views = re.findall('^\w.*', s, re.MULTILINE)[3]
                
            # get author name and console he played if exist
            author = reviewhtml.find_all('div',{'class':'_bottom-info_a3368_593'})
            if author:
                for a in author:
                    au = re.sub('^\s+', '', a.text, flags=re.MULTILINE)
                    au = re.sub('\s+$', '', au, flags=re.MULTILINE)
                    auth_name = re.findall('^\w.+', au, re.MULTILINE)[0]
                    try:
                        console = re.findall('^\w.+', au, re.MULTILINE)[1]
                        console = re.sub('Играл.? на ', '', console)
                    except IndexError:
                        console = np.NaN
            else:
                auth_name = np.NaN
                console = np.NaN
            
            # get authors' and users' scores
            scores = reviewhtml.find_all('div',{'class':'_ratings-container_99wqg_227'})
            for score in scores:
                sc = re.sub('^\s+', '', score.text, flags=re.MULTILINE)
                sc = re.sub('\s+$', '', sc, flags=re.MULTILINE)
                userScore = sc.split('\n')[0]
                scoreAmount = re.findall('^(.*)\s+\w+\s*$', sc.split('\n')[1])[0]
                scoreAmount = int(scoreAmount.replace(u'\xa0', u''))
                try:
                    authorScore = score.select('svg[class="_sg-rating_99wqg_431"]')[0].use['href']
                    authorScore = re.findall('\w+$', authorScore)[0]
                except (AttributeError, IndexError) as e:
                    authorScore = np.NaN
            game_info = reviewhtml.find_all('div', {'class':'_info-grid__value_99wqg_199'})
            game_platform = re.findall('\w+', game_info[0].text)
            genre = re.findall('\w+', game_info[1].text)[0]
            release_date = re.findall('[^\n]+', game_info[2].text.rstrip())[0]
            
            sgdf.loc[len(sgdf)] = [title, genre, game_platform, release_date, review_date, comments, views, auth_name,
                                   console, userScore, scoreAmount, authorScore]
# handling exceptions
except requests.exceptions.ConnectionError:
    print("Connection refused")
except requests.exceptions.Timeout:
    print('Maybe set up for a retry, or continue in a retry loop')
except requests.exceptions.TooManyRedirects:
    print('Tell the user their URL was bad and try a different one')
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

finish = datetime.datetime.now()
print("Total time for scraping and parsing: ", finish-start)

# save file for the more convenient use
# semicolons can be in the title, so make tabulation like separator
sgdf.to_csv('stopgame.csv', sep='\t', encoding='utf-8', index=False)
