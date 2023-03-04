#ライブラリインポート
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import matplotlib.pyplot as plt

#データ準備
xdeg=414 # データの数が増えたらその分これも増やす必要あり
x = np.arange(0,xdeg+1)
X1=templature
X2=rain
X3=lcxup
Y1=lcxup
X1.shape

#入力データの可視化
plt.plot(range(0, len(x)), X1, color="b", label="X1")
plt.plot(range(0, len(x)), X2, color="r", label="X2")
plt.plot(range(0, len(x)), X3, color="g", label="X3")
#plt.plot(range(0, len(x)), X4, color="y", label="X4")
plt.legend()
plt.show()
plt.plot(range(0, len(x)), Y1, color="b", label="Y1")
#plt.plot(range(0, len(x)), Y2, color="r", label="Y2")
plt.legend()
plt.show()

#LSTM用にデータの前処理
X_list=[X1,X2,X3]
Y_list=[Y1]
Xdata=[]
Ydata=[]
look_back=9   # look_back数ぶん前のデータを用いて、look_back+1個目のデータを予測する
# 例えば、10日間のデータが1日10個で合計100個あったとする
# そして3日間のデータを用いて、次の日のデータを予測したい時
# look_backを(10*3)=30に設定すれば良い
# 予測先はlook_back+1より31個目のデータを予測する
for i in range(len(x)-look_back):
    Xtimedata=[]
    # Xdataにlook_back数個にまとめたXtimedataのリスト内容を代入する
    for j in range(len(X_list)):
        Xtimedata.append(X_list[j][i:i+look_back])
    Xtimedata=np.array(Xtimedata)
    Xtimedata=Xtimedata.transpose()
    Xdata.append(Xtimedata)
    Ytimedata=[]
    # Ydataにlook_back+1個目のデータを代入する、つまりlook_back数分まとめたデータからlook_back+1個目のデータを予測する！
    for j in range(len(Y_list)):
        Ytimedata.append(Y_list[j][i+look_back])
    Ydata.append(Ytimedata)
Xdata=np.array(Xdata)
Ydata=np.array(Ydata)


#LSTMモデルの構築⇒学習開始
print(Xdata.shape)
Xdim=Xdata.shape[2]
Ydim=Ydata.shape[1]
validation_split_rate=0.2
model = Sequential()
model.add(LSTM(4, input_shape=(look_back,Xdim)))
model.add(Dense(Ydim))
model.compile(loss="mean_squared_error", optimizer=Adam(lr=0.001))
model.summary()
history=model.fit(Xdata,Ydata,batch_size=16,epochs=1000,validation_split=validation_split_rate)

#学習結果の可視化
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

#精度検証
Xdata_validation=Xdata[-int(len(Xdata)*(validation_split_rate)):]
Ydata_validation=Ydata[-int(len(Ydata)*(validation_split_rate)):]
Predictdata = model.predict(Xdata_validation)

plt.plot(range(0, len(Predictdata)),Predictdata[:,0], color="b", label="predict")
plt.plot(range(0, len(Ydata_validation)),Ydata_validation[:,0], color="r", label="row_data")
plt.legend()
plt.show()


from tensorflow import keras
# モデルを保存
model.save("my_model")

reconstructed_model = keras.models.load_model("my_model")
Predictdata = model.predict(Xdata_validation)
rePredictdata = reconstructed_model.predict(Xdata_validation)

plt.plot(range(0, len(Predictdata)),Predictdata[:,0], color="b", label="predict")
plt.plot(range(0, len(Ydata_validation)),Ydata_validation[:,0], color="r", label="row_data")
plt.legend()
plt.show()

plt.plot(range(0, len(Predictdata)),Predictdata[:,0], color="b", label="predict")
plt.plot(range(0, len(Ydata_validation)),Ydata_validation[:,0], color="r", label="row_data")
plt.legend()
plt.show()