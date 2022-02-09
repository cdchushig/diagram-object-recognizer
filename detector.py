import cv2 as cv
import json
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import numpy as np
from PIL import Image
import pathlib
import logging
import coloredlogs

PATH_DIR_PROJECT = str(pathlib.Path(__file__).parent.resolve())

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class Detector:

	def __init__(self):
		config_file_path = PATH_DIR_PROJECT + '/models/config.yml'
		weights_path = PATH_DIR_PROJECT + '/models/detectron2_uml_model.pth'
		self.cfg = get_cfg()
		self.cfg.merge_from_file(config_file_path)
		self.cfg.MODEL.WEIGHTS = weights_path
		self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
		self.cfg.MODEL.DEVICE = "cpu"

	def inference(self, file):

		logger.info("inference")
		predictor = DefaultPredictor(self.cfg)
		im = cv.imread(file)
		outputs = predictor(im)

		# with open(self.curr_dir+'/data.txt', 'w') as fp:
		# 	json.dump(outputs['instances'], fp)
		# 	# json.dump(cfg.dump(), fp)

		# get metadata
		MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes = ['actor', 'oval', 'line', 'text', 'arrow', 'system']
		metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])

		# visualise
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.2)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

		print(outputs['instances'])

		class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
		pred_class_names = list(map(lambda x: class_names[x], outputs['instances'].pred_classes))

		list_nodes = []

		for pred_class, score, pred_class_name, pred_box in zip(outputs['instances'].pred_classes, outputs['instances'].scores, pred_class_names, outputs['instances'].pred_boxes):
			dict_node = {
				"pred_class": int(pred_class.numpy()),
				"pred_class_name": pred_class_name,
				"score": float(score.numpy()),
				"pred_box": json.dumps(pred_box.numpy().tolist())
			}
			list_nodes.append(dict_node)

		dict_nodes = {
			"nodes": list_nodes,
			"version": "1.0"
		}

		img = Image.fromarray(np.uint8(v.get_image()[:, :, ::-1]))
		# write to jpg
		# cv.imwrite('img.jpg',v.get_image())
		return img, dict_nodes
