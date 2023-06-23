from leaders_scraper import LeadersScraper

new_leaders_scraper =  LeadersScraper()

leaders = new_leaders_scraper.get_leaders()
new_leaders_scraper.save(leaders)