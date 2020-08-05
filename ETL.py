import json
import jieba
import pandas as pd
import re
import redis
from string import punctuation
import xml.etree.ElementTree as ET

redis_host = 'localhost'
redis_port = 6379
redis_db = 0

fileNameA = './static/sb_a.csv'
fileNameB = './static/sb_b.xml'
outputName = './static/sb.json'
dictFileName = './static/dict.txt'


jieba.set_dictionary(dictFileName)
redis = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


def get_redis_key(productId):
    return "product:{}".format(productId)


def clean_punctuation(words):
    return re.sub(r"[{}【】]".format(punctuation)," ",words)


def word_segmentation(words):
    words = clean_punctuation(words)
    words = jieba.cut(words, cut_all=False, HMM=True)
    segmented_word = [word.strip().lower() for word in words]
    segmented_word = list(filter(None, segmented_word))
    segmented_word = ' '.join(map(str, segmented_word))
    return segmented_word


def process_dataA():
    df = pd.read_csv(fileNameA)
    for index, row in df.iterrows():
        result = {}
        result['product_id'] = row['item_id']
        result['merchant'] = 'sb_a'
        result['url'] = row['product_url']
        result['image_url'] = row['image_url']
        result['product_title'] = row['name']
        result['price'] = float(row['price'])
        result['brand'] = ''
        result['seller'] = row['shop_url']
        result['segmented_product_title']  = word_segmentation(row['name'])
        redis_key = get_redis_key(row['item_id'])
        redis.set(redis_key, json.dumps(result)) 


def process_dataB():
    tree = ET.parse(fileNameB)
    root = tree.getroot()
    for r in root.findall('product'):
        row = {}
        row['product_id'] = r.find('ProductID').text
        row['url'] = r.find('BuyURL').text
        row['merchant'] = 'sb_b'
        row['product_title'] = r.find('ProductName').text
        row['img_url'] =  r.find('ProductImage2').text
        row['seller'] = ''
        row['price'] = float(r.find('SalePrice').text)
        row['brand'] = re.findall("【(.*?) (.*?)】",row['product_title'])[0][0].lower()
        row['segmented_product_title'] = word_segmentation(row['product_title'])
        
        redis_key = get_redis_key(row['product_id'])
        redis.set(redis_key, json.dumps(row)) 
        

def upload():
    with open(outputName, 'w', encoding='utf-8') as outfile:
        for key in redis.scan_iter(match='product:*'):
            data = redis.get(key).decode('utf-8')
            json.dump(json.loads(data), outfile)
            outfile.write('\n')
        outfile.close()


if  __name__=="__main__":
    # If you want to etl data, you can complete it by airflow.
    process_dataA()
    process_dataB()
    upload()
