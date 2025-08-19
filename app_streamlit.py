import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import io

# Load model and label map
PATH_TO_SAVED_MODEL = "./saved_model"
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

# Helper for detection
@st.cache_resource
def get_category_index():
    from utils import label_map_util
    PATH_TO_LABELS = "./data/mscoco_label_map.pbtxt"
    NUM_CLASSES = 90
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    return label_map_util.create_category_index(categories)
category_index = get_category_index()

from utils import visualization_utils as vis_util

def run_inference(image_np):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    image_np_with_detections = image_np.copy()
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.30)
    return image_np_with_detections

st.title("Image Detection with TensorFlow & Streamlit")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    image_np = np.array(image)
    st.write("Running detection...")
    result_image_np = run_inference(image_np)
    result_image = Image.fromarray(result_image_np)
    st.image(result_image, caption="Detection Result", use_column_width=True)
