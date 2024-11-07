from detectron2.engine.defaults import DefaultPredictor
import sys
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
sys.path.insert(0, 'grit/third_party/CenterNet2/projects/CenterNet2/')
from centernet.config import add_centernet_config
from grit.grit.config import add_grit_config

def setup_cfg():
    cfg = get_cfg()
    cfg.MODEL.DEVICE="cpu"
    add_centernet_config(cfg)
    add_grit_config(cfg)
    cfg.merge_from_file('grit/configs/GRiT_B_DenseCap_ObjectDet.yaml')
    cfg.merge_from_list(['MODEL.WEIGHTS', 'grit/models/grit_b_densecap_objectdet.pth'])
    # Set score_threshold for builtin models
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.1
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = 0.1
    cfg.MODEL.TEST_TASK = 'DenseCap'
    cfg.MODEL.BEAM_SIZE = 1
    cfg.MODEL.ROI_HEADS.SOFT_NMS_ENABLED = False
    cfg.USE_ACT_CHECKPOINT = False
    cfg.freeze()
    return cfg

cfg = setup_cfg()

predictor = DefaultPredictor(cfg)
# image_path = '/home/sun/projects/cleanup-table/imgs/example_scene.jpg'
image_path = '/home/sun/projects/cleanup-table/datasets/sim_dataset/scene12.png'
img = read_image(image_path, format="BGR")
predictions = predictor(img)

boxes = predictions['instances'].pred_boxes if predictions['instances'].has("pred_boxes") else None
classes = predictions['instances'].pred_classes.tolist() if predictions['instances'].has("pred_classes") else None
predictions_list = predictions['instances'].pred_object_descriptions.data if predictions['instances'].has("pred_object_descriptions") else None
print("boxes: ", boxes)
print("classes: ", classes)
print("predictions_list: ", predictions_list)