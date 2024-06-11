import os, sys
import preprocess

try:
    if not os.path.exists('./result'):
        os.mkdir('./result')
        os.mkdir('./result/data')
        os.mkdir('./result/data/image')
        os.mkdir('./result/data/json')
        os.mkdir('./result/data/image/goods')
        os.mkdir('./result/data/image/info')
        os.mkdir('./result/data/image/texture')
        os.mkdir('./result/data/json/goods')
        os.mkdir('./result/data/json/info')
        os.mkdir('./result/log')
except:
    print("can't make dirs")