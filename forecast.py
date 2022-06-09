from MyTT import *
from Ashare import *
import matplotlib.pyplot as plt ;  from matplotlib.ticker import MultipleLocator

def forecast(code,N):    # 输入股票代码和预测天数
    xcode= code.replace('.XSHG','').replace('.XSHE','')                      #证券代码编码兼容处理 
    xcode='sh'+xcode if ('XSHG' in code)  else  'sz'+xcode  if ('XSHE' in code)  else code   

    df = get_price(xcode, frequency='1d', count=50)
    
    #-------------stock_code -> stock_name
    import pandas as pd

    scode_num=xcode[2:8]

    
    
    path = 'TranslationTable.xlsx'
    data = pd.read_excel(path)  #读取数据,
    
    stock_name=data[ data['Code']==int(scode_num) ].iloc[0,1]
    
    
    
    CLOSE=df.close.values
    MA5=MA(CLOSE,10)
    MA5=MA5.tolist()
    for i in range(N):
        fc=round(FORCAST(MA5,25),4)     # 以近25天为模型预测后一天
        MA5.append(fc)
    fc=MA5[len(MA5)-N:]
    plt.figure(figsize=(15, 8))
    plt.plot(MA5[:len(MA5)-N+1], label='MA5')  # 画图显示
    plt.plot(list(range(len(MA5)-N,len(MA5))),fc,label="forcast")
    plt.legend()
    plt.grid(linewidth=0.5, alpha=0.7)

    plt.title( stock_name+'  &   MA5预测', fontsize=20 )
    plt.savefig('./img/FORECAST.jpg')
    plt.close('all')
    # plt.show()

if __name__ == "__main__":
    code='000003.XSHE'
    forecast(code,10)   # 进行后十天的预测

