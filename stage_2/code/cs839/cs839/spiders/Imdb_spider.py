import scrapy
from collections import OrderedDict

class ImdbSpider(scrapy.Spider):
    name = 'imdb'

    def start_requests(self):

        start_year = 2018
        start_month = 1
        end_month = 12
        start_date = 1
        end_date = 31

        for i in range(0, 100):
            #filter range of one year
            filter_date_range = str(start_year)+"-"+str(start_month)+"-"+str(start_date)+","+str(start_year)+"-"+str(end_month)+"-"+str(end_date)

            #filter for movies
            filter_type = "feature"

            #filter count of movies in each year
            filter_count = 30

            base_url = "https://www.imdb.com/search/title"
            request_params = "?title_type="+filter_type+"&release_date="+filter_date_range+"&sort=num_votes,desc&count="+str(filter_count)
            start_url = base_url + request_params

            #start_url = "https://www.imdb.com/search/title?title_type=feature&release_date=2017-01-01,2017-12-31&sort=num_votes,desc&count=30"
            yield scrapy.Request(url= start_url, callback= self.parse)
            
            start_year-= 1

    #function that parses the page containing list of movies and performs a crawl over each movie
    def parse(self, response):

        movie_urls = response.css('h3.lister-item-header a::attr(href)').getall()

        for movie_url in movie_urls:
            yield response.follow(movie_url, self.parse_movie)


    def parse_movie(self, response):
        # now in info page
        title_class = response.css('div.title_wrapper')

        # schema name
        title = title_class.css('h1::text').get().strip()

        # schema certificate
        certificate = title_class.css('div.subtext::text').get().strip()

        # schema genre
        genre_tags = title_class.css('div.subtext a')[:-1]

        genre_list = []
        for i, genre_tag in enumerate(genre_tags):
            genre_list.append(genre_tags[i].css('a::text').get().strip())

        genre_string = ", ".join(genre_list)

        # schema release_date
        release_tag = title_class.css('div.subtext a')[-1]

        release_date = release_tag.css('a::text').get().strip()

        # schema rating
        rating = response.css('div.ratingValue strong span::text').get().strip()

        # schema grossing,run-time
        details_list = response.css('#titleDetails div.txt-block')

        grossing = ""
        runtime = ""
        for i, detail in enumerate(details_list):
            key_value_list = detail.css('::text').getall()
            if "Gross USA:" in key_value_list:
                grossing = key_value_list[-1].strip()
            if detail.css('time::text').get():
                runtime = detail.css('time::text').get()

        # schema director
        credit_items = response.css('div.credit_summary_item')

        director_list = []
        for i, credit_item in enumerate(credit_items):
            key = credit_item.css('h4.inline::text').get()
            if "Director" in key:
                director_list = credit_item.css('a::text').getall()
                break

        director_list = [director.strip() for director in director_list]
        directors = ", ".join(director_list)

        result = OrderedDict()
        result['Name'] = title
        result['ReleaseDate'] = release_date
        result['Certificate'] = certificate
        result['Rating'] = rating
        result['Runtime'] = runtime
        result['Director'] = directors
        result['Genre'] = genre_string
        result['Grossing'] = grossing

        yield result


if __name__ == "__main__":
    ImdbSpider()
