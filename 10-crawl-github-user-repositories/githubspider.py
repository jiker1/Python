# -*- coding: utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'shiyanlou-github'

    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?tab=repositories', 
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoyMToyNCswODowMM4FkpXN&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yN1QxMToxODoxMiswODowMM4ByCsB&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yNFQxNzowMToyNyswODowMM4BnQHM&tab=repositories'
               )

    def parse(self, response):
        for repository in response.css('li.public'):
            yield {
                'name': repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first(r'\n\s*(.*)'),
                'update_time': repository.xpath('.//relative-time/@datetime').extract_first()
            }
