print(f'{"microdust project v 1.0":=^100}')
print('='*100)

import requests
import json

REQUESTPOINT = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
PAR = {
            'serviceKey' : 'BSEbtpnwr+WG9F7SSNKIQnJSisUOOfIgmChrx+tcAU9kJr0sd+CirE3hBuvj/k7iwncVQYTp2sTHfFNy1FBbEw=='
           ,'returnType' : 'json'
           ,'numOfRows' : '100'
           ,'pageNO' : '1'
           ,'stationName' : '종로구'
           ,'dataTerm' : 'DAILY'
           ,'ver' : '1.0'           
}

ANSWER = requests.get(REQUESTPOINT,params = PAR)
RAWDATADIC = json.loads(ANSWER.content)

ddatastate = RAWDATADIC['response']['header']['resultCode']
if ddatastate == '00' :
      print('Data Download Completed')
if ddatastate != '00' :
      print('Requesting Data Error')
#데이터가 문제없이 불러와지면 '00'을 저장

DATALIST = RAWDATADIC['response']['body']['items']
DATAamou = RAWDATADIC['response']['body']['totalCount']

gitcheck = 1
