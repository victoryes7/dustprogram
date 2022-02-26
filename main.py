print(f'{"microdust project v 1.0":=^70}')
print('='*70)

import requests
import json
import pandas

StaList = pandas.read_excel('station_list.xls')
StaLo = list(StaList['Unnamed: 0'])[3:]
StaNa = list(StaList['Unnamed: 1'])[3:]
StaInfo = list(zip(StaLo,StaNa))

for Lo, Na in StaInfo :
      print( f'{Na:=<5} in {Lo:=>5}' )

stationname = input('input your needed station name:')

REQUESTPOINT = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
PAR = {
            'serviceKey' : 'BSEbtpnwr+WG9F7SSNKIQnJSisUOOfIgmChrx+tcAU9kJr0sd+CirE3hBuvj/k7iwncVQYTp2sTHfFNy1FBbEw=='
           ,'returnType' : 'json'
           ,'numOfRows' : '100'
           ,'pageNO' : '1'
           ,'stationName' : False
           ,'dataTerm' : 'DAILY'
           ,'ver' : '1.0'           
}
PAR['stationName'] = stationname

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
DATAdate = RAWDATADIC['response']['body']['items'][0]['dataTime']
DATAdate = DATAdate[:10]

ListOfCrit = [0.15 , 25 , 0.1 , 0.1 , 100 , 35]
#아황산, 일산화탄소, 오존, 이산화질소, 미세먼지, 초미세먼지
#SO2, CO, O3, NO2, PM10, PM25, 단위는 ppm, microgram/m세제곱
RFdatadic = {}
for Q in range(DATAamou) :
      RFdatadic[Q] = []

for num , DATA in enumerate(DATALIST) :
      ListOfDATA = []
      
      ListOfDATA.append(DATA.get('so2Value' , 0))
      ListOfDATA.append(DATA.get('coValue' , 0))
      ListOfDATA.append(DATA.get('o3Value' , 0))
      ListOfDATA.append(DATA.get('no2Value' , 0))
      ListOfDATA.append(DATA.get('pm10Value' , 0))
      ListOfDATA.append(DATA.get('pm25Value' , 0))
      
      for inx , DATA in enumerate(ListOfDATA) :
            if DATA == '-' :
                  ListOfDATA[inx] = 0
      ListOfDATA = list(map(float,ListOfDATA))
      
      for Q in range(6) :
            if ListOfDATA[Q] > ListOfCrit[Q] :
                  RFdatadic[num].append(Q)
                  
MSG = f'air quality of {DATAdate}'
print(f'{MSG:=^70}')

AtmoFact = ['sulfurate' , 'carbon monoxide' , 'ozone' , 'nitrogen dioxide' , 'fine dust' , 'ultrafine dust']
for Q in range(DATAamou) :
      
      DATAtime = RAWDATADIC['response']['body']['items'][Q]['dataTime'][11:]
      print(f'{DATAtime:=^70}')
      
      if RFdatadic[Q] :
            for W in RFdatadic[Q] :
                  print(f'{AtmoFact[W]}')
                  