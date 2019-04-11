# -*- coding: utf-8 -*-
import scrapy


class RottombotSpider(scrapy.Spider):
	name = 'RottonTomatoes'
	allowed_domains = ['www.rottentomatoes.com']
	#start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=2018']

	def start_requests(self):
		urls = [
		'https://www.rottentomatoes.com/top/bestofrt/?year='
		]
		for url in urls:
			year = 1980
			for year in range(1910, 2020):
				current_url = url + str(year)
				yield scrapy.Request(url=current_url, callback=self.parse)

	def parse_movie_info(self, response):
		data = dict()
		name = response.xpath('//*[@id="topSection"]/div[2]/div[1]/h1/text()').get()
		movie_info = response.xpath('//*[@id="mainColumn"]/section[3]/div/h2/text()').get()
		if movie_info == "Movie Info":
			movie_info = response.xpath('//*[@id="mainColumn"]/section[3]/div/div')
		else:
			movie_info = response.xpath('//*[@id="mainColumn"]/section[2]/div/div')

		genre = movie_info.xpath('ul/li[2]/div[2]/a/text()').getall()
		director = movie_info.xpath('ul/li[3]//a/text()').getall()
		rating = response.xpath('//*[@id="js-rotten-count"]/text()').getall()[-1].replace("\n", "").replace(" ", "")

		release = ""
		runtime = ""
		grossing = ""
		runtime = ""
		certificate = ""
		i = 1
		while True:
			tag = movie_info.xpath('ul/li[' + str(i) + ']/div[1]/text()').get()
			if tag is not None:
				if tag == "Rating: ":
					certificate = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/text()').get().split(" ")[0]
				if tag == "In Theaters: ":
					release = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/time/text()').get()
				if tag == "Runtime: ":
					runtime = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/time/text()').get()
				if tag == "Box Office: ":
					grossing = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/text()').get()
					#print("\n\n\n\nFOUND FOUND FOUND\n\n\n\n")
			i = i + 1
			if i > 10:
				break
		runtime = runtime.replace("\n", "").replace("  ", "")
		data['Name'] = name
		data['ReleaseDate'] = release
		data['Certificate'] = certificate
		data['Rating'] = rating
		data['Runtime'] = runtime
		data['Director'] = director
		data['Genre'] = genre
		data['Grossing'] = grossing
        
		#tag = movie_info.xpath('ul/li[7]/div[1]/text()').get()
		#print("|" + tag + "|")
		#if tag == "Runtime: ":
		#	data['runtime'] = movie_info.xpath('ul/li[7]/div[2]/time/text()').get()
		#else:
		#	print('inside else')
		#	data['runtime'] = movie_info.xpath('ul/li[6]/div[2]/time/text()').get()
		yield data

	def parse(self, response):
		links = response.xpath('//*[@id="top_movies_main"]/div/table//tr//a/@href').getall()

		for link in links:
			next_link = response.urljoin(link)
			yield scrapy.Request(next_link, callback=self.parse_movie_info)
        
