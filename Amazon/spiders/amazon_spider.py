import scrapy
from ..items import AmazonItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number=2
    # allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s?k=last+30+days+books&i=stripbooks-intl-ship&ref=nb_sb_noss_2'
    
    ]

    def parse(self, response):
        items=AmazonItem()
        product_name=response.css('.a-color-base.a-text-normal').css('::text').extract()
        product_author=response.css('.sg-col-12-of-28 .a-size-base+ .a-size-base').css('::text').extract()
        # product_author=response.css('.sg-col-12-of-28 .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.a-link-normal').css('::text').extract()
        product_price=response.css('.a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css('::text').extract()
        product_imagelink=response.css('.s-image::attr(src)').extract()

        items['product_name']=product_name
        items['product_author']=product_author
        items['product_price']=product_price
        items['product_imagelink']=product_imagelink
        yield items
        next_page='https://www.amazon.com/s?k=last+30+days+books&i=stripbooks-intl-ship&page=' + str(AmazonSpiderSpider.page_number) + '&qid=1598968145&ref=sr_pg_2/'
        if AmazonSpiderSpider.page_number <=100:
            AmazonSpiderSpider.page_number=AmazonSpiderSpider.page_number+1
            yield response.follow(next_page,callback=self.parse)