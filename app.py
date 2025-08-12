from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import os
import sys
import tensorflow as tf
from PIL import Image
import time

sys.path.append("..")
from utils import label_map_util
from utils import visualization_utils as vis_util
# setting our tf log level and settings
tf.get_logger().setLevel('ERROR')

PATH_TO_SAVED_MODEL = "./saved_model"
PATH_TO_LABELS = "./data/mscoco_label_map.pbtxt"
NUM_CLASSES = 90
#loading label map (.pbtxt file)
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


print("Number of GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

print('Loading model...', end='')
start_time = time.time()




end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds' .format(elapsed_time))

# flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

# Load the saved model once
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

def inference(image_np):
    # input needs to be a tensor, convert it using `tf.convert_to_tensor`
    input_tensor = tf.convert_to_tensor(image_np)
    # The model expects a batch of images, so add an axis with `tf.expand_dims`
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = detect_fn(input_tensor)
    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key:value[0, :num_detections].numpy() 
                  for key,value in detections.items()}
    detections['num_detections'] = num_detections
    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    image_np_with_detections = image_np.copy()
    viz_util.visualize_boxes_and_labels_on_image_array(
          image_np_with_detections,
          detections['detection_boxes'],
          detections['detection_classes'],
          detections['detection_scores'],
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw=200,
          min_score_thresh=.30,
          agnostic_model=False)
    return (image_np_with_detections)

# adding function to display index page
@app.route('/')
def index():
    return render_template('index.html')

# ...existing code...


# upload and display function
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Run inference and save result
        image_np = np.array(Image.open(filepath))
        image_np_inferenced = inference(image_np)
        im = Image.fromarray(image_np_inferenced)
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
        im.save(result_path)
        return render_template('index.html', result_image='result_' + filename)
    return render_template('index.html', error='Invalid file type.')

# serve result image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)