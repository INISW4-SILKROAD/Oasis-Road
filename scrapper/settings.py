# Scrapy settings for musinsa project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime, logging
from types import SimpleNamespace

suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')


BOT_NAME = "scrapper"

SPIDER_MODULES = ["scrapper.spiders"]
NEWSPIDER_MODULE = "scrapper.spiders"

#LOG_FILE = f'../result/log/{suffix}_log.txt'

LOG_FILE = f'./result/log/{suffix}_log.log'
LOG_LEVEL = 'DEBUG'
LOG_FORMATTER = 'scrapper.log_formatter.PoliteLogFormatter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "musinsa (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
FEED_FORMAT = "json"
FEED_URI = f"./result/{suffix}_musinsa_products.json"

RETRY_ENABLED = True
RETRY_TIMES = 1  # 기본 재시도 횟수를 증가시킵니다.


# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "musinsa.middlewares.MusinsaSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "musinsa.middlewares.MusinsaDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "scrapper.pipelines.MusinsaImagesPipeline": 300,
   "scrapper.pipelines.MusinsaInfoImagesPipeline": 310,
   "scrapper.pipelines.MusinsaInfoJsonPipeline": 320, 
   "scrapper.pipelines.OCRPipeline":330, 
   "scrapper.pipelines.DetectionPipeline" :340
   }
#    "musinsa.pipelines.DuplicatesPipeline": 100,

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FILES_STORE = "."
IMAGES_STORE = "."

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

PATHS = SimpleNamespace(
   GIMAGE = './result/data/image/goods',
   IIMAGE = './result/data/image/info',
   TIMAGE = './result/data/image/texture',
   GJSON  = './result/data/json/goods',
   IJSON  = './result/data/json/info'
)

# image domain/url
URLS= SimpleNamespace(
   IMAGE ='https://image.msscdn.net',
   INFO ='https://goods-detail.musinsa.com/goods'
)
