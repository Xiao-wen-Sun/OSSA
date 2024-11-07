from detectron2.engine.defaults import DefaultPredictor
import argparse
import sys
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
sys.path.insert(0, 'grit/third_party/CenterNet2/projects/CenterNet2/')
from centernet.config import add_centernet_config
from grit.config import add_grit_config
#/home/sun/projects/cleanup-table/GriT/third_party/CenterNet2/projects/CenterNet2/centernet/modeling/dense_heads/centernet.py
def setup_cfg(args):
    cfg = get_cfg()
    if args.cpu:
        cfg.MODEL.DEVICE="cpu"
    add_centernet_config(cfg)
    add_grit_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    if args.test_task:
        cfg.MODEL.TEST_TASK = args.test_task
    cfg.MODEL.BEAM_SIZE = 1
    cfg.MODEL.ROI_HEADS.SOFT_NMS_ENABLED = False
    cfg.USE_ACT_CHECKPOINT = False
    cfg.freeze()
    return cfg
def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="grit/configs/GRiT_B_DenseCap_ObjectDet.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--cpu", action='store_true', help="Use CPU only.")
    parser.add_argument(
        "--input",
        nargs="+",
        default='/home/sun/Projects_Learning/GriT/demo_images',
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        # default="results.txt",
        default="visualization",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--test-task",
        type=str,
        default='DenseCap',
        help="Choose a task to have GRiT perform",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=['MODEL.WEIGHTS', 'grit/models/grit_b_densecap_objectdet.pth'],
        nargs=argparse.REMAINDER,
    )
    return parser

args = get_parser().parse_args()

cfg = setup_cfg(args)

predictor = DefaultPredictor(cfg)
# image_path = '/home/sun/projects/cleanup-table/imgs/example_scene.jpg'
image_path = '/home/sun/projects/cleanup-table/datasets/sim_dataset/scene12.png'
img = read_image(image_path, format="BGR")
predictions = predictor(img)
predictions_list = predictions['instances'].pred_object_descriptions.data
print(predictions)