import cv2
import urllib
import numpy as np
import urllib.request as ur

def main():
    url_Str="https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Land_Cover_L48/ows?bbox=-8831962.608514%2C4533969.8342275005%2C-8831595.891709609%2C4534381.584555696&crs=EPSG%3A3857&format=image%2Fpng&request=GetMap&service=WMS&styles=&transparent=true&version=1.3.0&layers=NLCD_2019_Land_Cover_L48&WIDTH=100&HEIGHT=100"
    req = ur.urlopen(url_Str)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    cv2.imshow('lalala', img)
    if cv2.waitKey() & 0xff == 27: quit()


    return 0
if __name__ == '__main__':
    main()
