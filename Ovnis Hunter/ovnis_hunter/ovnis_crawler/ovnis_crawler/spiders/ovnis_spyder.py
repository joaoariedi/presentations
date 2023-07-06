import scrapy


class Report(scrapy.Item):
    link = scrapy.Field()
    date = scrapy.Field()
    posted = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    shape = scrapy.Field()
    duration = scrapy.Field()
    summary = scrapy.Field()
    images = scrapy.Field()

    
class OVNIsSpider(scrapy.Spider):
    name = "ovnis"

    BASE_URL = 'https://www.nuforc.org/webreports/'

    def start_requests(self):
        yield scrapy.Request(f'{self.BASE_URL}ndxevent.html', callback=self.parse_links)

    def parse_links(self, response):
        links = response.xpath("//a/@href").getall()
        for link in links[1:-1]:
            absolute_url = self.BASE_URL + link

            yield scrapy.Request(absolute_url, callback=self.parse_month)

    def parse_month(self, response):
        report = Report()
        table = response.xpath("//table")
        tbody = table.xpath("tbody")
        rows = tbody.xpath("tr")
        for row in rows:
            report['link'] = self.BASE_URL + "/" + row.xpath("td[1]/a//@href").get()
            report['date'] = row.xpath("td[1]/a//text()").get()
            report['city'] = row.xpath("td[2]//text()").get()
            report['state'] = row.xpath("td[3]//text()").get()
            report['country'] = row.xpath("td[4]//text()").get()
            report['shape'] = row.xpath("td[5]//text()").get()
            report['duration'] = row.xpath("td[6]//text()").get()
            report['summary'] = row.xpath("td[7]//text()").get()
            report['posted'] = row.xpath("td[8]//text()").get()
            report['images'] = row.xpath("td[9]//text()").get()

            yield report
