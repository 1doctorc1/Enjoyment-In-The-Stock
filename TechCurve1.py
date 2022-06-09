#股市行情数据获取和作图 -2
from  Ashare import *          #股票数据库    https://github.com/mpquant/Ashare
from  MyTT import *            #myTT麦语言工具函数指标库  https://github.com/mpquant/MyTT
    
# 证券代码兼容多种格式 通达信，同花顺，聚宽
# sh000001 (000001.XSHG)    sz399006 (399006.XSHE)   sh600519 ( 600519.XSHG )     sh600050 中国联通
def TechCurve1(stock_code,frequency='1d',count=120,end_date=''):

    # print('请按标准格式输入你想要查询的股票代码：')
    # stock_code=input()
    # stock_code='sh600050'
    df=get_price(stock_code,frequency=frequency,count=count)      #默认获取今天往前120天的日线行情
    num=0
    #-------------stock_code -> stock_name
    import pandas as pd
    xcode= stock_code.replace('.XSHG','').replace('.XSHE','')                      #证券代码编码兼容处理 
    xcode='sh'+xcode if ('XSHG' in stock_code)  else  'sz'+xcode  if ('XSHE' in stock_code)  else stock_code  
    scode_num=xcode[2:8]

    
    
    path = 'TranslationTable.xlsx'
    data = pd.read_excel(path)  #读取数据,
    
    stock_name=data[ data['Code']==int(scode_num) ].iloc[0,1]
    
    #------------------------------
    if count>5:
        print(stock_name+'日线行情\n',df.tail(5))
    else:
        num=count
        print(stock_name+'日线行情\n',df.tail(num))
    
    #-------有数据了，下面开始正题 -------------
    CLOSE=df.close.values;         OPEN=df.open.values           #基础数据定义，只要传入的是序列都可以  Close=df.close.values 
    HIGH=df.high.values;           LOW=df.low.values             #例如  CLOSE=list(df.close) 都是一样
    
    #-------------------------作图显示-----------------------------------------------------------------1
    import matplotlib.pyplot as plt ;  from matplotlib.ticker import MultipleLocator
    
    plt.figure(figsize=(15,8))  
    ###  plt.plot(CLOSE,label='SHZS'); 
    plt.plot(CLOSE,label='CLOSE');           #画图显示 
    plt.plot(OPEN,label='OPEN');       plt.plot(HIGH,label='HIGH');
    plt.plot(LOW,label='LOW');
    plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    plt.title( stock_name + "   &  ORIGINAL SHOW",fontsize=20);  
    plt.savefig('./img/ORIGINAL.jpg')
    plt.close('all')
    # plt.show()
    
    
    
    
    
    
    #-----------------------------------2
    MA5=MA(CLOSE,5)                                #获取5日均线序列
    MA10=MA(CLOSE,10)                              #获取10日均线序列
    up,mid,lower=BOLL(CLOSE)                       #获取布林带指标数据    
    
    plt.figure(figsize=(15,8))  
    plt.plot(up,label='BOLL上界');           #画图显示 
    plt.plot(mid,label='BOLL-MID');       plt.plot(lower,label='BOLL下界');
    plt.plot(MA10,label='MA10',linewidth=0.5,alpha=0.7);   #还多画了一条MA10线
    plt.legend();       #为figure添加图例
    plt.grid(linewidth=0.5,alpha=0.7);   
    plt.gcf().autofmt_xdate(rotation=45);
    plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    plt.title(stock_name + "   &   BOLL SHOW",fontsize=20);   
    plt.savefig('./img/BOLL.jpg')
    plt.close('all')
    # plt.show()
    
    
    # #-------------------3
    k,d,j=KDJ(CLOSE,HIGH,LOW)
    
    plt.figure(figsize=(15,8))  
    plt.plot(k,label='KDJ-K');           #画图显示 
    plt.plot(d,label='KDJ-D');       plt.plot(j,label='KDJ-J');
    plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    plt.title(stock_name + "   &   KDJ SHOW",fontsize=20);   
    plt.savefig('./img/KDJ.jpg')
    plt.close('all')
    # plt.show()
    
    # #--------4
    dif,dea,macd=MACD(CLOSE)
    
    plt.figure(figsize=(15,8))  
    # plt.plot(CLOSE,label='SHZS'); 
    plt.plot(dif,label='MACD-DIF');           #画图显示 
    plt.plot(dea,label='MACD-DEA');       plt.plot(macd,label='MACD-MACD');
    plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    plt.title( stock_name + "   &   MACD SHOW",fontsize=20);  
    plt.savefig('./img/MACD.jpg')
    plt.close('all')
    # plt.show()
    
    #-----------------------------5
    # dif=RSI(CLOSE)
    
    # plt.figure(figsize=(15,8))  
    # plt.plot(dif,label='RSI-DIF');           #画图显示 
    # plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    # plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    # plt.title( stock_name + "   &   RSI SHOW",fontsize=20);  
    # plt.savefig('./img/RSI.jpg')
    # plt.close('all')
    # plt.show()
    
    #-----------------------------6            
    # pdi,mdi,adx,adxr=DMI(CLOSE,HIGH,LOW)
    
    # plt.figure(figsize=(15,8))  
    # plt.plot(pdi,label='DMI-PDI');           #画图显示 
    # plt.plot(mdi,label='DMI-MDI');           #画图显示 
    # plt.plot(adx,label='DMI-ADX');       
    # plt.plot(adxr,label='DMI-ADXR');
    # plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    # plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    # plt.title( stock_name + "   &   DMI SHOW",fontsize=20);  
    # plt.savefig('./img/DMI.jpg')
    # plt.close('all')
    # plt.show()
    
    #-----------------------------7
    # ar,br=BRAR(OPEN,CLOSE,HIGH,LOW)
    
    # plt.figure(figsize=(15,8))  
    # plt.plot(ar,label='BRAR-AR');           #画图显示 
    # plt.plot(br,label='BRAR-BR');           #画图显示 

    # plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    # plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    # plt.title( stock_name + "   &   BRAR SHOW",fontsize=20);  
    # plt.savefig('./img/BRAR.jpg')
    # plt.close('all')
    # plt.show()
    
    #-----------------------------8
    # wr,wr1=WR(CLOSE,HIGH,LOW)
    
    # plt.figure(figsize=(15,8))  
    # plt.plot(wr,label='W&R-WR');           #画图显示 
    # plt.plot(wr1,label='W&R-WR1');           #画图显示 

    # plt.legend();       plt.grid(linewidth=0.5,alpha=0.7);   plt.gcf().autofmt_xdate(rotation=45);
    # plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    # plt.title( stock_name + "   &   W&R SHOW",fontsize=20);  
    # plt.savefig('./img/W&R.jpg')
    # plt.close('all')
    # plt.show()
    
    #-----------------------------
    
    
    
    
    
    

    # return df.tail(num)

if __name__=='__main__':
    TechCurve1('600050.XSHG','1M',120)








