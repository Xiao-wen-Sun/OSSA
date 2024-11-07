prompt_state_only = '''
As the action planner for a household robot, your responsibility is to scan a table, identify each object present, and output them as JSON with a key:
* JSON{"name"}: you only allow to use the object category ('tray', 'box', 'can', 'salad', 'cafe', 'bread', 'plate', 'bowl', 'cup', 'bottle', 'knife', 'fork', 'spoon', 'chopsticks', 'napkin', 'orange', 'mango', 'apple', 'lemon', 'pear', 'peach', 'banana', 'watermelon','strawberry', 'grapes', 'soup') in there.
  In a special case, when two objects from the same category are placed on the table, they are labeled as name 1 and name 2, respectively.
  If multiple similar tiny objects are present on the table, you should create an entry for each one. 
  Exercise caution when dealing with a variety of chunked, sliced or diced items, or with liquids or semi-fluids served on a single plate or bowl. Since direct handling is not possible, consider the object and its container as a single entity for manipulation. 
Three keys exist in JSON{"name"}. 
* JSON{"name"}{"color"}: write the the object color.
* JSON{"name"}{"size"}: write the the object size. If there are multiple same objects, compare them and label them as 'small' 'medium', or 'big'.
* JSON{"name"}{"shape"}: write the the object shape. You have seven options: 'elongated', 'irregular', 'rectangular', 'square', 'oval', 'round', 'spherical', and 'cylindrical'.
* JSON{"name"}{"container"}: judge whether this object is a container or not. Write "true" or "false"
* JSON{"name"}{"state"}: There are three possibilities:
  If the object attribute is a container, its condition is classified into one of three states: 'clean', 'dirty', or 'containing leftover food'. A 'clean' status is assigned if the container is free of food residue. It is deemed 'dirty' when minor food residues are present. The designation 'containing leftover food' applies if substantial food pieces, perceived as edible, are found within.
  If the object attribute is not a container but is edible, its condition is described by one of three terms: 'intact', 'leftover food', 'peel. An 'intact' condition implies the object has not been altered through cutting or peeling. The term 'leftover food' is used when the object has been processed (diced, sliced, chopped, chunked, or peeled), suggesting it has been partially consumed.
  If the object attribute is not a container and is inedible (for example, a knife, fork, spoon, napkin), its condition is classified into one of two states: 'clean' or 'dirty'. The state is 'dirty' when minor food residues are present on the object, or if the object is inside or adjacent to food. Conversely, it is considered 'clean' if there is no surface residue on the object and no leftover food next to it.
 Please double-check your output is in JSON format, if not, convert it to JSON format.
 You should only return the JSON, without any explanation, symbol, or notes.
 '''
prompt_no_state = '''
As the action planner for a household robot in the kitchen, your responsibility is to scan a table, identify each object present, and output them as JSON with a key:
* JSON{"name"}: you only allow to use the object category ('tray', 'box', 'can', 'salad', 'cafe', 'bread', 'plate', 'bowl', 'cup', 'bottle', 'knife', 'fork', 'spoon', 'chopsticks', 'napkin', 'orange', 'mango', 'apple', 'lemon', 'pear', 'peach', 'banana', 'watermelon','strawberry', 'grapes', 'soup') in there.
  In a special case, when two objects from the same category are placed on the table, they are labeled as name 1 and name 2, respectively.
  If multiple similar tiny objects are present on the table, you should create an entry for each one. 
  Exercise caution when dealing with a variety of chunked, sliced or diced items, or with liquids or semi-fluids served on a single plate or bowl. Since direct handling is not possible, consider the object and its container as a single entity for manipulation. 
Three keys exist in JSON{"name"}. 
* JSON{"name"}{"color"}: write the the object color.
* JSON{"name"}{"size"}: write the the object size. If there are multiple same objects, compare them and label them as 'small' 'medium', or 'big'.
* JSON{"name"}{"shape"}: write the the object shape. You have seven options: 'elongated', 'irregular', 'rectangular', 'square', 'oval', 'round', 'spherical', and 'cylindrical'.
* JSON{"name"}{"container"}: judge whether this object is a container or not. Write "true" or "false"
* JSON{"name"}{"destination"}: Based on the state of this object and your common sense knowledge, determine the appropriate placement for the object, 
* JSON{"name"}{"grasping_type"}: Use your common sense knowledge and consider the object's size and shape to determine the best way for the robot arm to grasp it.
  You have three options: 'top grasp', 'edge grasp', and 'ungraspable'.
  For objects that are elongated and a small size, a 'top grasp' is adequate. 
  When the object is round and large, an 'edge grasp' becomes necessary. 
* JSON{"name"}{"placing_type"}: Based on the state of this object, decide on the action: 'pour' 'place' or 'uncertain'. 
 Please double-check your output is in JSON format, if not, convert it to JSON format.
 You should only return the JSON, without any explanation, symbol, or notes.
 '''
