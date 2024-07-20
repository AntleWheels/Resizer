from flask import Flask, render_template, request, jsonify, send_file
from process import resize_image, compress_image
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize():
    if 'image' not in request.files:
        return jsonify({'error': 'Image is required'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    width = request.form.get('width', type=int)
    height = request.form.get('height', type=int)

    img_io = resize_image(file, width, height)
    
    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='resized.jpg')

@app.route('/compress', methods=['POST'])
def compress():
    if 'image' not in request.files:
        return jsonify({'error': 'Image is required'}), 400
    if 'size' not in request.form:
        return jsonify({'error': 'Size is required'}), 400
    if 'unit' not in request.form:
        return jsonify({'error': 'Unit is required'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        target_size = float(request.form['size'])
    except ValueError:
        return jsonify({'error': 'Invalid size'}), 400

    unit = request.form['unit']
    if unit == 'KB':
        target_size_kb = target_size
    elif unit == 'MB':
        target_size_kb = target_size * 1024
    else:
        return jsonify({'error': 'Invalid unit'}), 400

    img_io = compress_image(file, target_size_kb)
    
    if img_io is None:
        return jsonify({'error': 'Could not compress image to desired size'}), 400

    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='compressed.jpg')

if __name__ == '__main__':
    app.run(debug=True)
