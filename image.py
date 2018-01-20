import requests, base64
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import json

DirName='/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])

class image:
    def __init__(self):
        self.keyword=set(["weapon","gun","knife"])
        self.headers = {
            # Request headers.
            'Content-Type': 'application/octet-stream',
            # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
            'Ocp-Apim-Subscription-Key': os.environ.get('SUB1'),
        }
        self.params = {
    # Request parameters. All of them are optional.
            'visualFeatures': 'Tags,Categories,Description',
            'language': 'en',
        }

# Replace the three dots below with the full file path to a JPEG image of a celebrity on your computer or network.
    def check(self,img):
        image = open(img,'rb').read() # Read image file in binary mode
        try:
            # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
            #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the 
            #   URL below with "westus".
            response = requests.post(url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze',
                                     headers = self.headers,
                                     params = self.params,
                                     data = image)
            data = response.json() 
            print(data)
            for i in data["tags"]:
                if i["name"] in self.keyword and i["confidence"]>.75:
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
        image = open(img,'rb').read() # Read image file in binary mode
        try:
    # Execute the REST API call and get the response.
            response = requests.request('POST', uri_base + '/face/v1.0/detect', data=image, headers=headers, params=params)
            print ('Response:')
            parsed = json.loads(response.text)
            print (json.dumps(parsed, sort_keys=True, indent=2))
        except Exception as e:
            print('Error:')
            print(e)

####################################   

if __name__ =="__main__":
    img=image()
    print()
    pos = DirName+"/hackathon/video/"
    i=0
    while(True):
        try:
            test=pos+str(i)+".png"
            print(test)
            if os.path.isfile(test):
                res=img.check(test)
                if res[0]:
                    print(img.face_details(test))
            else:
                print("File Doesn't exist")
                break
            if 0xFF == ord('q'):
                break
            i=i+1
        except:
            print("Closing the program")
            break