prompt_commands = '''
As the action planner for a household robot, your responsibility is to scan a table, identify each object present, and output them as JSON with a key:
* JSON{"name"}: you only allow to use the object category ('tray', 'box', 'can', 'salad', 'cafe', 'bread', 'plate', 'bowl', 'cup', 'bottle', 'knife', 'fork', 'spoon', 'chopsticks', 'napkin', 'orange', 'mango', 'apple', 'lemon', 'pear', 'peach', 'banana', 'watermelon','strawberry', 'grapes', 'soup') in there.
  In a special case, when two objects from the same category are placed on the table, they are labeled as name 1 and name 2, respectively.
  If multiple similar tiny objects are present on the table, you should create an entry for each one. 
  Exercise caution when dealing with a variety of chunked, sliced or diced items, or with liquids or semi-fluids served on a single plate or bowl. Since direct handling is not possible, consider the object and its container as a single entity for manipulation. 
Three keys exist in JSON{"name"}. 
* JSON{"name"}{"color"}: write the the object color.
* JSON{"name"}{"size"}: write the the object size. If there are multiple same objects, compare them and label them as 'small' 'medium', or 'big'.
* JSON{"name"}{"shape"}: write the the object shape. You have seven options: 'elongated', 'irregular', 'rectangular', 'square', 'oval', 'round', 'spherical', and 'cylindrical'.
* JSON{"name"}{"container"}: judge whether this object is a container or not. Write "true" or "false"
* JSON{"name"}{"state"}: There are three possibilities:
  If the object attribute is a container, its condition is classified into one of three states: 'clean', 'dirty', or 'containing leftover food'. A 'clean' status is assigned if the container is free of food residue. It is deemed 'dirty' when minor food residues are present. The designation 'containing leftover food' applies if substantial food pieces, perceived as edible, are found within.
  If the object attribute is not a container but is edible, its condition is described by one of three terms: 'intact', 'leftover food', 'peel'. An 'intact' condition implies the object has not been altered through cutting or peeling. The term 'leftover food' is used when the object has been processed (diced, sliced, chopped, chunked, or peeled), suggesting it has been partially consumed. The term 'peel' is fruit peel.
  If the object attribute is not a container and is inedible (for example, a knife, fork, spoon, napkin), its condition is classified into one of two states: 'clean' or 'dirty'. The state is 'dirty' when minor food residues are present on the object, or if the object is inside or adjacent to food. Conversely, it is considered 'clean' if there is no surface residue on the object and no leftover food next to it.
* JSON{"name"}{"destination"}: Based on the state of this object and your common sense knowledge, determine the appropriate placement for the object, 'trash bin', 'fridge', 'cupboard', 'dishwasher'.
  please keep the 'clean' and 'intact' objects in the 'cupboard'.
  Different user has different preferences to deal with the 'leftover food'. You need to base it on the user instructions too. 
  If the user instruction includes "keep all the leftover food", the destination of this object is 'fridge'.
  If the user instruction includes "discard all the leftover food", the destination of this object is the 'trash bin'.
  If the user does not give specific instructions for the leftover food, the destination of this object is 'uncertain'. 
* JSON{"name"}{"grasping_type"}: Use your common sense knowledge and consider the object's size and shape to determine the best way for the robot arm to grasp it.
  You have three options: 'top grasp', 'edge grasp', and 'ungraspable'.
  For objects that are elongated and a small size, a 'top grasp' is adequate. 
  When the object is round and large, an 'edge grasp' becomes necessary. 
  As for leftover food that is in a liquid, semi-fluid state, or has been sliced, chunked, or diced, it is 'ungraspable'.
* JSON{"name"}{"placing_type"}: Based on the state of this object, decide on the action: 'pour' 'place' or 'uncertain'. 
  If the destination is 'uncertain' the action should also be 'uncertain'.
  If the container has leftovers and the destination is a trash bin, the action should be 'pour'; otherwise, simply 'place' it.
 Please double-check your output is in JSON format, if not, convert it to JSON format.
 You should only return the JSON, without any explanation, symbol, or notes.
 '''
 
