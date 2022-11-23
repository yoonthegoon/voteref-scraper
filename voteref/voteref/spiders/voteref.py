import scrapy


class VotersSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, **kwargs):
        super(VotersSpider, self).__init__(**kwargs)
        self.state_name = kwargs.get('state_name')
        self.q_list = kwargs.get('q_list')

    def start_requests(self):
        for q in self.q_list:
            url = f'https://voteref.com/voters' \
                  f'?state_name={self.state_name.replace(" ", "+")}' \
                  f'&query_type=voter' \
                  f'&q={q.replace(" ", "+")}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for row in response.css('#voters-table > tbody:nth-child(2) > tr'):
            name = row.css('th > a::text').get()
            registered_address = row.css('td:nth-child(2)::text').get()
            yield {
                'name': name,
                'registered_address': registered_address,
            }
