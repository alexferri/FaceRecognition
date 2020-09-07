'''
 Author: Alexandre Ferri
 Created on Mon Dec 09 2019
'''

from flask import Blueprint, request, jsonify
import cv2
import os
import numpy as np

bp_training = Blueprint('training', __name__)
lbph = cv2.face.LBPHFaceRecognizer_create(threshold=50)

def getImagesWithId():
    paths = [os.path.join("fotos", f) for f in os.listdir("fotos")]
    faces = []
    ids = []
    for path in paths:
        imgFace = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
        id = int(os.path.split(path)[-1].split('.')[1])

        ids.append(id)
        faces.append(imgFace)

    return np.array(ids), faces

@bp_training.route('/api/training', methods=['PUT'])
def train():
    print("Training...")

    ids, faces = getImagesWithId()

    lbph.train(faces, ids)
    lbph.write('classifierLBPH.yml')

    print('Done!')

    return jsonify({'success': True}), 200
