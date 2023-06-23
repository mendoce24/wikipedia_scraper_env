import pip._vendor.requests as requests
import urllib.parse
import re
import json
from bs4 import BeautifulSoup

class LeadersScraper:
    
    def __init__(self) -> None:
        self.root_url = 'https://country-leaders.onrender.com'
        self.cookie_url = self.root_url + '/cookie'
        self.leaders_url = self.root_url + '/leaders'
        self.countries_url = self.root_url + '/countries'


    def get_first_paragraph(self,wikipedia_url, session):
        """"""
        print(wikipedia_url) # keep this for the rest of the notebook
        first_paragraph = ""
        req = session.get(wikipedia_url)
        soup = BeautifulSoup(req.content, "html")
        paragraphs = soup.find_all('p')
        full_name_leader = wikipedia_url.split('/')[-1].split('_')
        name_leader = urllib.parse.unquote(full_name_leader[0])

        for paragraph in paragraphs:
                if name_leader in str(paragraph):
                    first_paragraph = paragraph
                    break
        
        return re.sub('[^a-zA-Z0-9\(\) \.\,\:\,]','',first_paragraph.get_text())


    def get_leaders(self):
        session = requests.Session()
        session.permanent = True

        cookie = session.get(self.cookie_url).cookies       
        
        # query the /countries endpoint using the get() method and store it in the req variable (1 line)
        countries = session.get(self.countries_url, cookies=cookie).json()
        # Get the JSON content and store it in the countries variable (1 line)    
        leaders_percountry = {}

        for country in countries:
            index_leader = 0
            
            leaders_percountry[country] = [session.get(self.leaders_url, cookies=cookie,params={'country': country}).json()]

            for leader_percountry in leaders_percountry[country][0]:
                if type(leader_percountry) != dict:
                    print('Error getting leader data')
                    break
                text_wikipedia = self.get_first_paragraph(leader_percountry['wikipedia_url'],session)
                leaders_percountry[country][0][index_leader]['wikipedia_first_p'] = text_wikipedia
                index_leader += 1

        return leaders_percountry
    

    def save(self, leaders_per_country):
        with open("leaders.json", "w") as outfile:
            # json_data refers to the above JSON
            json.dump(leaders_per_country, outfile)


    def load(self):
        with open("leaders.json", "r") as outfile:
            # json_data refers to the above JSON
            leaders_recover = json.load(outfile)
        return leaders_recover
