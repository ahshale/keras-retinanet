import numpy as np
import os
import csv
import xml.etree.ElementTree as ET
import pickle

def parse_voc_annotation(ann_dir, img_dir, ann_file, resize_scale=5):
    
    with open(ann_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)

        for ann in sorted(os.listdir(ann_dir)):
            print(ann)

            try:
                tree = ET.parse(ann_dir + ann)
            except Exception as e:
                print(e)
                print('Ignore this bad annotation: ' + ann_dir + ann)
                continue
            
            for elem in tree.iter():
                if 'filename' in elem.tag:
                    
                    filename = img_dir + elem.text

                if 'object' in elem.tag:
                    for attr in list(elem):
                        #print()
                        if 'name' in attr.tag:
                            obj_name = attr.text
                            print(obj_name)
                                
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
                    print(obj_info)
                    csv_writer.writerow(obj_info)

def cls_map(map_file):
    with open(map_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['metal','0'])
        csv_writer.writerow(['glass','1'])
        csv_writer.writerow(['stone','2'])

if __name__ == '__main__':
    ANN_DIR = 'D:/xgll/dataset/trainset_xml/'
    IMG_DIR = 'D:/xgll/dataset/resized_trainset/'
    ANN_FILE = 'D:/xgll/dataset/ann_file.csv'
    MAP_FILE = 'D:/xgll/dataset/map_file.csv'
    parse_voc_annotation(ANN_DIR, IMG_DIR, ANN_FILE)
    cls_map(MAP_FILE)