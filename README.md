README

Enjoyment in the Stock

- 运行环境为Window10   Spyder(anaconda)
- Pycharm可能会因为导入库的版本不同导致个别功能无法实现且出现GUI格式错误
- 相关开发者文档，如需求及概要分析，具体功能设计文档将在代码开源和课程答辩后2周内传至个人博客，欢迎关注！



- img文件：存储程序运行过程中通过专业经济学数学函数生成的指标图像
- Ashare.py：股票数据获取API文件
- forecast.py：基于经济学函数的简单线性预测
- GUI.py：主文件(包含多个其他文件的接口)/GUI配置文件(github上首个单文件纯手敲千行代码)
- gui_test.py：没有本地MongoDB库相关函数的GUI.py的拷贝
  - 可通过配置MongoDB的URL链接绑定本地数据库或者云端数据库
- mongo_db.py：配置MongoDB相关函数
- MyTT.py：整合多层次多级经济学函数
- TechCurve1/2.py：股票指标图像生成的整合文件
- TranslationTable.xlsx：用于将股票代码转换为股票名称的数据集
  - 可能会出现找不到对应代码的情况

