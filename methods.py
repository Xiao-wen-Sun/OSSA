import ast
from openai import OpenAI
import json
# from utils import encode_image, get_image_files, setup_cfg
from utils import encode_image, get_image_files, setup_cfg
import re
from prompts import prompt_state_only, stateonly_example, scene_description, plain_prompt
from prompts import prompt_commands, vision_prompt, scene_planner1, scene_planner2, scene_planner3
from prompts import task1, task2, task3, example_scene_description
from datetime import datetime
from detectron2.engine.defaults import DefaultPredictor
from detectron2.data.detection_utils import read_image
from datetime import datetime


class Methods:
    def __init__(self):
        super().__init__()
        with open("openai_api_key.txt") as fapi:
            self.api_key = fapi.read()
        self.model_vision_VLM = "gpt-4-vision-preview"
        # self.model_vision_VLM = "gpt-4-1106-vision-preview"
        self.model_version = "gpt-3.5-turbo"
        self.model_version_L = "gpt-4-0125-preview"  # "gpt-4"
        self.client = OpenAI(api_key=self.api_key)
        self.token_limit = 4096
        self.cfg = setup_cfg()
        self.predictor = DefaultPredictor(self.cfg)
     

    def VLM_based_planner(self, user_instruction, image_path, state_only, zeroshot):
        # Getting the base64 string
        image_url_p = encode_image("/home/sun/projects/cleanup-table/imgs/example_scene2.png")
        if state_only==1:
            prompts = [{"role": "system", "content": prompt_state_only},]
            if zeroshot == 1:
                messages = prompts
            else:
                scene_example_prompts = [{"role": "user", "content": [{"type": "text", "text": task1},
                                                            {"type": "image_url","image_url": {"url": image_url_p,},},],},
                            {"role": "assistant", "content": stateonly_example},
                            ]
                messages = prompts + scene_example_prompts
        else:
            prompts = [{"role": "system", "content": plain_prompt},]
            if zeroshot == 1:
                messages = prompts
            else:
                scene_example_prompts = [{"role": "user", "content": [{"type": "text", "text": task1},
                                                            {"type": "image_url","image_url": {"url": image_url_p,},},],},
                            {"role": "assistant", "content": scene_planner1},
                            {"role": "user", "content": [{"type": "text", "text": task2},
                                                            {"type": "image_url","image_url": {"url": image_url_p,},},],},
                            {"role": "assistant", "content": scene_planner2},
                            {"role": "user", "content": [{"type": "text", "text": task3},
                                                            {"type": "image_url","image_url": {"url": image_url_p,},},],},
                            {"role": "assistant", "content": scene_planner3},
                            ]
                messages = prompts + scene_example_prompts
        image_url = encode_image(image_path)  
        user = {"role": "user","content": [{"type": "text", "text": user_instruction,},
                                           {"type": "image_url", "image_url": {"url": image_url,},},],}
        messages.append(user) 
        response = self.client.chat.completions.create( model= self.model_vision_VLM, 
                                                        messages= messages, 
                                                        max_tokens=1000, 
                                                        temperature=0)
        objects = response.choices[0].message.content
        # print(f"vlm-based objects: {objects}")
        return objects
    
    def LLM_based_planner(self, user_instruction, image_path, state_only, zeroshot, densetype):
        if state_only==1:
            prompts = [{"role": "system", "content": prompt_state_only},]
            if zeroshot == 1:
                messages = prompts
            else:
                scene_example_prompts = [{"role": "user", "content": "dense_captioning:" + example_scene_description},
                                    {"role": "user","content": "user_utterance: "+ task1},
                                    {"role": "assistant", "content": stateonly_example},
                                    ]
                messages = prompts + scene_example_prompts
        else:
            prompts = [{"role": "system", "content": prompt_commands},]
            if zeroshot == 1:
                messages = prompts
            else:
                scene_example_prompts = [{"role": "user", "content": "dense_captioning:" + example_scene_description},
                                        {"role": "user","content": "user_utterance: "+ task1},
                                        {"role": "assistant", "content": scene_planner1},
                                        {"role": "user","content": "user_utterance: "+ task2},
                                        {"role": "assistant", "content": scene_planner2},                               
                                        {"role": "user","content": "user_utterance: "+ task3},
                                        {"role": "assistant", "content": scene_planner3},
                                    ]
                messages = prompts + scene_example_prompts
        if densetype == "grit":
            dense_captioning = self.grit_dense_captioning(image_path)
        elif densetype == "gpt4":
            dense_captioning = self.gpt4_dense_captioning(image_path)
        else:
            print("please specify dense captioning method")
        # print("dense captioning", dense_captioning)
        dense_captioning = {"role": "user","content": "dense_captioning:" + dense_captioning}
        user = {"role": "user","content": "user_utterance:" + user_instruction}
        messages.append(dense_captioning) 
        messages.append(user) 
        response = self.client.chat.completions.create(
                                                        model= self.model_version_L, 
                                                        messages= messages, 
                                                        max_tokens=600, 
                                                        temperature=0)
        predicted_objects = response.choices[0].message.content
        # print(f"llm-based predicted_objects: {predicted_objects}")
        return predicted_objects
    def grit_dense_captioning(self, image_path):
        img = read_image(image_path, format="BGR")
        predictions = self.predictor(img)
        boxes = predictions['instances'].pred_boxes if predictions['instances'].has("pred_boxes") else None
        classes = predictions['instances'].pred_classes.tolist() if predictions['instances'].has("pred_classes") else None
        dense_captioning = predictions['instances'].pred_object_descriptions.data if predictions['instances'].has("pred_object_descriptions") else None
        # print("boxes: ", boxes)
        # print("classes: ", classes)
        # print("dense_captioning: ", dense_captioning)
        dense_captioning = ', '.join(dense_captioning)
        return dense_captioning
    def gpt4_dense_captioning(self, image_path, zeroshot=1):
        image_url_p = encode_image("/home/sun/projects/cleanup-table/imgs/example_scene.jpg")
        image_url = encode_image(image_path)
        if zeroshot == 1:
            prompts=[{"role": "system", "content": vision_prompt},
                 {"role": "user", "content": [{"type": "text", "text": "describe each independent object on the table",},
                                            {"type": "image_url","image_url": {"url": image_url,},},],}]
        else:
            prompts=[{"role": "system", "content": vision_prompt},
                    {"role": "user", "content": [{"type": "text", "text": "how many independent objects are on the table",},
                                                {"type": "image_url","image_url": {"url": image_url_p,},},],},
                    {"role": "assistant", "content": scene_description},
                    {"role": "user", "content": [{"type": "text", "text": "how many independent objects are on the table",},
                                                {"type": "image_url","image_url": {"url": image_url,},},],}]
        response = self.client.chat.completions.create(
                                                        model=self.model_vision_VLM,
                                                        messages=prompts,
                                                        max_tokens=300,)
        dense_captioning = response.choices[0].message.content
        return dense_captioning
