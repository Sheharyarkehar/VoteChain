from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import urllib
from skimage import io
import cv2
import numpy as np
from numpy import asarray
import urllib.request

def _grab_image(path=None, stream=None, url=None):
                # if the path is not None, then load the image from disk
                if path is not None:
                    image = cv2.imread(path)
                # otherwise, the image does not reside on disk
                else:
                    # if the URL is not None, then download the image
                    if url is not None:
                        resp = urllib.urlopen(url)
                        data = resp.read()
                    # if the stream is not None, then the image has been uploaded
                    elif stream is not None:
                        data = stream.read()
                    # convert the image to a NumPy array and then read it into
                    # OpenCV format
                    image = np.asarray(bytearray(data), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                # return the image
                return image
class MyFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
      image = _grab_image(stream=request.FILES["file"])
      test_original=image
      table = str.maketrans(dict.fromkeys("[]"))
      a=str(request.POST.getlist('url')).translate(table)
      table=str.maketrans(dict.fromkeys("''"))
      img = io.imread(a.translate(table))
      fingerprint_database_image =asarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
      sift = cv2.xfeatures2d.SIFT_create()
      keypoints_1, descriptors_1 = sift.detectAndCompute(test_original, None)
      keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)
      matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), dict()).knnMatch(descriptors_1,descriptors_2, k=2)
      match_points = []
      ans = 0.0
      for p, q in matches:
        if p.distance < 0.1 * q.distance:
            match_points.append(p)
             keypoints = 0
        if len(keypoints_1) <= len(keypoints_2):
           keypoints = len(keypoints_1)            
        else:
           keypoints = len(keypoints_2)
        ans=len(match_points) / keypoints    
        if (len(match_points) / keypoints)>0.95:
           print("% match: ", len(match_points) / keypoints * 100)
           print("Figerprint ID: " + str(file)) 
           result = cv2.drawMatches(test_original, keypoints_1, fingerprint_database_image,keypoints_2, match_points, None) 
           result = cv2.resize(result, None, fx=2.5, fy=2.5)
           break;
#       keypoints = 0

#       if len(keypoints_1) == len(matches):
#            keypoints = len(keypoints_2)
#       else:
#            keypoints = len(keypoints_1)

#            result = cv2.drawMatches(test_original, keypoints_1, fingerprint_database_image,
#                                  keypoints_2, match_points, None)
#            result = cv2.resize(result, None, fx=2.5, fy=2.5)

#       if keypoints >= len(matches):
#           num = len(matches)
#           denom = keypoints
#           ans = num / denom * 100

#       else:
#          num = keypoints
#          denom = len(matches)
#          ans = num / denom * 100
        # file_serializer = MyFileSerializer(data=request.data)
      print(ans)  
      if ans>=75:
       return Response(True, status=status.HTTP_200_OK)

      else:
       return Response(False, status=status.HTTP_400_BAD_REQUEST)
