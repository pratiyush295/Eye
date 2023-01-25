from flask import Flask,render_template,request,redirect,url_for,flash

import os
import urwid
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

app=Flask(__name__)
ALLOWED_EXT=['png','jpg','jpeg','gif','jfif']

model=load_model('model.h5')

def predict_output(path_img):
    image=Image.open(path_img)
    image=image.resize((150,150))
    image_arr=np.array(image)
    image_arr.shape=(1,150,150,3)


    # img=cv2.imread(path_img)
    # img=cv2.resize(img,(150,150))
    # img=img.reshape((1,150,150,3))
    result=model.predict(image_arr)
    return result[0][0]


def allowed_files(filename):
    
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT


def clear_folder(path):
    
    for file in os.listdir(path):
        image=os.path.join(path,file)
        os.remove(image)




@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')




@app.route('/',methods=['POST'])
def predict():
    image=request.files['file']

    if image.filename=='':
        no_file="UPLOAD A FILE"
        return render_template('index.html',no_file=no_file)


    if allowed_files(image.filename)==False:
        wrong_format='Wrong Format'
        return render_template('index.html',wrong_format=wrong_format)

    clear_folder('./static/images/')

    
    image_path="./static/images/"+image.filename
    image.save(image_path)

    result=predict_output(image_path)
    if result==0.0:
        result="CAT"
    else:
        result="DOG"

    return render_template('index.html',result=result,image_path=image_path)    









if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)