plain_prompt = '''
As the action planner for a household robot, your responsibility is to scan a table, identify each object present, and output them as JSON with a key:
* JSON{"name"}: you only allow to use the object category ('tray', 'box', 'can', 'salad', 'cafe', 'bread', 'plate', 'bowl', 'cup', 'bottle', 'knife', 'fork', 'spoon', 'chopsticks', 'napkin', 'orange', 'mango', 'apple', 'lemon', 'pear', 'peach', 'banana', 'watermelon','strawberry', 'grapes', 'soup') in there.
  In a special case, when two objects from the same category are placed on the table, they are labeled as name 1 and name 2, respectively.
  If multiple similar tiny objects are present on the table, you should create an entry for each one. 
  Exercise caution when dealing with a variety of chunked, sliced or diced items, or with liquids or semi-fluids served on a single plate or bowl. Since direct handling is not possible, consider the object and its container as a single entity for manipulation. 
Three keys exist in JSON{"name"}. 
* JSON{"name"}{"color"}: 
* JSON{"name"}{"size"}:  
* JSON{"name"}{"shape"}:  
* JSON{"name"}{"container"}: 
* JSON{"name"}{"state"}: 
* JSON{"name"}{"destination"}:  
* JSON{"name"}{"grasping_type"}: 
* JSON{"name"}{"placing_type"}: 
 Please double-check your output is in JSON format, if not, convert it to JSON format.
 You should only return the JSON, without any explanation, symbol, or notes.
 '''
# plain_prompt = '''
# As the action planner for a household robot, your responsibility is to scan a table, identify each object present, and output them as JSON with a key:
# * JSON{"name"}: you only allow to use the object category ('tray', 'box', 'can', 'salad', 'cafe', 'bread', 'plate', 'bowl', 'cup', 'bottle', 'knife', 'fork', 'spoon', 'chopsticks', 'napkin', 'orange', 'mango', 'apple', 'lemon', 'pear', 'peach', 'banana', 'watermelon','strawberry', 'grapes', 'soup') in there.
#   In a special case, when two objects from the same category are placed on the table, they are labeled as name 1 and name 2, respectively.
#   If multiple similar tiny objects are present on the table, you should create an entry for each one. 
#   Exercise caution when dealing with a variety of chunked, sliced or diced items, or with liquids or semi-fluids served on a single plate or bowl. Since direct handling is not possible, consider the object and its container as a single entity for manipulation. 
# Three keys exist in JSON{"name"}. 
# * JSON{"name"}{"color"}: write the the object color.
# * JSON{"name"}{"size"}:  'small' 'medium', or 'big'.
# * JSON{"name"}{"shape"}:  You have seven options: 'elongated', 'irregular', 'rectangular', 'square', 'oval', 'round', 'spherical', and 'cylindrical'.
# * JSON{"name"}{"container"}: "true" or "false"
# * JSON{"name"}{"state"}: you have six options: 'clean', 'dirty', 'containing leftover food', 'intact', 'leftover food', 'peel'. 
# * JSON{"name"}{"destination"}: you have five options: 'dishwasher', 'cupboard', 'fridge', 'trash bin', 'uncertain'. 
# * JSON{"name"}{"grasping_type"}: You have three options: 'top grasp', 'edge grasp', and 'ungraspable'.
# * JSON{"name"}{"placing_type"}: 'pour' 'place' or 'uncertain'. 
#  Please double-check your output is in JSON format, if not, convert it to JSON format.
#  You should only return the JSON, without any explanation, symbol, or notes.
#  '''
 
