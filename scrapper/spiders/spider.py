import scrapy
from scrapy import Spider

from .. import items
import re

INFO_IMG_REGEX_PATTERN = re.compile(r'src=[\"\']((?:https?://)?(?://)?(?:www\.)?[-\w]+(?:\.[-\w]+)+(?:/[\w./?%&=-]*)?\.(?:jpg|png|JPEG|jpeg))[\"\']?')

class MusinsaSpider(Spider):
	# 스파이더 이름(실행)
    name = "one"
    def __init__(self, *args, **kwargs):
        super(MusinsaSpider, self).__init__(*args, **kwargs)
        self.id = kwargs['id']
      
    def start_requests(self):
        product_url = "https://goods-detail.musinsa.com/goods/"
        url = product_url + str(self.id)
        
        yield scrapy.Request(url, self.parse_items)

    # 상품 상세 페이지에 있는 정보 크롤링
    def parse_items(self, response):
        item = items.MusinsaItem()

        product_json = response.json()['data']
        pid = product_json['goodsNo']

        item['id'] = pid # 품번
        item['json'] = response
        
        item['name'] = product_json['goodsNm'] # 제품명
        
        item['info'] = 'info_' + str(pid)+'.json'
        item['price'] = product_json['goodsPrice']['originPrice'] # 무신사 판매가
        
        item['img_urls'] = [product_json['thumbnailImageUrl']] + [i['imageUrl'] for i in product_json['goodsImages']] # 제품 이미지
        item['info_img_urls'] = re.findall(INFO_IMG_REGEX_PATTERN, product_json['goodsContents'])
        
        yield item

    def get_review(self, id):
        url = 'https://goods.musinsa.com/api/goods/v1/review/satisfaction-html?goodsNo='+str(id)
        yield scrapy.Request(url)