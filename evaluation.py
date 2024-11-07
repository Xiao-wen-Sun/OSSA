import json
from utils import evaluate_correct_number

def evaluation(label_results, predicted_results, state_only):
    all_correct_state = 0
    all_correct_destination = 0
    all_correct_grasping_type = 0
    all_correct_placing_type = 0
    all_uncertain_objects = 0
    all_correct_uncertain_objects = 0
    all_correct_complete = 0
    all_objects_num = 0
    uncertain_objects_rate = 0
    i = 0
    for predicted_result in predicted_results:
        correct_state = 0
        correct_destination = 0
        correct_grasping_type = 0
        correct_placing_type = 0
        uncertain_objects = 0
        correct_uncertain_objects = 0
        correct_complete = 0
        label_results_scene = [label_result for label_result, label_result_value in label_results.items()]
        for predicted_scene, predicted_scene_value in predicted_result.items():
            
            print(f"--------------predicted_scene: {predicted_scene}--------------------")
            
            if predicted_scene in label_results_scene:
                i += 1
                label_objects = label_results[predicted_scene]
                predicted_objects = predicted_result[predicted_scene]
                # label_objects = ast.literal_eval(label_objects)
                # predicted_objects = ast.literal_eval(predicted_objects)
                print(f"{i} the number of objects {len(label_objects)}")
                all_objects_num += len(label_objects)
                correct_state, correct_destination, correct_grasping_type, correct_placing_type, uncertain_objects, correct_uncertain_objects, correct_complete = evaluate_correct_number(label_objects, predicted_objects, state_only)

                all_correct_state += correct_state
                all_correct_destination += correct_destination
                all_correct_grasping_type += correct_grasping_type
                all_correct_placing_type += correct_placing_type
                all_uncertain_objects += uncertain_objects
                all_correct_uncertain_objects += correct_uncertain_objects
                all_correct_complete += correct_complete
            
    state_rate = all_correct_state/all_objects_num
    destination_rate = all_correct_destination/all_objects_num
    grasping_type_rate = all_correct_grasping_type/all_objects_num
    placing_type_rate = all_correct_placing_type/all_objects_num

    s_destination_rate = all_correct_destination/all_correct_state
    s_grasping_type_rate = all_correct_grasping_type/all_correct_state
    s_placing_type_rate = all_correct_placing_type/all_correct_state

    if all_uncertain_objects:
        uncertain_objects_rate = all_correct_uncertain_objects/all_uncertain_objects
    else:
        print(f"there is no ambguity in this scene")
    compelete_rate = all_correct_complete/all_objects_num
    
    print(f"State Detection Rate: {state_rate}")
    print(f"Ambiguous Detection Rate: {uncertain_objects_rate}")
    # print(f"Destination Generation Rate: {destination_rate}")
    # print(f"Grasping Type Generation Rate: {grasping_type_rate}")
    # print(f"Placing Type Generation Rate: {placing_type_rate}")
    
    print(f"ss Destination Generation Rate: {s_destination_rate}")
    print(f"ss Grasping Type Generation Rate: {s_grasping_type_rate}")
    print(f"ss Placing Type Generation Rate: {s_placing_type_rate}")
    print(f"Completion Rate: {compelete_rate}")
    print(f"total {all_objects_num} objects be labeled in this dataset")
    
