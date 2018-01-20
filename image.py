import requests, base64
import os
import urllib, http
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import json
from pymongo import MongoClient
connection = MongoClient(port=27017)
db = connection.weapon_detection
people = db.people
depress = db.depress

DirName='/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])

class image:
    def __init__(self):
        self.keyword=set(["weapon","gun","knife"])
        self.headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': os.environ.get('SUB1'),
        }
        self.params = {
            'visualFeatures': 'Tags,Categories,Description',
            'language': 'en',
            'model':'weapons'
        }

    def check(self,img):
        image = open(img,'rb').read() # Read image file in binary mode
        try:
            response = requests.post(url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze',
                                     headers = self.headers,
                                     params = self.params,
                                     data = image)
            data = response.json() 
            print(data)
            if data:
                for i in data["tags"]:
                    if i["name"] in self.keyword and i["confidence"]>.50:
                        print(i["name"])
                        return True,"Alert"
            return False,"Fine"
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def face_details(self,img):
        uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': os.environ.get('SUB2'),
        }
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }
        image = open(img,'rb').read()
        try:
            response = requests.request('POST', uri_base + '/face/v1.0/detect', data=image, headers=headers, params=params)
            parsed = json.loads(response.text)
            return parsed
        except Exception as e:
            print('Error:')
            print(e)
    def emotion_details(self,img):
        headers = {
            # Request headers. Replace the placeholder key below with your subscription key.
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': os.environ.get('SUB3'),
        }

        params = urllib.parse.urlencode({
        })


        image = open(img,'rb').read()

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, image, headers)
            response = conn.getresponse()
            data = response.read()
            parsed = json.loads(data)
            #print ("Response:")
            #print (json.dumps(parsed, sort_keys=True, indent=2))
            conn.close()
            return parsed
        except Exception as e:
            print(e.args)  

if __name__ =="__main__":
    img=image()
    print()
    pos = DirName+"/hackathon/video/public/images/"
    i=0
    while(True):
        try:
            test=pos+str(i)+".png"
            print(test)
            if os.path.isfile(test):
                res=img.check(test)
                if res[0]:
                    faces=img.face_details(test)
                    print(faces)
                    if faces:
                        for face in faces:
                            saving={'location':str(i)+".png",'age':face["faceAttributes"]["age"],'gender':face["faceAttributes"]["gender"]}
                            people.insert(saving)
                    else:
                        saving={'location':str(i)+".png",'age':'','gender':''}
                        people.insert(saving)
                faces=img.emotion_details(test)
                for face in faces:
                    print(face)
                    if face['scores']["sadness"]>0.75:
                        saving = {'location':str(i)+".png"}
                        depress.insert(saving)
            else:
                print("File Doesn't exist")
                break
            if 0xFF == ord('q'):
                break
            i=i+1
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))