from bson.binary import Binary, USER_DEFINED_SUBTYPE
import pickle

from common.logger import get_logger
from database.entities.datasetentities import DatasetImage, DatasetLabel, DatasetLabelName

my_logger = get_logger(__name__)

CIFAR_COL_ANNOTATION = 'cifar_annotations'
CIFAR_COL_IMAGES = 'cifar_images'
CIFAR_COL_LABELS = 'cifar_labels'


class CifarCollections(object):
    def __init__(self, col_annotation, col_images, col_labels):
        self.col_annotation = col_annotation
        self.col_images = col_images
        self.col_labels = col_labels

    def insert_annotation_data(self, annotation_data):
        my_logger.info("Attempting to insert label with image_id " + str(annotation_data.get_image_id()))
        annotation_data = annotation_data.__dict__
        self.col_annotation.insert_one(annotation_data)
        my_logger.info("Label has been inserted for image_id " + str(annotation_data['image_id']))

    def insert_image_data(self, image_data):
        my_logger.info("Attempting to insert image with image_id " + str(image_data.get_image_id()))
        image_data = image_data.__dict__
        image_data['image'] = Binary(pickle.dumps(image_data['image']), subtype=USER_DEFINED_SUBTYPE)
        self.col_images.insert_one(image_data)
        my_logger.info("Image has been inserted for image_id " + str(image_data['image_id']))

    def insert_labels_data(self, label_data):
        my_logger.info("Attempting to insert label name " + label_data.get_name())
        label_data = label_data.__dict__
        self.col_labels.insert_one(label_data)
        my_logger.info("Label names has been inserted with name" + label_data['name'])

    def find_annotation_data(self, find_build):
        results = self.col_annotation.find(find_build)
        if results is None:
            return None
        dataset = list()
        for data in list(results):
            dataset.append(DatasetLabel(data['image_id'], data['source'], data['type'], data['label']))
        return dataset
        my_logger.info("Annotation count found: " + str(len(dataset)))

    def find_image_data(self, find_build):
        results = self.col_images.find(find_build)
        if results is None:
            return None
        dataset = list()
        for data in list(results):
            dataset.append(DatasetImage(data['image_id'], data['filename'], pickle.loads(data['image'])))
        return dataset
        my_logger.info("Images count found: " + str(len(dataset)))

    def find_label_data(self, find_build):
        results = self.col_labels.find(find_build)
        if results is None:
            return None
        dataset = list()
        for data in list(results):
            dataset.append(DatasetLabelName(data['source'], data['index'], data['name']))
        return dataset
        my_logger.info("Label count found: " + str(len(dataset)))
