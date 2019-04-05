# -*- coding: utf-8 -*-
import scrapy


class RottombotSpider(scrapy.Spider):
	name = 'rottombot'
	allowed_domains = ['www.rottentomatoes.com']
	#start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=2018']

	def start_requests(self):
		urls = [
		'https://www.rottentomatoes.com/top/bestofrt/?year='
		]
		for url in urls:
			year = 1980
			for year in range(1920, 2019):
				current_url = url + str(year)
				yield scrapy.Request(url=current_url, callback=self.parse)

	def parse_movie_info(self, response):
		data = dict()
		data['title'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/h1/text()').get()
		movie_info = response.xpath('//*[@id="mainColumn"]/section[3]/div/h2/text()').get()
		if movie_info == "Movie Info":
			movie_info = response.xpath('//*[@id="mainColumn"]/section[3]/div/div')
		else:
			movie_info = response.xpath('//*[@id="mainColumn"]/section[2]/div/div')

		data['genre'] = movie_info.xpath('ul/li[2]/div[2]/a/text()').getall()
		data['director'] = movie_info.xpath('ul/li[3]//a/text()').getall()
		data['rating'] = response.xpath('//*[@id="js-rotten-count"]/text()').getall()[-1].replace("\n", "").replace(" ", "")

		i = 1
		while True:
			tag = movie_info.xpath('ul/li[' + str(i) + ']/div[1]/text()').get()
			if tag is not None:
				if tag == "In Theaters: ":
					data['release'] = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/time/text()').get()
				if tag == "Runtime: ":
					data['runtime'] = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/time/text()').get()
				if tag == "Box Office: ":
					data['grossing'] = movie_info.xpath('ul/li[' + str(i) + ']/div[2]/text()').get()
					#print("\n\n\n\nFOUND FOUND FOUND\n\n\n\n")
			i = i + 1
			if i > 10:
				break
		if 'runtime' not in data:
			data['runtime'] = ''
		data['runtime'] = data['runtime'].replace("\n", "").replace("  ", "")
		
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
        
