
import os

import PIL.Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import  Image

import boto3
import io
import json


os.environ['AWS_DEFAULT_REGION'] = 'xxxxxxxxxxxx'
os.environ['AWS_ACCESS_KEY_ID'] = 'xxxxxxxxxxxxxxxxxx'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'xxxxxxxxxxxx'

bool_checked_dict={

}

class CheckBoxDetection():
    def __int__(self):
        pass
    def Amazon_detect_text_api(self,image):
        # Encode the image as a JPG
        ret, buffer = cv2.imencode(".jpg", image)

        # Create a ByteIO object from the encoded image
        byte_io = io.BytesIO(buffer)
        client = boto3.client('textract')
        response_fields = client.analyze_document(Document={'Bytes': byte_io.getvalue()}, FeatureTypes=['FORMS'])
        blocks = response_fields['Blocks']

        with open('outs/analyse_dummy.json', 'w', encoding='utf-8') as f:
            json.dump(response_fields, f, ensure_ascii=False, indent=4)
        return response_fields

    def CheckedBoxesDetection(self,image):
        response = self.Amazon_detect_text_api(image)
        # json_file = 'outs/analyse_dummy.json'
        # response = None
        # with open(json_file, 'r') as f:
        #     response = json.load(f)

        blocks = response['Blocks']
        SelectionStatus = 'SELECTED'
        if SelectionStatus == 'SELECTED':
            Found_Text = get_text_by_SelectionStatus(SlectionStatus=SelectionStatus, blocks=blocks)
            for line in Found_Text:
                bool_checked_dict[line] = True
        SelectionStatus = 'NOT_SELECTED'
        if SelectionStatus == 'NOT_SELECTED':
            Found_Text = get_text_by_SelectionStatus(SlectionStatus=SelectionStatus, blocks=blocks)
            for line in Found_Text:
                bool_checked_dict[line] = False



    def Perform_OCR_To_Detect_CheckBox(self,filename):
        plot_flag = True
        save_output = True
        out_folder = 'outs'
        os.makedirs(out_folder, exist_ok=True)
        line_min_width = 15
        image_path = filename
        image = cv2.imread(image_path)

        image = image.astype(np.uint8)
        self.CheckedBoxesDetection(image)

        if save_output:
            cv2.imwrite(os.path.join(out_folder, f'out_{image_path}'), image)
        return bool_checked_dict




def get_text_by_SelectionStatus(SlectionStatus,blocks):
    selected_id_list= []
    FOUND_TEXT = []
    for block in blocks:
        if block['BlockType'] == 'SELECTION_ELEMENT':
            if block["SelectionStatus"] == SlectionStatus:
                selected_id_list.append(block['Id'])
                selected_id = block['Id']

    key_value_block_list= []
    for selected_id in selected_id_list:
        for block_1 in blocks:
            if block_1['BlockType'] == 'KEY_VALUE_SET':
                try:
                    rel_blocks = block_1['Relationships']
                    for rel_block in rel_blocks:
                        for id in rel_block['Ids']:
                            if selected_id == id:
                                key_value_block_list.append(block_1['Id'])

                except KeyError:
                    pass

    main_key_block_childs_list = []
    for key_value_block in key_value_block_list:
        for block_2 in blocks:
            if block_2['BlockType'] == 'KEY_VALUE_SET':
                try:
                    rel_blocks = block_2['Relationships']
                    for rel_block in rel_blocks:
                        for id in rel_block['Ids']:
                            if key_value_block == id:
                                rel_blocks = block_2['Relationships']
                                for rel_block in rel_blocks:
                                    if rel_block['Type'] == 'CHILD':
                                        main_key_block_childs_list.append(rel_block['Ids'])

                except KeyError:
                    pass
    for key_block in main_key_block_childs_list:
        for block_3 in blocks:
            if block_3['BlockType'] == 'LINE':
                rel_blocks = block_3['Relationships']
                for rel_block in rel_blocks:
                    if rel_block['Type'] == 'CHILD':
                        child_list = rel_block['Ids']
                        if key_block == child_list:
                            FOUND_TEXT.append(block_3['Text'])

    return FOUND_TEXT



filename='in/checked.png'

check_box_detection= CheckBoxDetection()
bool_checked_dict=check_box_detection.Perform_OCR_To_Detect_CheckBox(filename)
print(bool_checked_dict)