vision_prompt = "You are a robot's eyes, your job is to describe each independent object on the table. The more details, the better." 

scene_description = '''
    From the top left of the image, I see an open bag of cereal.  This is one independent object: 1. An open bag of cereal. The total objects number is 1;
    To the right, I see a white plate with a piece of bread sliced in half and topped with seeds. I will count it as two independent objects: 2. A piece of sliced bread. 3.  A dirty plate, The total object number is 1 + 2 = 3;
    To the right, I see two stacked white plates with a small spoon, a big spoon, a knife, and a fork, The plates look clean, so I guess they are never to be used. I will count it as 6 independent objects: 4. A clean knife, 5.  A clean fork, 6. A small and clean spoon, 7. A big and clean spoon, 8. Clean Plate 1 and 9. Clean Plate 2. The total objects number is 3 + 6 = 9;
    To the right, there is an edge of the table. 
    From the middle left, I see a piece of flat napkin. This is one independent object: 10. A piece of flat napkin. The total objects number is 9 + 1 = 10;
    To the right, I see a white mug, and there is nothing inside. This is one independent object: 11. An empty mug. The total Objects number is 10 + 1 = 11;
    To the right, I see a white plate with two bananas and an orange. I will count it as 4 independent objects: 12. Intact Banana 1, 13. Intact Banana 2, 14. A Intact orange, 15. A dirty plate. The total objects number is 11 + 4 = 15;
    To the right, I see a glass, but I can not clarify if there's water inside or not. This is one independent object: 16. A glass. The total Objects number is 15 + 1 = 16;
    To the right, I see a bowl with soup and a metal strip. It is a spoon. Based on common sense knowledge, the hand cannot simultaneously grasp liquid directly, and bacteria on the hands will contaminate food. Typically, to transport these small pieces, we move the container holding them instead. Therefore, I will count it as two independent objects:17. A dirty spoon and 18. A bowl with soup. The total objects number is 16 + 2 = 18;
    To the right, there is an edge of the table. 
    From the bottom left, I see a green bow with three intact apples. I will count it as 4 independent objects: 19. A Intact red apple 1, 20. A Intact red apple 2, 21. Green apple, and 22. Green bowl. The total objects number is 18 + 4 = 22;
    To the right, I see a half-apple, a half-orange, and an orange peel. I will count it as three independent objects: 23. A half apple, 24. A half orange, and 25, orange peel. The total objects number is 22 + 3 = 25;
    To the right, I see a plate with sliced apples, a knife, and a fork. The knife and the fork are placed together on the plate with sliced apples, which indicates they have been used. Based on common sense knowledge, the hand cannot simultaneously grasp numerous small food items and Bacteria on the hands may contaminate food. Typically, to transport these small pieces, we move the container holding them instead. I will count them as 3 independent objects: 26. A dirty knife, and 27. A dirty fork. 28. The plate with many small pieces of apples. The total objects number is 25 + 3 = 28;
    To the right, I see a banana peel. There is one independent object: 29. A banana peel. The total objects number is 28 + 1 = 29;
    To the right, I see a crimped napkin. There is one independent object: 30. A crimped napkin. The total objects number is 29 + 1 = 30;
    To the right, there is an edge of the table. To the bottom, there is an edge of the table. 
    There are a total of 30 independent objects on the table.
    1. An open bag of cereal. 
    2. A piece of sliced bread. 
    3. A plate with piece of sliced bread.
    4. A clean knife.
    5.  A clean fork.
    6. A small and clean spoon.
    7. A big and clean spoon. 
    8. Clean Plate 1.
    9. Clean Plate 2. 
    10. A piece of flat napkin. 
    11. An empty mug. 
    12. Intact Banana 1.
    13. Intact Banana 2.
    14. A Intact orange. 
    15. A dirty plate. 
    16. A glass. 
    17. A dirty spoon.
    18. A bowl with soup. 
    19. A Intact red apple 1.
    20. A Intact red apple 2.
    21. A Intact green apple.
    22. A dirty green bowl. 
    23. A half apple. 
    24. A half-orange.
    25, Orange peels. 
    26. A dirty knife. 
    27. A dirty fork. 
    28. A plate with many small pieces of apples. 
    29. A banana peel. 
    30. A crimped napkin.
'''
example_scene_description = '''
    1. A bunch of two intact bananas.
    2. A white cup filled with a liquid that appears to be coffee, featuring a cream design on the surface.
    3. A white bowl containing a brown liquid, likely a type of soup or sauce.
    4. A white plate with several sliced pieces of banana scattered on it.
    5. A small piece of banana on the table, separate from the plate.
    '''
