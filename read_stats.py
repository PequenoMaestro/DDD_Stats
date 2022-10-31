from os import link
import string
import time
from datetime import datetime
import requests
from requests_html import HTMLSession

import re

import pandas as pd
import numpy as np
import plotly.express as px

def get_episodes_info(url:string):
        
    comment_count_list = []
    title_list = []
    episode_number=[]

    try:
        session = HTMLSession()
        response = session.get(url)

        links = response.html.find("a")
        links.reverse()

        for link in links:
            text = link.full_text
 
            regex_comment_count = '([0-9]+)\s*Kommentar'
            regex_title = '#\d+ – (.*)'
            regex_number ='#(\d+)'

            match_comment_count = re.findall(regex_comment_count, text)
            match_title = re.findall(regex_title, text)
            match_number = re.findall(regex_number, text)
            
            if(match_number != [] and match_comment_count != []):
                n=0
                if(match_comment_count != []):
                    n = int(match_comment_count[0])
                    # fix super high comment counts (#69)
                    if(n > 100):
                        n=0
                episode_number.append(int(match_number[0]))
                
                title="not found"
                if(match_title!=[]):
                    title = match_title[0]
                title_list.append(title)
                
                comment_count_list.append(n)

    except requests.exceptions.RequestException as e:
        print(e)

    return [comment_count_list,title_list,episode_number]
        
def get_all_month_links():
    link_list = []

    session = HTMLSession()
    response = session.get("https://www.dasdilettantischeduett.de/")
    links = response.html.find("a")
    
    for link in links:
        
        try:
            url = link.attrs['href']
            regex = '\/\d+\/\d+\/'
            match = re.findall(regex, url)
            
            if (match !=[]):
                link_list.append(url)
    
        
        except Exception as e:
            continue;

    link_list.reverse()
    return link_list




links = get_all_month_links()
all_comment_counts = []
all_titles = []
all_episode_numbers = []

for link in links:
    [counts,titles,numbers] = get_episodes_info(link)
    all_comment_counts.extend(counts)
    all_titles.extend(titles)
    all_episode_numbers.extend(numbers)

comment_counts= np.array(all_comment_counts)
print("Mean",np.mean(comment_counts))
print("Std",np.std(comment_counts))
print("Median",np.median(comment_counts))

infos = pd.DataFrame({
                     'titles': all_titles,
                     'comment_count': all_comment_counts,
                     'episode_numbers': all_episode_numbers,
                     })

infos.to_csv('episode_infos.csv')

fig = px.bar(infos,x="episode_numbers",y="comment_count",hover_data={"episode_numbers","titles","comment_count"})
fig.show()


