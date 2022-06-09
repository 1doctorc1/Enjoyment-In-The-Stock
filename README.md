README

## Enjoyment in the Stock项目

2022年北京邮电大学

信息与通信工程学院

程序设计方法课程

Enjoyment in the Stock项目

专用Github仓库

相关开发者文档，如需求及概要分析，具体功能设计文档将在代码开源和课程答辩后2周内传至个人博客[https://1doctorc1.github.io](https://1doctorc1.github.io/)，欢迎关注！

### 该项目包含以下要素：

- 千行代码(GUI设计能用Qt designer我就要手敲)
- 专业的经济学知识(确实有不少的经济学python函数，但是我不懂，项目组里其他人懂，所以咱也不知道专业不专业)
- 精准且长期的股票预测(至少在我眼里，股票这种东西，能预测一天就是牛)
- 开源代码(走过路过，瞧一瞧看一看啊)
- 开发者文档(因为图库问题早就不用的博客还是被扒了出来)

### 注意事项：

- 运行环境为Window10   Spyder(anaconda)
- Pycharm可能会因为导入库的版本不同导致个别功能无法实现且出现GUI格式错误
- 记得所有下载的文件放在同一文件夹下哦
- 试用版请以gui_test.py作为主函数运行

### 文件功能介绍：

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

