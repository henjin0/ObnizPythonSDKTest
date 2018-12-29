from obniz import Obniz
from matplotlib import pyplot as plt
from drawnow import drawnow, figure
import asyncio
import numpy as np

# 静的変数として利用
class STATIC:
    var = np.array([0.0,0.0]);
    data = np.array([0,0]);

# 書き込むfigure
fig = figure()

# 接続
async def onconnect(obniz):
    obniz.io0.pull("5v")
    obniz.io0.output(True)
    obniz.io1.pull("0v")
    obniz.io1.output(False)
    
    # ad6電圧が変わるとよびだされるよ
    def callback(voltage):
        
        print("{}: change to {} V!".format(len(STATIC.var),voltage))
        if (voltage > 2.5):
            obniz.io0.output(False)
        else:
            obniz.io0.output(True)

        STATIC.var = np.append(STATIC.var,STATIC.var[-1]+1.0);
        STATIC.data = np.append(STATIC.data,voltage);
        #print(len(STATIC.var))
        if(len(STATIC.var) > 100):
            STATIC.var = np.delete(STATIC.var,0);
            STATIC.data = np.delete(STATIC.data,0);

        #print("show {},{}".format(STATIC.var,STATIC.data))
        # グラフ描写するよ
        def draw():
            plt.title("ポテンショメータの値が変わったことを見せたいだけ")
            plt.xlabel("データ点数")
            plt.ylabel("AD6に流れた電圧")
            plt.plot(STATIC.var,STATIC.data)
            plt.pause(0.01)
            
        # リアルタイムで描写するよ
        drawnow(draw)
    
    obniz.io5.pull("0v")
    obniz.io5.output(False)
    obniz.ad6.start(callback)
    obniz.io7.pull("5v")
    obniz.io7.output(True)
    
# Obnizと接続するよ
obniz = Obniz('****-****')
obniz.onconnect = onconnect

# あとで調べます
asyncio.get_event_loop().run_forever()
