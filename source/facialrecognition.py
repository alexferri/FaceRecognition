'''
 Author: Alexandre Ferri
 Created on Mon Dec 09 2019
'''

from flask import Blueprint, request, Response, jsonify
from .extentions import db
from datetime import datetime
import cv2
import numpy as np
import base64

bp_recognition = Blueprint('recognition', __name__)
faceDetector = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")

width, height = 220, 220

@bp_recognition.route('/api/recognize', methods=['POST'])
def recognize():
    recognizer = cv2.face.LBPHFaceRecognizer_create(threshold=50)
    recognizer.read("classifierLBPH.yml")

    r = request.get_json()
    imgStr = base64.b64decode(r['img'])

    # convert string of image data to uint8
    nparr = np.fromstring(imgStr, np.uint8)

    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # img = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

    greyImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    detectedFaces = faceDetector.detectMultiScale(greyImage, scaleFactor=1.5, minSize=(150,150))

    if len(detectedFaces) > 0:
        for (x, y, l, a) in detectedFaces:
            faceImage = cv2.resize(greyImage[y:y + a, x:x + l], (width, height))
            id, confianca = recognizer.predict(faceImage)

            percent = round(100 - confianca)

            print(id) 
            print("{0}%".format(percent))

            if int(percent) >= 55:
                return getUserById(id)
            else:
                return jsonify({'success': True, 'msg': 'Face não identificada!', 'adm': False}), 202

    else:
        return jsonify({'success': False, 'msg': 'Face não identificada!', 'adm': False}), 201



@bp_recognition.route('/api/recognizeIpad', methods=['POST'])
def recognizeIpad():
    recognizer = cv2.face.LBPHFaceRecognizer_create(threshold=50)
    recognizer.read("classifierLBPH.yml")

    r = request.get_json()
    imgStr = base64.b64decode(r['img'])

    # convert string of image data to uint8
    nparr = np.fromstring(imgStr, np.uint8)

    # decode image
    img1 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

    greyImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    detectedFaces = faceDetector.detectMultiScale(greyImage, scaleFactor=1.5, minSize=(150,150))

    if len(detectedFaces) > 0:
        for (x, y, l, a) in detectedFaces:
            faceImage = cv2.resize(greyImage[y:y + a, x:x + l], (width, height))
            id, confianca = recognizer.predict(faceImage)

            percent = round(100 - confianca)

            print(id) 
            print("{0}%".format(percent))

            if int(percent) >= 55:
                return getUserById(id)
            else:
                return jsonify({'success': True, 'msg': 'Face não identificada!', 'adm': False}), 202

    else:
        return jsonify({'success': False, 'msg': 'Face não identificada!', 'adm': False}), 201
        


def getUserById(id):
    # print('vai dar select')
    # data_e_hora_atuais = datetime.now()
    # data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
    # print(data_e_hora_em_texto)

    cur = db.connection.cursor()

    # print('conectou')
    # data_e_hora_atuais = datetime.now()
    # data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
    # print(data_e_hora_em_texto)

    sql = """
        select 
            l.id as login_id,
            u.*
        from 
            login l
            join user u on l.user_id = u.id
        where l.id=%s
    """

    cur.execute(sql, [id])

    # print('executou')
    # data_e_hora_atuais = datetime.now()
    # data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
    # print(data_e_hora_em_texto)

    results = cur.fetchall() 
    cur.close()

    # print('deu select.')
    # data_e_hora_atuais = datetime.now()
    # data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
    # print(data_e_hora_em_texto)

    if len(results) > 0:
        user = results[0]

        if int(user['status']) < 1:
            msg = 'Usuário inativo!'
            return jsonify({'success': False, 'msg': msg, 'adm': True}), 203

        if int(user['holidays']) == 1:
            msg = 'Usuário deveria estar de férias!'
            return jsonify({'success': False, 'msg': msg, 'adm': False}), 203

        if int(user['suspended']) == 1:
            msg = 'Usuário suspenso!'
            return jsonify({'success': False, 'msg': msg, 'adm': False}), 203
        
        return jsonify({'success': True, 'user': user}), 200
    else: 
        return jsonify({'success': False, 'msg': 'Face não identificada!', 'adm': False}), 201