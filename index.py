import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import base64
import cv2
from skimage.metrics import structural_similarity as ssim
import argparse
import imutils

UPLOAD_FOLDER = '.\static\image'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == "POST":
        f = request.files['image']
        print(f)
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'p1.jpg'))
        # global image_original
        # image_original = filename
        return render_template('firmar.html')
        
@app.route('/compare', methods=['POST'])
def compare():
    if request.method == "POST":
        # name=image_original
        # print(name)
        # f = request.files["canvas"]
        # filename = secure_filename(f.filename)
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'firma.png'))
        return render_template('compare.html', value='')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        f1 = request.values['jsvar']
        f = f1.replace('data:image/png;base64,', '')
        # print(f)
        val=bytes(f, encoding='utf-8')
        # print(val)

        # path ="\\static\\images\\prueba.png"
        with open("prueba.jpg", "wb") as fh:
            fh.write(base64.decodebytes(val))
        
        formatear()
        result = comparar()
        return render_template('compare.html', value=result)

def formatear():
    from PIL import Image
    img2 = Image.open('.\\static\\image\\p1.jpg')
    img2 = img2.convert('RGBA')

    datas = img2.getdata()
    newData = []

    for item in datas:
        if item[0] > 180 and item[1] > 180 and item[2] > 180:
            newData.append((255, 255, 255,0))
        else:
            newData.append((0,0,0,255))

    img2.putdata(newData)
    img2.save("./original.png", "PNG")
    img2.close()
    # # Creamos mascara de bits de transparencia
    # trans_mask = img1[:,:,3] == 0

    # # Reemplazamos areas de transparencia con blanco y no transparente
    # img1[trans_mask] = [255, 255, 255, 255]

    # # Nueva imagen sin canal alpha
    # new_img = cv2.cvtColor(img1, cv2.COLOR_BGRA2BGR)

    # # Cargar imagen con canal alpha. Usar IMREAD_UNCHANGED para asegurar la carga del canal alpha
    img1 = Image.open('prueba.jpg')
    # Resize the copy image with the size of original image
    h, w = img2.size
    # print(h,w)
    img1 = img1.resize((h,w))
    img1.convert('RGBA')
    datas = img1.getdata()
    newData = []
    for item in datas:
        # if(item[3] > 0):
            # print(item)
        if not item[3] > 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img1.putdata(newData)
    # print(newData)
    img1.save("./copia.png", "PNG")
    img1.close()

def comparar():
    img_a = 'original.png'
    img_b = 'copia.jpg'
    # print(img_a)
    # print(img_b)

    # Construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-f", "--first", required=True, help='original.png')
    # ap.add_argument("-s", "--second", required=True, help='copia.png')
    # args = vars(ap.parse_args())

    # Cargar las 2 imagenes
    imageA = cv2.imread('original.png')
    imageB = cv2.imread('copia.png')
    # print(type(imageB))
    # print(imageA.shape)
    # print(imageB.shape)

    # Convertir la imagen a escala de grises
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # Computar Structure Similarity Index (SSIM) entre las 2 imagenes
    # se devuelve la imagen de diferencia
    (score, diff) = ssim(grayA, grayB, full=True)
    # diff = (diff * 255).asType("uint8")

    # print('SSIM Score: {:.5f}'.format(score*100))
    if(score*100 > 94):
        return ('Accuracy Score: {:.5f}'.format(score) + '%. Parece bastante real :)')
    else:
        return ('Accuracy Score: {:.5f}'.format(score*100) + '%')

if __name__ == '__main__':
    app.run(debug=True)