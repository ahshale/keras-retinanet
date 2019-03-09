import numpy as np
import os
import csv
import xml.etree.ElementTree as ET
import pickle

def parse_voc_annotation(ann_dir, img_dir, ann_file, resize_scale=5):
    
    with open(ann_file, 'wb') as f:
        csv_writer = csv.writer(f)

        for ann in sorted(os.listdir(ann_dir)):

            try:
                tree = ET.parse(ann_dir + ann)
            except Exception as e:
                print(e)
                print('Ignore this bad annotation: ' + ann_dir + ann)
                continue
            
            for elem in tree.iter():
                if 'filename' in elem.tag:
                    filename = img_dir + elem.text
                    
                    for attr in list(elem):
                        if 'name' in attr.tag:
                            obj_name = attr.text
                                
                        if 'bndbox' in attr.tag:
                            for dim in list(attr):
                                if 'xmin' in dim.tag:
                                    obj_xmin = int(round(float(dim.text) / resize_scale))
                                if 'ymin' in dim.tag:
                                    obj_ymin = int(round(float(dim.text) / resize_scale))
                                if 'xmax' in dim.tag:
                                    obj_xmax = int(round(float(dim.text) / resize_scale))
                                if 'ymax' in dim.tag:
                                    obj_ymax = int(round(float(dim.text) / resize_scale))

                        obj_info = [filename, obj_xmin, obj_ymin, obj_xmax, obj_ymax, obj_name]
                        obj_info = ','.join([it for it in obj_info])
                        csv_writer.writerow(obj_info)

def cls_map(map_file):
    with open(map_file, 'wb') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow('metal,0')
        csv_writer.writerow('glass,1')
        csv_writer.writerow('stone,2')

if __name__ == '__main__':
    ANN_DIR = r'E:\paper\居民区垃圾\paper_data\xml'
    IMG_DIR = r'E:\paper\居民区垃圾\paper_data\dataset'
    ANN_FILE = r'E:\paper\居民区垃圾\paper_data\ann_file.csv'
    MAP_FILE = r'E:\paper\居民区垃圾\paper_data\map_file.csv'
    parse_voc_annotation(ANN_DIR, IMG_DIR, ANN_FILE)
    cls_map(MAP_FILE)