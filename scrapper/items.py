# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MusinsaItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field() # 제품명
    id = scrapy.Field() # 품번
    info = scrapy.Field() # 공시
    price = scrapy.Field() # 무신사 판매가
    
    imgs = scrapy.Field() # 제품 이미지
    info_imgs = scrapy.Field() # 상세 이미지
    texture_img = scrapy.Field()

    portion = scrapy.Field()
    
    img_urls = scrapy.Field() # 상품이미지 url
    info_img_urls = scrapy.Field() # 상세 이미지 url
    json = scrapy.Field() # 상품 정보
    info_json = scrapy.Field() # 공시정보