def main(task, dataset_path, method, state_only, zeroshot, densetype):
    image_names = get_image_files(dataset_path)
    if task == 1:
        user_utterance = "clearing the table"
    elif task == 2:
        user_utterance = "clearing the table and keeping all the leftover food"
    elif task == 3:
        user_utterance = "clearing the table and throwing away all the leftover food"
    print(f"user_utterance: {user_utterance}")
    # Get the current date and time
    now = datetime.now()
    print("Current date and time:", now)
    # If you just need the current time
    current_time = now.strftime("%H:%M:%S")
    print("Current time:", current_time)
    results_path = f'/home/sun/projects/cleanup-table/results/task{task}_{method}_dense_{densetype}_stateonly{state_only}_zeroshot{zeroshot}_results_gpt4_{current_time}.json'
    # Function to read the current data from the file
    def read_current_data(path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def write_data(path, data):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    for image_name in image_names:
        new_result = {}
        current_data = read_current_data(results_path)
        image_path = dataset_path + image_name 
        if method == "vlm":
            predicted_objects = methods.VLM_based_planner(user_utterance, image_path, state_only, zeroshot)
        elif method == "llm":
            predicted_objects = methods.LLM_based_planner(user_utterance, image_path, state_only, zeroshot, densetype)
        else:
            predicted_objects = {"key":"value"}
        try:
            # Check if the item starts with 'JSON'
            if predicted_objects.startswith("JSON"):
                predicted_objects = json.loads(predicted_objects[4:])
            elif predicted_objects.startswith("```json"):
                predicted_objects = json.loads(predicted_objects[8:-4])
            else:
                predicted_objects = json.loads(predicted_objects)
        except json.JSONDecodeError:
            print(f"{image_name} Failed to decode JSON, skipping to the next item.")
            print(f"predicted_objects json: {predicted_objects}")
            continue
        # print(f"{method} predicted_objects: {predicted_objects}")
        key = f'{image_name.split(".")[0]}'
        value = predicted_objects
        new_result[key] = value
        # print(f"finish scene {image_name}")
        current_data.append(new_result)
        write_data(results_path, current_data)
def test_single_image(method, user_utterance,image_path, state_only, zeroshot, densetype):
    # for test single image
    if method == "vlm":
        predicted_objects = methods.VLM_based_planner(user_utterance, image_path, state_only, zeroshot)
        predicted_objects = json.loads(predicted_objects[8:-4])
    elif method == "llm":
        predicted_objects = methods.LLM_based_planner(user_utterance, image_path, state_only, zeroshot, densetype)
        predicted_objects = json.loads(predicted_objects[8:-4])
    else:
        predicted_objects = {"key":"value"}
    print("-----------------output-------------------")
    print(f"{method} predicted_objects: {predicted_objects}")
        
                
if __name__ == '__main__':
   
    user_utterance1 = "clearing the table"
    user_utterance2 = "clearing the table and keeping all the leftover food"
    user_utterance3 = "clearing the table and throwing away all the leftover food"
    # image_path = "/home/sun/projects/cleanup-table/datasets/test/scene22.jpeg"
    
    image_path = "/home/sun/projects/cleanup-table/datasets/test/scene7.jpeg"
    # image_path = "/home/sun/projects/cleanup-table/imgs/example_scene3.png"
    methods = Methods()
    # the output of zeroshot and fewshot has tiny different
    # zeroshot = 1, no example
    # zeroshot = 0, with example
    zeroshot = 1
    # state_only = 1, only generate object state
    # state_only = 0, generate object state and commands
    state_only = 0
    method = "vlm"
    # method = "llm"
    # densetype = "grit"
    # densetype = "gpt4"
    densetype = "no"
    # user_utterance = user_utterance1
    # test_single_image(method, user_utterance,image_path, state_only, zeroshot, densetype)
    # # run in the dataset
    task = 1
    dataset_path = '/home/sun/projects/cleanup-table/datasets/test/'
    main(task, dataset_path, method, state_only, zeroshot, densetype)
    