'''
 Author: Alexandre Ferri
 Created on Mon Dec 09 2019
'''

from flask import Blueprint, request, jsonify
from .extentions import db
import cv2
import os
import io
import numpy as np
import base64
import PIL.Image as Image

bp_capture = Blueprint('capture', __name__)
classfier = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eyeClassifier = cv2.CascadeClassifier("haarcascade-eye.xml")

width, height = 220, 220

@bp_capture.route('/api/insert/<id>/<number>', methods=['POST'])
def insert_image(id, number):
    r = request.get_json()
    imgStr = base64.b64decode(r['img'])

    #  convert binary data to numpy array
    nparr = np.fromstring(imgStr, np.uint8)

    #  let opencv decode image to correct format
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img1 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detectedFaces = classfier.detectMultiScale(grayImg, scaleFactor=1.5, minSize=(150,150))

    pictureSaved = False

    for (x, y, l, a) in detectedFaces:
        # region = img[y:y + a, x:x + l]
        # grayRegionEye = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        # detectedEyes = eyeClassifier.detectMultiScale(grayRegionEye)

        # for (ox, oy, ol, oa) in detectedEyes:
        if np.average(grayImg) > 100:
            faceImage = cv2.resize(grayImg[y:y + a, x:x + l], (width, height))
            
            # blob_client = blob_service_client.get_blob_client(container=container_name, blob="pessoa." + str(id) + "." + str(number) + ".jpg")
            # blob_client.upload_blob(b)

            cv2.imwrite("fotos/pessoa." + str(id) + "." + str(number) + ".jpg", faceImage)

            imgSave = cv2.resize(img, (200, 200))
            cv2.imwrite("originais/pessoa." + str(id) + "." + str(number) + ".jpg", imgSave)

            pictureSaved = True

            print("[Foto: " + str(number) + " capturada com sucesso]")

            # break
    
    if pictureSaved:
        resp = {'success': True, 'msg': 'Foto capturada com sucesso'}
        return jsonify(resp), 200
    else:
        resp = {'success': False, 'msg': 'Foto não reconhecida'}
        return jsonify(resp), 201





@bp_capture.route('/api/pictures/<id>', methods=['GET'])
def return_images(id):
    paths = [os.path.join("originais", f) for f in os.listdir("originais")]
    images = []

    for path in paths:
        picId = int(os.path.split(path)[-1].split('.')[1])

        if int(picId) == int(id):
            img1 = cv2.imread(path)
            img2 = cv2.resize(img1, (200, 200))
            img = cv2.rotate(img2, cv2.ROTATE_90_CLOCKWISE)
            pic = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

            images.append(pic)
    
    result = {'pictures': images}

    return jsonify(result), 200


    

@bp_capture.route('/api/remove/pictures/<id>', methods=['PUT'])
def remove_images(id):

    paths = [os.path.join("fotos", f) for f in os.listdir("fotos")]
    for path in paths:
        picId = int(os.path.split(path)[-1].split('.')[1])
        if int(picId) == int(id):
            os.remove(path)

    paths = [os.path.join("originais", f) for f in os.listdir("originais")]
    for path in paths:
        picId = int(os.path.split(path)[-1].split('.')[1])
        if int(picId) == int(id):
            os.remove(path)
    
    result = {'success': True}
    return jsonify(result), 200




@bp_capture.route('/api/rename', methods=['GET'])
def rename_images():
    paths = [os.path.join("mudar", f) for f in os.listdir("mudar")]

    id = 6
    number = 0
    
    for path in paths:
        number += 1

        if int(number) == 6:
            number = 1
            id += 1

        img = cv2.imread(path)
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detectedFaces = classfier.detectMultiScale(grayImg, scaleFactor=1.5, minSize=(150,150))

        pictureSaved = False

        for (x, y, l, a) in detectedFaces:
            region = img[y:y + a, x:x + l]
            grayRegionEye = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            detectedEyes = eyeClassifier.detectMultiScale(grayRegionEye)

            for (ox, oy, ol, oa) in detectedEyes:
                if np.average(grayImg) > 100:
                    faceImage = cv2.resize(grayImg[y:y + a, x:x + l], (width, height))

                    cv2.imwrite("fotos/pessoa." + str(id) + "." + str(number) + ".jpg", faceImage)
                    
                    pictureSaved = True

                break

        # os.rename(path, "mudar/pessoa." + str(id) + "." + str(number) + ".jpg")
        
    result = {'success': True}
    return jsonify(result), 200