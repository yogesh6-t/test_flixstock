from hashing.hashing import convert_hash
from hashing.hashing import dhash
from hashing.hashing import hamming
from imutils import paths
import argparse
import cv2
import pickle
import vptree

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', required = True, type = str, help = 'path for input directory')
ap.add_argument('-t', '--tree', required = True, type = str, help = 'path for output vptree')
ap.add_argument('-a', '--hashes', required = True, type = str, help = 'path for output hashes dictionary')
args = vars(ap.parse_args())

imagePaths = list(paths.list_images(args['images']))
hashes = {}

for (i,imagePath) in enumerate(imagePaths):
    print('[processing image {}/{}'.format(i+1, len(imagePaths)))
    image = cv2.imread(imagePath)
    h = dhash(image)
    h = convert_hash(h)
    l = hashes.get(h, [])
    l.append(imagePath)
    hashes[h] = l

print('building Tree...')
points = list(hashes.keys())
tree = vptree.VPTree(points, hamming)

print('serializing VPtree...')
f = open(args['tree'], 'wb')
f.write(pickle.dumps(tree))
f.close()

print('serializing hashes...')
f = open(args['hashes'], 'wb')
f.write(pickle.dumps(hashes))
f.close()
