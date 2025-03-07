import os

from flask import Blueprint, request, jsonify, send_file, abort

from data.upload_tools.upload_image import upload_image

blueprint = Blueprint('img_api', __name__, template_folder='templates')


@blueprint.route('/api/get_img')
def get_img():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ['path']):
        return jsonify({'error': 'Bad request'})
    if not os.path.exists(request.json['path']):
        return jsonify({'error': 'Path does not exist'})
    try:
        return send_file(request.json['path'])
    except FileNotFoundError:
        abort(404)


@blueprint.route('/api/send_img', methods=['POST'])
def send_img():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    saved_img_path = upload_image(request.files['file'])
    if not saved_img_path:
        return jsonify({'error': 'Upload img error'})
    return jsonify({'path': saved_img_path})
