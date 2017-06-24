# -*- coding: utf-8 -*-
import scrapy


class JusteatspiderSpider(scrapy.Spider):
    name = 'justeatspider'
    allowed_domains = ['justeat.com']
    start_urls = [
        'https://www.just-eat.ca/area/h2v-montreal/?lat=45.522435&long=-73.602111',
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u,
                                 cookies={'je-last_latitude_used': '45.522435',
                                          'je-last_longitude_used': '-73.602111',
                                          'je-last_city_used': 'Montréal',
                                          'je-last_houseNo_used': '263',
                                          'je-last_street_used': 'Rue Saint Viateur Ouest',
                                          'je-location': 'H2V 1Y1'},
                                 dont_filter=True)

    def parse(self, response):
        for listing in response.xpath('//*[contains(@data-test-id, "listingGroupOpen")]//section[contains(@class, "listing-item")]'):
            yield {
                'name': listing.xpath('.//h3[contains(@class, listing-item-title)]/text()').extract(),
                'rating': listing.xpath('.//meta[contains(@itemprop, "ratingValue")]/@content').extract(),
                'numberOfRatings': listing.xpath('.//meta[contains(@itemprop, "ratingCount")]/@content').extract(),
                'cuisineType': listing.xpath('.//p[contains(@itemprop, "servesCuisine")]/strong/text()').extract(),
                'location': listing.xpath('.//p[contains(@itemprop, "address")]/text()').extract(),
                'url': listing.xpath('.//a[contains(@class, "listing-item-link")]/@href').extract(),
                'deliveryFee': listing.xpath('.//p[contains(@class, "infoText u-clearfix")]/text()').extract()[0],
                'deliveryRequirement': listing.xpath('.//p[contains(@class, "infoText u-clearfix")]/text()').extract()[1],
            }
