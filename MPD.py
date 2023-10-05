import pyrebase
import os
import cv2
import numpy as np
import face_recognition
import glob

def tool():
    config = {
        "apiKey": "AIzaSyBJsnBXhodczgkiuvpOaIDOh4WDUF6tN-E",
        "authDomain": "mpi-system.firebaseapp.com",
        "databaseURL": "https://mpi-system-default-rtdb.firebaseio.com",
        "projectId": "mpi-system",
        "storageBucket": "mpi-system.appspot.com",
        "messagingSenderId": "429607724215",
        "serviceAccount": "E:/Project/mpd/upload/serviceAccount.json"
    };

    firebase=pyrebase.initialize_app(config)
    storage = firebase.storage()
    storage.delete("copy",None)
    path="  E:/Project/Retrieve/"
    b="E:/Project/Retrieve/"
    ab=str(1)

    files = glob.glob(path+'*')
    for o in files:
        os.remove(o)

    all_files = storage.child().list_files()
    for file in all_files:
        print(file.name)
        try:
                storage.child(file.name).get_url(None)
                file.download_to_filename(b+ab+".jpeg")
                S=b+ab+".jpeg"
        except:
                print('Download Failed')
    try:
        path1="E:/Project/Database/"
        im=os.listdir(path1)
        v="E:/Project/Database/"
        for f in im:
            m=v+f
            img_bgr = face_recognition.load_image_file(m)
            img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
            img_modi=face_recognition.load_image_file(m)
            img_modi_rgb = cv2.cvtColor(img_modi,cv2.COLOR_BGR2RGB)
            face = face_recognition.face_locations(img_modi_rgb)[0]
            copy = img_modi_rgb.copy()
                    # ------ Drawing bounding boxes around Faces------------------------
            cv2.rectangle(copy, (face[3], face[0]),(face[1], face[2]), (255,0,255), 2)
            train_encode = face_recognition.face_encodings(img_modi_rgb)[0]
                    #----- lets test an image
            test = face_recognition.load_image_file(S)
            test = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)
            test_encode = face_recognition.face_encodings(test)[0]
            print(face_recognition.compare_faces([train_encode],test_encode,tolerance =0.4))
            if(face_recognition.compare_faces([train_encode],test_encode))==[True]:#rerturns true for similar
                cv2.rectangle(img_modi, (face[3], face[0]),(face[1], face[2]), (255,0,255), 1)
                storage.child("copy").put(v+f)
                l=1
                break
            else:
                l=2
        if(l==2):
            storage.child("copy").put("E:/Project/images/Notfound.jpg")
    except IndexError:
        storage.child("copy").put("E:/Project/images/Error.jpg")

    db=firebase.database()
    url=storage.child("copy").get_url(None)
    data={"ImgUrl":url}
    db.child("copy").set(data)
    return 'Done'e
