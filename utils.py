import base64
from datetime import datetime
import os
from sentence_transformers import SentenceTransformer, util
import json
import sys
# from detectron2.config import get_cfg
# sys.path.insert(0, 'grit/third_party/CenterNet2/projects/CenterNet2/')
# from centernet.config import add_centernet_config
# from grit.grit.config import add_grit_config

import matplotlib.pyplot as plt

# Load the sBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_encoded_data}"
def get_image_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    # Filter out only the image files (assuming common image extensions)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff'))]
    return image_files    
def calculate_two_string_consine(text1, text2):
    # Encode the sentences to get their embeddings
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    # Compute cosine similarity between the embeddings
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    # print(f"Cosine similarity: {cosine_similarity.item()}")
    return cosine_similarity.item()
def count_object_detections(candidate, reference):
    # Normalize the lists by converting each element to lowercase
    candidate_normalized = [[item.lower() for item in sublist] for sublist in candidate]
    reference_normalized = [[item.lower() for item in sublist] for sublist in reference]
    correct_objects = []
    for item1 in candidate_normalized:
        for item2 in reference_normalized: 
            object_name_consine = calculate_two_string_consine(item1, item2)
            if object_name_consine > 0.7:
                item1 == item2
                correct_objects.append(item2)
                print(f'{item2} is correct')
                reference_normalized.remove(item2)        
    return correct_objects
# # AmbDR == Ambiguous Detection Rate
# # ComGR == Commands Generation Rate
# # ComR == Completion Rate
def evaluate_correct_number(label_objects, predicted_objects, state_only):
    correct_state = 0
    correct_destination = 0
    correct_grasping_type = 0
    correct_placing_type = 0
    uncertain_objects = 0
    correct_uncertain_objects = 0
    correct_complete = 0
    mark = 0
    # TODO 
    for key, value in predicted_objects.items():
        if isinstance(value, str):  # Make sure the value is a string before applying .lower()
            predicted_objects[key] = value.lower()
    label_objects = [[label_object, label_object_value] for label_object, label_object_value in label_objects.items()]
    predicted_objects = [[predicted_object, predicted_object_value] for predicted_object, predicted_object_value in predicted_objects.items()]
    for predicted_object in predicted_objects:
        skip_current_i = False
        for label_object in label_objects:
            object_name_consine = calculate_two_string_consine(label_object[0].lower(), predicted_object[0].lower())
           
            if object_name_consine > 0.7:
                print(f"predicted_object: {predicted_object[0]}")
                print(f"label_object: {label_object[0]}")
                # if all the value are same, we judge it as one object
                # and predicted_object_value["size"] == label_object_value["size"]
                # predicted_object_value["shape"] == label_object_value["shape"]
                label_object_state = label_object[1]["state"]
                # print(f"The label object state is: {label_object_state}")
                try:
                    predicted_object_state = predicted_object[1]["state"]
                    # print(f"The predicted object state is: {predicted_object_state}")
                except KeyError:
                    print(f"{label_object[1]} does not the key 'state'.")
                    continue
                object_state_consine = calculate_two_string_consine(label_object_state, predicted_object_state)
                if object_state_consine > 0.7:
                    correct_state += 1 
                    if state_only != 1:
                        if label_object[1]["destination"] == "uncertain":
                            uncertain_objects +=1
                            if predicted_object[1]["destination"] == label_object[1]["destination"]:
                                correct_uncertain_objects +=1
                        
                        if predicted_object[1]["destination"] == label_object[1]["destination"]:
                            correct_destination +=1
                            if predicted_object[1]["grasping_type"] == label_object[1]["grasping_type"] and predicted_object[1]["placing_type"] == label_object[1]["placing_type"]:
                                correct_complete += 1
                        if predicted_object[1]["grasping_type"] == label_object[1]["grasping_type"]:
                            correct_grasping_type +=1
                        if predicted_object[1]["placing_type"] == label_object[1]["placing_type"]:
                            correct_placing_type +=1
                    # print(f"{label_object[0]} and {predicted_object} are same object")  
                    label_objects.remove(label_object)
                    skip_current_i = True
                    break  # Exit the inner loop
        if skip_current_i:
            continue
        
    return correct_state, correct_destination, correct_grasping_type, correct_placing_type, uncertain_objects, correct_uncertain_objects, correct_complete

def setup_cfg():
    cfg = get_cfg()
    cfg.MODEL.DEVICE="cpu"
    add_centernet_config(cfg)
    add_grit_config(cfg)
    cfg.merge_from_file('grit/configs/GRiT_B_DenseCap_ObjectDet.yaml')
    cfg.merge_from_list(['MODEL.WEIGHTS', 'grit/models/grit_b_densecap_objectdet.pth'])
    # Set score_threshold for builtin models
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = 0.1
    cfg.MODEL.TEST_TASK = 'DenseCap'
    cfg.MODEL.BEAM_SIZE = 1
    cfg.MODEL.ROI_HEADS.SOFT_NMS_ENABLED = False
    cfg.USE_ACT_CHECKPOINT = False
    cfg.freeze()
    return cfg

        
def count_same_meaning_items_of_ambiguity(candidate, reference):
    # Normalize the lists by converting each element to lowercase
    candidate_normalized = [item.lower() for item in candidate]
    reference_normalized = [item.lower() for item in reference]
    same_meaning_count = 0
    for item1 in candidate_normalized:
        for item2 in reference_normalized:
            cosine = calculate_two_string_consine(item1, item2)
            print(f"{item1} and {item2} cosine value is {cosine}")
            if cosine > 0.8:
                same_meaning_count +=1
    return same_meaning_count


        

  
