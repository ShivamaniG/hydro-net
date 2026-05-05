import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
import utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['RESULT_FOLDER'] = 'app/static/results'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Load image
            image = cv2.imread(filepath)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Get parameters from form
            method = request.form.get('method', 'model') # 'model' or 'ndwi'
            algo = request.form.get('algo', 'a_star')

            try:
                start_x = int(request.form.get('start_x', 0))
                start_y = int(request.form.get('start_y', 0))
                goal_x = int(request.form.get('goal_x', image.shape[1]-1))
                goal_y = int(request.form.get('goal_y', image.shape[0]-1))
            except ValueError:
                return render_template('index.html', error='Invalid coordinates')

            start_node = (start_x, start_y)
            goal_node = (goal_x, goal_y)

            # 1. Segmentation
            if method == 'ndwi':
                mask = utils.get_water_mask_ndwi(image_rgb)
            else:
                mask = utils.get_water_mask_model(image_rgb)

            # 2. Pathfinding
            path = utils.pathfinding_search(mask, start_node, goal_node, algorithm=algo)

            # 3. Visualization
            vis_img = utils.generate_visual_output(image_rgb, mask, path, start_node, goal_node)

            result_filename = 'result_' + filename
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            cv2.imwrite(result_path, cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR))

            return render_template('index.html',
                                   original_img=url_for('static_file', filename='uploads/' + filename),
                                   result_img=url_for('static_file', filename='results/' + result_filename),
                                   path_found=len(path) > 0)

    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