stateonly_example = '''
JSON{
    "cup 1": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
  },
  "plate": {
    "color": "white",
    "size": "large",
    "shape": "round",
    "container": "true",
    "state": "containing leftover food",
  },
  "banana": {
    "color": "yellow",
    "size": "medium",
    "shape": "elongated",
    "container": "false",
    "state": "intact",
  },
  "cup 2": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
  }
}
'''

task1 = "clear the table."
scene_planner1 = '''
JSON{
    "cup 1": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
    "destination": "uncertain",
    "grasping_type": "top grasp",
    "placing_type": "uncertain"
  },
  "plate": {
    "color": "white",
    "size": "medium",
    "shape": "round",
    "container": "true",
    "state": "containing leftover food",
    "destination": "uncertain",
    "grasping_type": "edge grasp",
    "placing_type": "uncertain"
  },
  "banana": {
    "color": "yellow",
    "size": "medium",
    "shape": "elongated",
    "container": "false",
    "state": "intact",
    "destination": "cupboard",
    "grasping_type": "top grasp",
    "placing_type": "place"
  },
  "cup2": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
    "destination": "uncertain",
    "grasping_type": "top grasp",
    "placing_type": "uncertain"
  }
}
'''


task2 = "Help me clear the table and keep all the leftover food."
scene_planner2 = '''
JSON{
    "cup 1": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
    "destination": "fridge",
    "grasping_type": "top grasp",
    "placing_type": "place"
  },
  "plate": {
    "color": "white",
    "size": "medium",
    "shape": "round",
    "container": "true",
    "state": "containing leftover food",
    "destination": "fridge",
    "grasping_type": "edge grasp",
    "placing_type": "place"
  },
  "banana": {
    "color": "yellow",
    "size": "medium",
    "shape": "elongated",
    "container": "false",
    "state": "intact",
    "destination": "cupboard",
    "grasping_type": "top grasp",
    "placing_type": "place"
  },
  "cup2": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
    "destination": "fridge",
    "grasping_type": "top grasp",
    "placing_type": "place"
  }
}
'''


task3 = "clear the table and discard all the leftover food."
scene_planner3 = '''
JSON{
    "cup 1": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
    "destination": "trash bin",
    "grasping_type": "top grasp",
    "placing_type": "pour"
  },
  "plate": {
    "color": "white",
    "size": "medium",
    "shape": "round",
    "container": "true",
    "state": "containing leftover food",
    "destination": "trash bin",
    "grasping_type": "edge grasp",
    "placing_type": "pour"
  },
  "banana": {
    "color": "yellow",
    "size": "medium",
    "shape": "elongated",
    "container": "false",
    "state": "intact",
    "destination": "cupboard",
    "grasping_type": "top grasp",
    "placing_type": "place"
  },
  "cup2": {
    "color": "white",
    "size": "small",
    "shape": "cylindrical",
    "container": "true",
    "state": "containing leftover food",
    "destination": "trash bin",
    "grasping_type": "top grasp",
    "placing_type": "pour"
  }
}
'''


# # # Counting the tokens
# num_tokens_example = len(vlm_scene_planner3.split())
# print(num_tokens_example)
