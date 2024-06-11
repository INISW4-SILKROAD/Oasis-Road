from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapper.settings import PATHS, URLS

from pathlib import PurePosixPath
from urllib.parse import urlparse
import hashlib

import json
from preprocess import FabricCropper, PortionRegex, ocr


def hash(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:15]


class MusinsaImagesPipeline(ImagesPipeline):
    '''
    img_urls의 링크에서 이미지를 저장하고, 저장 경로를 imgs에 저장하는 파이프라인
    '''
    def get_media_requests(self, item, info):
        for image_url in item['img_urls']:
            url = URLS.IMAGE + image_url
            yield Request(url)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Custom file path logic
        name = PurePosixPath(urlparse(request.url).path).name
    
        return f'{PATHS.GIMAGE}/{name}'
    
    def item_completed(self, results, item, info):
        if not results:
            raise DropItem("Item contains no images")

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        item['imgs'] = image_paths
        return item


class MusinsaInfoImagesPipeline(ImagesPipeline):
    '''
    info_img_urls의 링크에서 이미지를 저장하고, 저장 경로를 info_imgs에 저장하는 파이프라인
    '''
    def get_media_requests(self, item, info):
        for image_url in item['info_img_urls']:
            if image_url[12:19] == 'youtube':
                continue
            
            if image_url[0:8] =='/images/':
                url = URLS.IMAGE + '/' + image_url

            elif image_url[0] == '/':
                url = 'https://' + image_url.lstrip('/')
            else:
                url = image_url
            yield Request(url)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Custom file path logic
        name = str(item['id'])+'_'+ hash(request.url)+'.jpg' 

        return f'{PATHS.IIMAGE}/{name}'
    
    def item_completed(self, results, item, info):
        if not results:
            raise DropItem("Item contains no info images")

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no info images")

        item['info_imgs'] = image_paths
        return item


class MusinsaInfoJsonPipeline(FilesPipeline):     
    '''
    공시 정보를 json으로 저장하고 혼용률 정보를 파싱하는 파이프라인
    '''
    def get_media_requests(self, item, info):
        url = URLS.INFO + '/'+ str(item['id'])+'/essential'
        yield Request(url)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Custom file path logic
        name = 'detail_'+ PurePosixPath(urlparse(request.url).path).parent.name + '.json'
        return f'{PATHS.IJSON}/{name}'

    def item_completed(self, results, item, info):
        # JSON 파일을 파싱하여 혼용률 정보를 아이템에 추가
        if not results:
            raise DropItem("Item contains no JSON")

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no JSON")

        with open(image_paths[0], 'r', encoding='utf-8') as f:
            data = json.load(f)

        item['info_json'] = image_paths[0]        
        item['portion'] = data['data'][0]['value']  # 혼용률 정보 추가
        return item

class OCRPipeline:
    '''
    혼용률 정보를 전처리 후, 없다면 상세이미지에 ocr을 통해 찾는 파이프라인
    '''
    def process_item(self, item, spider):
        portion = PortionRegex.extract_and_process_text(item['portion'])
        if PortionRegex.is_correct_portion(portion):
            item['portion'] = portion     
            return item
        
        for path in item['info_imgs']:
            text = ocr(path)
            portion = PortionRegex.extract_and_process_text(text)
            if PortionRegex.is_correct_portion(portion):
                item['portion'] = portion     
                return item
        else:
            item['portion'] = None
            return item
            
class DetectionPipeline:
    '''
    상품 상세 이미지에서 texture를 잘라 저장하는 파이프라인
    '''
    def __init__(self):
        self.model = FabricCropper()
        
    def process_item(self, item, spider):
        for path in item['info_imgs']:
            result, path = self.model.crop_bbox(item['id'], path, PATHS.TIMAGE+'/', 0.7)
            if result != None:
                item['texture_img'] = result
                return item
        
        item['texture_img'] = None
        return item
            