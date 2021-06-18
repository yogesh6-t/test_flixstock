from hashing.hashing import convert_hash
from hashing.hashing import dhash
import argparse
import cv2
import pickle
import time

ap = argparse.ArgumentParser()
ap.add_argument('-t', '--tree', required = True, type = str, help = 'path to VPTree')
ap.add_argument('-a', '--hashes', required = True, type = str, help = 'path for hashes directory')
ap.add_argument('-q', '--query', required = True, type = str, help = 'path to query image')
ap.add_argument('-d', '--distance', type = int, help = 'max hamming dist')
args = vars(ap.parse_args())

print('[INFO] loading VP tree and hashes..')
tree = pickle.loads(open(args['tree'], 'rb').read())
hashes = pickle.loads(open(args['hashes'], 'rb').read())
image = cv2.imread(args['query'])
cv2.imshow('query', cv2.resize(image, (300, 400)))
cv2.imwrite('result.jpg', cv2.resize(image, (300, 400)))
queryHash = dhash(image)
queryHash = convert_hash(queryHash)
print('[INFO] queryHash is : {}'.format(queryHash))

print('[INFO] performing search...')
start = time.time()
results = tree.get_all_in_range(queryHash, args['distance'])
results = sorted(results)
end = time.time()

print('[INFO] search took {} seconds'.format(end-start))
for (d,h) in enumerate(results):
    resultPaths = hashes.get(h, [])
    print('[INFO] {} total images with d : {}, h :{}'.format(len(resultPaths), d,h))
    for resultPath in resultPaths:
        result = cv2.imread(resultPath)
        cv2.imshow('result', cv2.resize(image, (300, 400)))
        cv2.imwrite('result.jpg', cv2.resize(image, (300, 400)))
        cv2.waitKey(0)

cv2.waitKey(0)

