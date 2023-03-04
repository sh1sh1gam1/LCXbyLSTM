import os
path = "./"
files = os.listdir(path)
data_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
print(data_list)

# 気象庁のデータと、ケーブルデータを関連させる
import pandas as pd
import time 

place_codeA = [62]
place_codeB = [47772]
place_name = ["大阪"] 
# data_list = ["status1.xls","status2.xls","status3.xls","status4.xls","status5.xls","status6.xls","status7.xls","status8.xls","status9.xls","status10.xls","status11.xls"] 
df_list = []

import requests
from bs4 import BeautifulSoup #ダウンロードしてなかったらpipでできるからやってね。
import csv

flag = False
pre_year = 2021
nex_year = 2022
pre_month = 8
nex_month = 9
pre_day = 14
nex_day = 17
nex_min = ""

# URLで年と月ごとの設定ができるので%sで指定した英数字を埋め込めるようにします。
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=%s&view=p1"


#取ったデータをfloat型に変えるやつ。(データが取れなかったとき気象庁は"/"を埋め込んでいるから0に変える)
def str2float(str):
  try:
    return float(str)
  except:
    return 0.0


if __name__ == "__main__":
  #都市を網羅します
  for place in place_name:
    #最終的にデータを集めるリスト (下に書いてある初期値は一行目。つまり、ヘッダー。)
    All_list = [['年月日', '降水量(mm)','平均気温']]
    print(place)
    index = place_name.index(place)
    # for文で2016年~2021年までの11回。
    for exc in data_list:
      flag = False
      All_list = [['年月日', '降水量(mm)','平均気温']]
      for year in range(pre_year,nex_year):
        print(str(year) + "年")
        # その年の1月~12月の12回を網羅する。
        for month in range(pre_month,nex_month):
          #2つの都市コードと年と月を当てはめる。
          print(str(month) + "月")
          time.sleep(0.2)
          # 31日で終わる月に対する処理
          if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            for day in range(pre_day, nex_day):
              r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month,day))
            
              r.encoding = r.apparent_encoding
              # まずはサイトごとスクレイピング
              soup = BeautifulSoup(r.text)
              # findAllで条件に一致するものをすべて抜き出します。
              # 今回の条件はtrタグでclassがmtxになってるものです。
              rows = soup.findAll('tr',class_='mtx')
              # 表の最初の1~4行目はカラム情報なのでスライスする。(indexだから初めは0だよ)
              # 【追記】2020/3/11 申し訳ございません。間違えてました。
              rows = rows[2:]
              # 1日〜最終日までの１行を網羅し、取得します。
              for row in rows:
              # 今度はtrのなかのtdをすべて抜き出します
                data = row.findAll('td')
                #１行の中には様々なデータがあるので全部取り出す。
                # ★ポイント
                rowData = [] #初期化
                rowData.append(str(year) + "/" + str(month) + "/" + str(day) + "/" + str(data[0].string))
                #rowData.append(str2float(data[1].string))
                #rowData.append(str2float(data[2].string))
                rowData.append(str2float(data[3].string))
                rowData.append(str2float(data[4].string))
                #rowData.append(str2float(data[6].string))
                #rowData.append(str2float(data[9].string))
                #次の行にデータを追加
                All_list.append(rowData)



          elif month == 4 or month == 6 or month == 9 or month == 11:
            for day in range(pre_day,nex_day):
              r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month,day))

              r.encoding = r.apparent_encoding
              soup = BeautifulSoup(r.text)
              rows = soup.findAll('tr',class_='mtx')
              rows = rows[2:]
              for row in rows:
                data = row.findAll('td')
                rowData = [] 
                rowData.append(str(year) + "/" + str(month) + "/" + str(day) + "/" + str(data[0].string))
                #rowData.append(str2float(data[1].string))
                #rowData.append(str2float(data[2].string))
                rowData.append(str2float(data[3].string))
                rowData.append(str2float(data[4].string))
                #rowData.append(str2float(data[6].string))
                #rowData.append(str2float(data[9].string))
                All_list.append(rowData)
          else:
            if year % 4 == 0:
              for day in range(pre_day, nex_day):
                r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month,day))

                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text)
                rows = soup.findAll('tr',class_='mtx')
                rows = rows[2:]
                for row in rows:
                  data = row.findAll('td')
                  rowData = [] 
                  rowData.append(str(year) + "/" + str(month) + "/" + str(day) + "/" + str(data[0].string))
                  #rowData.append(str2float(data[1].string))
                  #rowData.append(str2float(data[2].string))
                  rowData.append(str2float(data[3].string))
                  rowData.append(str2float(data[4].string))
                  #rowData.append(str2float(data[6].string))
                  #rowData.append(str2float(data[9].string))
                  All_list.append(rowData)
            else:
              for day in range(pre_day, nex_day):
                r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month,day))

                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text)
                rows = soup.findAll('tr',class_='mtx')
                rows = rows[2:]
                for row in rows:
                  data = row.findAll('td')
                  rowData = [] 
                  rowData.append(str(year) + "/" + str(month) + "/" + str(day) + "/" + str(data[0].string))
                  #rowData.append(str2float(data[1].string))
                  #rowData.append(str2float(data[2].string))
                  rowData.append(str2float(data[3].string))
                  rowData.append(str2float(data[4].string))
                  #rowData.append(str2float(data[6].string))
                  #rowData.append(str2float(data[9].string))
                  All_list.append(rowData)

      All_df=pd.DataFrame(data=All_list)
      #0行目をcolumns用に取り出し
      col=All_df.loc[0,:]

      #0行目をcolumnsにしたDataFrame
      all_data_df_p=pd.DataFrame(data=All_list, columns=col)
      df=all_data_df_p

      #DataFrameの作成と確認
      all_data_df=df.drop(df.index[[0]])

      print(type(exc))
      # 全てのシートを取り込み
      df = pd.read_excel(exc, sheet_name=None)
      # シート名を取り込み
      df_stayleseet_key = df.keys()
      # 1シートごとに読み込みし直す
      for stayle_key in df_stayleseet_key:
        print(stayle_key)
        df = pd.read_excel(exc , sheet_name=stayle_key)
        df = df.iloc[[4,6,7], 1:]

        t = df.iloc[0,0]
        old_ms = t[36:38]
        new_ms = t[55:57]
        if(int(new_ms) - int(old_ms) < 0):
          flag = True
        t = t[25:35]

        if pre_day < 10 and pre_month < 10:
          t = t[0:5] + t[6:8] + t[9]
        elif pre_day < 10 and pre_month >= 10:
          t = t[0:5] + t[6:9] + t[9]
        elif pre_day >= 10 and pre_month < 10:
          t = t[0:5] + t[6:8] + t[8:11]
        else:
          t = t[0:5] + t[6:9] + t[8:11]


        df = df.iloc[:,1:]

        target = ' ' 
        for i in range(len(df.columns)):
          temp = t + '/' + df.iloc[0,i]
          idx = temp.find(target) - 2
          df.iloc[0,i] = temp[:idx]

        df = df.T

        df = df.rename(columns={4: '年月日', 6:'LCX上り入力', 7:'LCX下り入力'})

        print(len(df))

        if(flag):
          for i in range(len(df)):
            temp = df["年月日"][i]
            if int(temp[10:12]) < 10:
              df["年月日"][i] = temp[0:7] + str(int(temp[7:9]) + 1) + temp[9:15]

        #print(df)

        result = pd.merge(all_data_df, df,  
            how="inner", on = "年月日")
        #print(all_data_df)
        #print(result)
        df_list.append(result)

for i in range(len(df_list)-1):
  print(i)
  if(i == 0):
    df_new = pd.concat(
    [df_list[i], df_list[i+1]],
    axis=0,
    ignore_index=True)
  else:
    df_new = pd.concat(
    [df_new, df_list[i+1]],
    axis=0,
    ignore_index=True
)
    
df_new.sort_values('年月日', inplace=True)
df_new


# データ整形
df = df_new.drop('年月日', axis=1)
df = df.drop('LCX下り入力', axis=1)
df = df.astype("float32")
print(df)

import numpy as np

#平均気温
templature = df[["平均気温"]].values
templature = templature.reshape(-1)
templature = templature.astype(np.float64)
# templature[:] *= 10

#降水量
rain = df[["降水量(mm)"]].values
rain = rain.reshape(-1)
rain = rain.astype(np.float64)
# rain[:] *= 10

#LCX上り入力
lcxup = df[["LCX上り入力"]].values
lcxup = lcxup.reshape(-1)
lcxup = lcxup.astype(np.float64)
# lcxup[:] *= 1.2