import pip._vendor.requests as requests
import urllib.parse
import re
import json
from bs4 import BeautifulSoup

class LeadersScraper:
    
    def __init__(self) -> None:
        """Inicialitation of varibles with the information of thw Wikipedia weg page"""
        self.root_url = 'https://country-leaders.onrender.com'
        self.cookie_url = self.root_url + '/cookie'
        self.leaders_url = self.root_url + '/leaders'
        self.countries_url = self.root_url + '/countries'


    def get_first_paragraph(self,wikipedia_url, session):
        """
            function that receives wikipedia_url, session as parameters and returns first_paragraph
            which was validated to remove all special characters
        """
        first_paragraph = ""
        #get all the information from a URL
        req = session.get(wikipedia_url)
        #get teh HTML code from the reques
        soup = BeautifulSoup(req.content, "html")
        #find all the information with tag (p)
        paragraphs = soup.find_all('p')
        #substract the name of the leader from the URL
        full_name_leader = wikipedia_url.split('/')[-1].split('_')
        #cleans the information subtracted from the url
        name_leader = urllib.parse.unquote(full_name_leader[0])

        #iterate through the data contained in the p tag 
        for paragraph in paragraphs:
            #condition to validate if the name of the leader is in the subtracted information 
            #thus obtain the first useful paragraph
            if name_leader in str(paragraph):
                first_paragraph = paragraph
                break
        #regex to replace all the characteres useless 
        return re.sub('[^a-zA-Z0-9\(\) \.\,\:\,]','',first_paragraph.get_text())


    def get_leaders(self):
        """Function to get the information of the leader in a dictionary"""
        session = requests.Session()
        session.permanent = True
        leaders_percountry = {}

        #make the request of the cookies
        cookie = session.get(self.cookie_url).cookies       
        
        # query the /countries endpoint using the get() method and store it in the req variable 
        countries = session.get(self.countries_url, cookies=cookie).json()
        # Get the JSON content and store it in the countries variable    

        #iterate through the countrys list
        for country in countries:
            index_leader = 0 #variable to count the index in the leaders iteration 
            
            #get the dictionary with the leaders in an specefic country
            leaders_percountry[country] = [session.get(self.leaders_url, cookies=cookie,params={'country': country}).json()]

            #iterate through the leaders and get the first paragraph useful
            for leader_percountry in leaders_percountry[country][0]:
                #validation of error when the cookies expired
                if type(leader_percountry) != dict:
                    print('Error getting leader data')
                    break
                #get the first paragrahp
                text_wikipedia = self.get_first_paragraph(leader_percountry['wikipedia_url'],session)
                #insert the first paragrahp in the dictionario of leaders per country
                leaders_percountry[country][0][index_leader]['wikipedia_first_p'] = text_wikipedia
                #index increase
                index_leader += 1

        return leaders_percountry
    

    def save(self, leaders_per_country):
        """save the dictionary of leader per country in a Json File"""
        with open("leaders.json", "w") as outfile:
            json.dump(leaders_per_country, outfile)


    def load(self):
        """return a dictionary with the leader per country taked of a Json File"""
        with open("leaders.json", "r") as outfile:
            leaders_recover = json.load(outfile)
        return leaders_recover