if __name__ == '__main__':
    
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_stateonly1_zeroshot1_results1.json', 'r') as file:
    #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_kitchen_cskt0_zeroshot1_results1.json', 'r') as file:
    # #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_stateonly0_zeroshot1_results1.json', 'r') as file:
    #     predicted_results = json.load(file)
    #-----------State only-----------LLM + GRiT----------------
    
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_grit_stateonly1_zeroshot1_results_gpt4_16:26:59.json', 'r') as file:
    #     predicted_results = json.load(file)  
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_grit_stateonly1_zeroshot1_results_gpt4_14:17:24.json', 'r') as file:
    #     predicted_results = json.load(file)  
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_grit_stateonly1_zeroshot1_results_gpt4_15:15:14.json', 'r') as file:
    #     predicted_results = json.load(file)  
    
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_grit_stateonly1_zeroshot0_results_gpt4_12:42:01.json', 'r') as file:
    #     predicted_results = json.load(file)     
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_grit_stateonly1_zeroshot0_results_gpt4_13:20:58.json', 'r') as file:
    #     predicted_results = json.load(file)      
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_grit_stateonly1_zeroshot0_results_gpt4_08:11:39.json', 'r') as file:
    #     predicted_results = json.load(file)  
   
  
    #----------------------LLM + GPT4----------------
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_gpt4_stateonly1_zeroshot1_results_gpt4_16:32:57.json', 'r') as file:
    #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_gpt4_stateonly1_zeroshot1_results_gpt4_15:36:28.json', 'r') as file:
    #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_gpt4_stateonly1_zeroshot1_results_gpt4_09:36:52.json', 'r') as file:
    #      predicted_results = json.load(file)   
    
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_gpt4_stateonly1_zeroshot0_results_gpt4P_09:12:10.json', 'r') as file:
    #     predicted_results = json.load(file)  
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_gpt4_stateonly1_zeroshot0_results_gpt4P_10:03:23.json', 'r') as file:
    #     predicted_results = json.load(file)      
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_gpt4_stateonly1_zeroshot0_results_gpt4_17:25:22.json', 'r') as file:
    #     predicted_results = json.load(file)     
    # with open('/home/sun/projects/cleanup-table/results/task1_llm_dense_gpt4_stateonly1_zeroshot0_results_gpt4_18:38:43.json', 'r') as file:
    #     predicted_results = json.load(file)      

    
    #--------------VLM----------zero shot----------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_vlm_dense_no_stateonly1_zeroshot1_results_gpt4_10:36:07.json', 'r') as file:
    #     predicted_results = json.load(file)     
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_dense_no_stateonly1_zeroshot1_results_gpt4_10:55:10.json', 'r') as file:
    #     predicted_results = json.load(file)  
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_dense_no_stateonly1_zeroshot1_results_gpt4_11:44:44.json', 'r') as file:
    #     predicted_results = json.load(file) 
    
    #------------------VLM------few shot----------------------          
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_vlm_dense_no_stateonly1_zeroshot0_results_gpt4_10:51:53.json', 'r') as file:
    #      predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_dense_no_stateonly1_zeroshot0_results_gpt4_12:10:05.json', 'r') as file:
    #      predicted_results = json.load(file)   
    
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_dense_no_stateonly1_zeroshot0_results_gpt4_12:24:39.json', 'r') as file:
    #      predicted_results = json.load(file)  
    
    #--------------------------------task 1--------------------------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_11:14:43.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/second-time/task1_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_19:22:25.json', 'r') as file:
    #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/third-time/task1_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_17:16:56.json', 'r') as file:
    #     predicted_results = json.load(file)   
    
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_11:38:05.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/second-time/task1_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_18:23:43.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/third-time/task1_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_16:51:12.json', 'r') as file:
    #     predicted_results = json.load(file)    
    
    
    #--------------------------------task 2--------------------------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task2_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_14:38:55.json', 'r') as file:
    #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/second-time/task2_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_19:54:57.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/third-time/task2_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_17:54:42.json', 'r') as file:
    #     predicted_results = json.load(file)   
    
    # with open('/home/sun/projects/cleanup-table/results/first-time/task2_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_12:19:12.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/second-time/task2_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_19:36:38.json', 'r') as file:
    #     predicted_results = json.load(file)
    # with open('/home/sun/projects/cleanup-table/results/third-time/task2_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_17:32:11.json', 'r') as file:
    #     predicted_results = json.load(file)
    
    #--------------------------------task 3--------------------------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task3_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_15:04:13.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/second-time/task3_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_20:25:01.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/third-time/task3_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_18:11:19.json', 'r') as file:
    #     predicted_results = json.load(file)    
    
    # with open('/home/sun/projects/cleanup-table/results/second-time/task3_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_20:44:26.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/first-time/task3_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_13:19:12.json', 'r') as file:
    #     predicted_results = json.load(file)  
    # with open('/home/sun/projects/cleanup-table/results/third-time/task3_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_18:33:05.json', 'r') as file:
    #     predicted_results = json.load(file) 
    
    
    
    #--------------------------------task 1--------------------------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_19:05:18.json', 'r') as file:
    #     predicted_results = json.load(file)  
    # with open('/home/sun/projects/cleanup-table/results/third-time/task1_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_13:31:16.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/second-time/task1_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_16:18:03.json', 'r') as file:
    #     predicted_results = json.load(file)   
    
    # with open('/home/sun/projects/cleanup-table/results/first-time/task1_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_12:27:19.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/second-time/task1_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_15:59:05.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/third-time/task1_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_12:44:38.json', 'r') as file:
    #     predicted_results = json.load(file)   
    
    #--------------------------------task 2--------------------------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task2_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_19:32:51.json', 'r') as file:
    #     predicted_results = json.load(file) 
    # with open('/home/sun/projects/cleanup-table/results/third-time/task2_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_13:59:00.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/second-time/task2_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_16:57:03.json', 'r') as file:
    #     predicted_results = json.load(file)   
    
    # with open('/home/sun/projects/cleanup-table/results/second-time/task2_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_17:26:07.json', 'r') as file:
    #     predicted_results = json.load(file)      
    # with open('/home/sun/projects/cleanup-table/results/first-time/task2_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_20:41:26.json', 'r') as file:
    #     predicted_results = json.load(file) 
    # with open('/home/sun/projects/cleanup-table/results/third-time/task2_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_14:43:26.json', 'r') as file:
    #     predicted_results = json.load(file)       
    
    #--------------------------------task 3--------------------------------------
    # with open('/home/sun/projects/cleanup-table/results/first-time/task3_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_19:59:47.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/second-time/task3_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_18:05:33.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/third-time/task3_llm_dense_grit_stateonly0_zeroshot0_results_gpt4_16:00:59.json', 'r') as file:
    #     predicted_results = json.load(file) 
    
    # with open('/home/sun/projects/cleanup-table/results/first-time/task3_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_20:21:49.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/second-time/task3_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_17:43:21.json', 'r') as file:
    #     predicted_results = json.load(file)   
    # with open('/home/sun/projects/cleanup-table/results/third-time/task3_llm_dense_grit_stateonly0_zeroshot1_results_gpt4_15:33:13.json', 'r') as file:
    #     predicted_results = json.load(file)    
        
    # -------------------no prompt reminder-----
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_dense_no_stateonly0_zeroshot0_results_gpt4_13:45:57.json', 'r') as file:
    #      predicted_results = json.load(file)          
    # with open('/home/sun/projects/cleanup-table/results/task1_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_14:30:25.json', 'r') as file:
    #     predicted_results = json.load(file)    
    # with open('/home/sun/projects/cleanup-table/results/task2_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_17:17:43.json', 'r') as file:
    #     predicted_results = json.load(file)
    
    with open('/home/sun/projects/cleanup-table/results/task3_vlm_dense_no_stateonly0_zeroshot1_results_gpt4_18:18:26.json', 'r') as file:
        predicted_results = json.load(file)
    
    
    
        
           
    #  # loading the annotation file and results
    # with open('/home/sun/projects/cleanup-table/results/vlm_kitchen_cskt0_zeroshot1_results.json', 'r') as file:
    #     label_results = json.load(file)
    with open('/home/sun/projects/cleanup-table/annotations/task3_annotations_xw.json', 'r') as file:
        label_results = json.load(file)

    state_only = 0
    evaluation(label_results, predicted_results, state_only)
    print("end the code")
