

from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome
from  Ashare import *
import pandas as pd
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt 
from matplotlib.ticker import MultipleLocator
from TechCurve1 import *
from TechCurve2 import *
from forecast import *
#from mongo_db import *
import time
#matplotlib.use("Qt5Agg")

"""
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget,
  QHBoxLayout, QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, 
  QBrush, QColor
from PyQt5.QtCore import Qt
"""
class MyFigureCanvas(FigureCanvas):
    """
    继承自FigureCanvas
    使得该类既是一个PyQt5的Qwidget
    又是一个matplotlib的FigureCanvas
    画布
    """
    def __init__(self):
        # 画布上初始化一个图像
        self.figure = Figure()
        super().__init__(self.figure)
        
class pandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
class MainUi(QtWidgets.QMainWindow):
    producer_list=[("1doctorc1","2281781492","zchi@qq.com"),
                   ("橙留香","1048854132","a1048854132@qq.com"),
                   ("小冰","810912294","810912294@qq.com"),
                   ("源码地址","","https://github.com/1doctorc1?tab=repositories"),
                   ("开发者文档及使用指南","","https://1doctorc1.github.io/"),
                   ("上述表格内容选中即粘入剪切板","","")]
    itemModel=None
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.df=pd.DataFrame({})
        #设置窗口名称
        #由于后续隐藏边框所以这里可以不设置窗口名称
        self.setWindowTitle("MyAshare")
        
        #在网格布局内，使用两个QWidget()部件分别作为左侧菜单模块的部件和右侧内容模块的部件
        self.setFixedSize(960,700)#设置窗口大小
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格
        
        #self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        #self.right_widget.setObjectName('right_widget')
        #self.right_layout = QtWidgets.QGridLayout()
        #self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格
        
        #模块改进
        
        #重要模块
        #同一图形化界面多窗口的切换
        self.right_stacked_widget=QtWidgets.QStackedWidget()
        self.right_stacked_widget.setObjectName('right_stacked_widget')
        #暂不指定其布局格式
        
        
        
        
        
        
        
        
        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_stacked_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        
        #在左侧菜单模块中，继续使用网格对部件进行布局
        #在左侧菜单的布局中添加按钮部件QPushButton()左侧菜单的按钮、菜单列提示和整个窗口的最小化和关闭按钮
        self.left_close = QtWidgets.QPushButton("",self) # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("",self) # 空白按钮
        self.left_mini = QtWidgets.QPushButton("",self)  # 最小化按钮
        
        #左侧菜单按钮绑定按钮点击功能
        self.left_close.clicked.connect(self.close)
        self.left_mini.clicked.connect(self.showMinimized)
        self.left_visit.clicked.connect(self.slot_max_or_recv)
        
        #根据可视化数据和图表来确定
        self.left_label_1 = QtWidgets.QPushButton("主要功能")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("我的")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')
        
        #使用qtawesome这个第三方库来实现按钮中的Font Awesome字体图表的显示
        #查询网址http://www.fontawesome.com.cn/faicons/
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.database',color='white'),"股票数据")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.line-chart',color='white'),"指标图示1")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.line-chart',color='white'),"指标图示2")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.home',color='white'),"主页面")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='white'),"下载管理")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.forward',color='white'),"股票预测")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment',color='white'),"反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question',color='white'),"遇到问题")
        self.left_button_9.setObjectName('left_button')
        #self.left_xxx = QtWidgets.QPushButton(" ")
        #禁用一部分按钮，用于后续功能的开发
        self.left_button_5.setDisabled(True)
        self.left_button_9.setDisabled(True)
        
        
        
        
        
        
        
        
        #绑定按钮功能
        #
        #self.left_button_1.setShortcut('enter+a')
        
        
        self.left_button_1.clicked.connect(self.Tow_1)
        self.left_button_4.clicked.connect(self.Tow_4)
        self.left_button_7.clicked.connect(self.Tow_7)
        self.left_button_8.clicked.connect(self.Tow_8)
        self.left_button_2.clicked.connect(self.Tow_2)
        self.left_button_3.clicked.connect(self.Tow_3)
        self.left_button_6.clicked.connect(self.Tow_6)
        
        
        
        
        
        
        
        
        
        
        
        
        #方便后续调整，列，行，宽，长
        self.left_layout.addWidget(self.left_mini, 0, 0,1,1)
        self.left_layout.addWidget(self.left_close, 0, 2,1,1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        
        self.left_layout.addWidget(self.left_label_1,3,0,1,3)
        self.left_layout.addWidget(self.left_button_1, 4, 0,1,3)
        self.left_layout.addWidget(self.left_button_2, 5, 0,1,3)
        self.left_layout.addWidget(self.left_button_3, 6, 0,1,3)
        
        self.left_layout.addWidget(self.left_label_2, 1, 0,1,3)
        self.left_layout.addWidget(self.left_button_4, 2, 0,1,3)
        #self.left_layout.addWidget(self.left_button_5, 3, 0,1,3)
        self.left_layout.addWidget(self.left_button_6, 7, 0,1,3)
        self.left_layout.addWidget(self.left_label_3, 8, 0,1,3)
        self.left_layout.addWidget(self.left_button_7, 10, 0,1,3)
        self.left_layout.addWidget(self.left_button_8, 11, 0,1,3)
        #self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        
        #右侧内容模块
        
        #默认页面form1
        self.form1=QtWidgets.QWidget()  
        self.right_stacked_widget.addWidget(self.form1) 
        self.form1_layout=QtWidgets.QGridLayout(self.form1)
        #搜索模块
        #定义一个文本和n个搜索框
        #通过QLable()部件和QLineEdit()部件来实现
        #这两个部件同时包裹在一个网格布局的QWidget()部件
        self.right_bar_widget = QtWidgets.QWidget() # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout() # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' '+'输入栏  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        
        #由于可能有多个输入参数，这里多列出几个输入框
        self.frequency = QtWidgets.QLineEdit()
        self.frequency.setPlaceholderText("行情时间线1m/30m/1d/1w")
        self.count= QtWidgets.QLineEdit()
        self.count.setPlaceholderText("时间段数")
        self.end_date= QtWidgets.QLineEdit()
        self.end_date.setPlaceholderText("截止日期查看历史行情,可选")
        self.stock_code= QtWidgets.QLineEdit()
        self.stock_code.setPlaceholderText("输入标准股票代码(sh000001/000001.XSHG/399006.XSHE)，点击左侧菜单栏功能按钮启动")
        self.clear_input=QtWidgets.QPushButton("清空")
        self.clear_input.clicked.connect(self.clear_input_f)
        
        self.right_bar_layout.addWidget(self.search_icon,0,0,1,1)
        self.right_bar_layout.addWidget(self.frequency,0,1,1,2)
        self.right_bar_layout.addWidget(self.count,0,3,1,2)
        self.right_bar_layout.addWidget(self.end_date,0,5,1,2)
        self.right_bar_layout.addWidget(self.clear_input,0,7,1,1)
        self.right_bar_layout.addWidget(self.stock_code,1,1,1,6)
        self.form1_layout.addWidget(self.right_bar_widget, 0, 0, 2, 8)
        
        #联系我们页面form2(次序按照设计顺序)
        self.form2=QtWidgets.QWidget()
        self.right_stacked_widget.addWidget(self.form2)

        self.form2_layout=QtWidgets.QVBoxLayout(self.form2)
        
        #设置布局
        self.we_box=QtWidgets.QWidget()
        self.we_box_layout=QtWidgets.QHBoxLayout()
        self.we_box.setLayout(self.we_box_layout)
        self.we_label=QtWidgets.QLabel("制作人名单")
        self.we_label.setAlignment(QtCore.Qt.AlignCenter)
        self.we_label.setFont(qtawesome.font('fa',16))
        self.form2_layout.addWidget(self.we_label)
        self.table_view=QtWidgets.QTableView()
        #存储任意层次结构的数据，5行3列
        self.itemModel=QtGui.QStandardItemModel(6,3)
        #表头
        self.itemModel.setHorizontalHeaderLabels(["代号","联系方式QQ","邮箱"])
        #输入内容
        for (row, producer) in enumerate(self.producer_list):
            for column in range(len(producer)):
                self.itemModel.setItem(row, column,QtGui.QStandardItem(producer[column]))
        #绑定数据源
        self.table_view.setModel(self.itemModel)
        #最后一列自动拉伸
        self.table_view.horizontalHeader().setStretchLastSection(True)
        #合并行列
        self.table_view.setSpan(3,0,1,2)
        self.table_view.setSpan(4,0,1,2)
        self.table_view.setSpan(5,0,1,3)
        # 单元格不可编辑
        self.table_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.form2_layout.addWidget(self.table_view)
        
        
        
        
        
        #反馈建议页面form3
        self.form3=QtWidgets.QWidget()
        self.right_stacked_widget.addWidget(self.form3)
        self.form3_layout=QtWidgets.QVBoxLayout(self.form3)
        #总体采用垂直布局，box采用水平布局
        #多行文本框
        self.suggest_box=QtWidgets.QWidget()
        self.suggest_box_layout=QtWidgets.QHBoxLayout()
        self.suggest_box.setLayout(self.suggest_box_layout)
        self.submit_text=QtWidgets.QTextEdit()
        self.submit_text.setPlaceholderText("你的建议，是我们前进的动力")
        self.suggest_label=QtWidgets.QLabel("建议：")
        self.suggest_label.setFont(qtawesome.font('fa',16))
        self.suggest_box_layout.addWidget(self.suggest_label)
        self.suggest_box_layout.addWidget(self.submit_text)
        self.suggest_box_layout.setStretch(1,1)
        self.form3_layout.addWidget(self.suggest_box)
        
        self.button_box=QtWidgets.QWidget()
        self.button_box_layout=QtWidgets.QHBoxLayout()
        self.button_box.setLayout(self.button_box_layout)
        self.copy_button=QtWidgets.QPushButton("复制")
        self.paste_button=QtWidgets.QPushButton("粘贴")
        self.clear_button=QtWidgets.QPushButton("清空")
        self.submit_button=QtWidgets.QPushButton("提交")
        
        self.copy_button.clicked.connect(self.copy)
        self.paste_button.clicked.connect(self.paste)
        self.clear_button.clicked.connect(self.clear)
        self.submit_button.clicked.connect(self.submit)
        self.button_box_layout.addWidget(self.copy_button)
        self.button_box_layout.addWidget(self.paste_button)
        self.button_box_layout.addWidget(self.clear_button)
        self.button_box_layout.addWidget(self.submit_button)
        self.button_box_layout.addWidget(QtWidgets.QLabel(),10)
        self.button_box.setContentsMargins(250,20,200,200)
        self.form3_layout.addWidget(self.button_box)
        
        
        
    
        
        #股票数据查询界面
        #由于个股查询界面的信息需要等Tow_1运行结束后才能开始
        self.form4=QtWidgets.QWidget()
        self.right_stacked_widget.addWidget(self.form4)
        self.form4_layout=QtWidgets.QVBoxLayout(self.form4)
        
        #右侧下部模块设计为主要的数据可视化图片展示区以及可能的基本数据区
        self.fun_box=QtWidgets.QWidget()
        self.fun_box_layout=QtWidgets.QGridLayout()
        self.fun_box.setLayout(self.fun_box_layout)
        self.show_static=QtWidgets.QPushButton("显示数据")
        self.clear_one=QtWidgets.QPushButton("清除")
        self.clear_all=QtWidgets.QPushButton("清空")
        self.fun_box_layout.addWidget(self.show_static, 0, 0, 1, 1)
        self.fun_box_layout.addWidget(self.clear_one, 0, 1, 1, 1)
        self.fun_box_layout.addWidget(self.clear_all, 0, 2, 1, 1)
        self.show_static.clicked.connect(self.static_1)
        self.clear_one.clicked.connect(self.clear_one_static)
        self.clear_all.clicked.connect(self.clear_all_static)
        
        self.form4_layout.addWidget(self.fun_box)
        
        
        #股票图像呈现界面
        self.form5=QtWidgets.QWidget()
        self.right_stacked_widget.addWidget(self.form5)
        self.form5_layout=QtWidgets.QVBoxLayout(self.form5)
        
        #创建一个继承了FigureCanvas的类MyFigureCanvas的对象figureCanvas
        self.figure_box1=QtWidgets.QWidget()
        self.figure_box1_layout=QtWidgets.QHBoxLayout()
        self.figure_box1.setLayout(self.figure_box1_layout)
        
        self.select_tip=QtWidgets.QLineEdit()
        self.select_tip.setText("注意：先生成再选择指标按钮输出对应图像")
        self.select_tip.setAlignment(QtCore.Qt.AlignCenter)
        self.select_tip.setReadOnly(True)
        self.figure_box1_layout.addWidget(self.select_tip)
        
        self.figure_generate1=QtWidgets.QPushButton("生成")
        self.figure_generate1.clicked.connect(self.generate_figure1)
        self.figure_box1_layout.addWidget(self.figure_generate1)
        
        self.select_mark1=QtWidgets.QLabel("指标：")
        self.select_mark1.setFont(qtawesome.font('fa',16))
        self.figure_box1_layout.addWidget(self.select_mark1)
        
        self.original_button=QtWidgets.QPushButton("ORIGINAL")
        self.original_button.clicked.connect(self.show_original)
        self.figure_box1_layout.addWidget(self.original_button)
        
        self.boll_button=QtWidgets.QPushButton("BOLL")
        self.boll_button.clicked.connect(self.show_boll)
        self.figure_box1_layout.addWidget(self.boll_button)
        
        self.kdj_button=QtWidgets.QPushButton("KDJ")
        self.kdj_button.clicked.connect(self.show_kdj)
        self.figure_box1_layout.addWidget(self.kdj_button)
        
        self.macd_button=QtWidgets.QPushButton("MACD")
        self.macd_button.clicked.connect(self.show_macd)
        self.figure_box1_layout.addWidget(self.macd_button)
        
        self.figure_clear1=QtWidgets.QPushButton("清除")
        self.figure_clear1.clicked.connect(self.clear_figure1)
        self.figure_box1_layout.addWidget(self.figure_clear1)
        
        self.form5_layout.addWidget(self.figure_box1)
        #figure_box1
        
        # self.figure_box1=QtWidgets.QWidget()
        # self.figure_box1_layout=QtWidgets.QGridLayout()
        # self.figure_box1.setLayout(self.figure_box1_layout)
        # #TechCurve("sh600050")
        # #工具栏 用于操作图片
        # self.mark_text_1=QtWidgets.QLabel("ORIGINAL")
        # self.mark_text_1.setFont(qtawesome.font('fa',16))
        # self.figure_box1_layout.addWidget(self.mark_text_1,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        # self.mark_show=QtWidgets.QPushButton("展示数据图表")
        # self.mark_show.clicked.connect(self.show_mark)
        # self.figure_box1_layout.addWidget(self.mark_show,0,1,1,1)
        
        # self.mark_clear=QtWidgets.QPushButton("清除")
        # self.mark_clear.clicked.connect(self.clear_mark)
        # self.figure_box1_layout.addWidget(self.mark_clear,0,2,1,1)
        
        # self.figureCanvas_1=MyFigureCanvas()
        # self.navigationToolbar_1=NavigationToolbar2QT(self.figureCanvas_1, self)
        # self.figure_box1_layout.addWidget(self.navigationToolbar_1,1,0,1,1)
        # self.form5_layout.addWidget(self.figure_box1,0,0,1,1)
        
        
        
        # #figure_box2
        
        # self.figure_box2=QtWidgets.QWidget()
        # self.figure_box2_layout=QtWidgets.QGridLayout()
        # self.figure_box2.setLayout(self.figure_box2_layout)
        
        # self.mark_text_2=QtWidgets.QLabel("BOLL")
        # self.mark_text_2.setFont(qtawesome.font('fa',16))
        # self.figure_box2_layout.addWidget(self.mark_text_2,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        
        
        # # self.boll_clear=QtWidgets.QPushButton("清除")
        # # self.boll_clear.clicked.connect(self.clear_boll)
        # # self.figure_box2_layout.addWidget(self.boll_clear,0,1,1,1)
        
        # self.figureCanvas_2=MyFigureCanvas()
        # self.navigationToolbar_2=NavigationToolbar2QT(self.figureCanvas_2, self)
        # self.figure_box2_layout.addWidget(self.navigationToolbar_2,1,0,1,1)
        # self.form5_layout.addWidget(self.figure_box2,0,1,1,1)
        
        
        # #figure_box3
        
        # self.figure_box3=QtWidgets.QWidget()
        # self.figure_box3_layout=QtWidgets.QGridLayout()
        # self.figure_box3.setLayout(self.figure_box3_layout)
        
        # self.mark_text_3=QtWidgets.QLabel("KDJ")
        # self.mark_text_3.setFont(qtawesome.font('fa',16))
        # self.figure_box3_layout.addWidget(self.mark_text_3,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        
        
        # # self.kdj_clear=QtWidgets.QPushButton("清除")
        # # self.kdj_clear.clicked.connect(self.clear_kdj)
        # # self.figure_box3_layout.addWidget(self.kdj_clear,0,1,1,1)
        
        # self.figureCanvas_3=MyFigureCanvas()
        # self.navigationToolbar_3=NavigationToolbar2QT(self.figureCanvas_3, self)
        # self.figure_box3_layout.addWidget(self.navigationToolbar_3,1,0,1,1)
        # self.form5_layout.addWidget(self.figure_box3,1,0,1,1)
        
        # #figure_box4
        # self.figure_box4=QtWidgets.QWidget()
        # self.figure_box4_layout=QtWidgets.QGridLayout()
        # self.figure_box4.setLayout(self.figure_box4_layout)
        
        # self.mark_text_4=QtWidgets.QLabel("MACD")
        # self.mark_text_4.setFont(qtawesome.font('fa',16))
        # self.figure_box4_layout.addWidget(self.mark_text_4,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        
        # # self.macd_clear=QtWidgets.QPushButton("清除")
        # # self.macd_clear.clicked.connect(self.clear_macd)
        # # self.figure_box4_layout.addWidget(self.macd_clear,0,1,1,1)
        
        # self.figureCanvas_4=MyFigureCanvas()
        # self.navigationToolbar_4=NavigationToolbar2QT(self.figureCanvas_4, self)
        # self.figure_box4_layout.addWidget(self.navigationToolbar_4,1,0,1,1)
        # self.form5_layout.addWidget(self.figure_box4,1,1,1,1)
        
        
        
        #股票指标呈现界面
        self.form6=QtWidgets.QWidget()
        self.right_stacked_widget.addWidget(self.form6)
        self.form6_layout=QtWidgets.QVBoxLayout(self.form6)
        
        self.figure_box2=QtWidgets.QWidget()
        self.figure_box2_layout=QtWidgets.QHBoxLayout()
        self.figure_box2.setLayout(self.figure_box2_layout)
        
        self.select_tip2=QtWidgets.QLineEdit()
        self.select_tip2.setText("注意：先生成再选择指标按钮输出对应图像")
        self.select_tip2.setAlignment(QtCore.Qt.AlignCenter)
        self.select_tip2.setReadOnly(True)
        self.figure_box2_layout.addWidget(self.select_tip2)
        
        self.figure_generate2=QtWidgets.QPushButton("生成")
        self.figure_generate2.clicked.connect(self.generate_figure2)
        self.figure_box2_layout.addWidget(self.figure_generate2)
        
        self.select_mark2=QtWidgets.QLabel("指标：")
        self.select_mark2.setFont(qtawesome.font('fa',16))
        self.figure_box2_layout.addWidget(self.select_mark2)
        
        self.rsi_button=QtWidgets.QPushButton("RSI")
        self.rsi_button.clicked.connect(self.show_rsi)
        self.figure_box2_layout.addWidget(self.rsi_button)
        
        self.dmi_button=QtWidgets.QPushButton("DMI")
        self.dmi_button.clicked.connect(self.show_dmi)
        self.figure_box2_layout.addWidget(self.dmi_button)
        
        self.brar_button=QtWidgets.QPushButton("BRAR")
        self.brar_button.clicked.connect(self.show_brar)
        self.figure_box2_layout.addWidget(self.brar_button)
        
        self.wr_button=QtWidgets.QPushButton("W&R")
        self.wr_button.clicked.connect(self.show_wr)
        self.figure_box2_layout.addWidget(self.wr_button)
        
        self.figure_clear2=QtWidgets.QPushButton("清除")
        self.figure_clear2.clicked.connect(self.clear_figure2)
        self.figure_box2_layout.addWidget(self.figure_clear2)
        
        self.form6_layout.addWidget(self.figure_box2)
        # #figure_box5
        
        # self.figure_box5=QtWidgets.QWidget()
        # self.figure_box5_layout=QtWidgets.QGridLayout()
        # self.figure_box5.setLayout(self.figure_box5_layout)
        # #TechCurve("sh600050")
        # #工具栏 用于操作图片
        # self.mark_text_5=QtWidgets.QLabel("RSI")
        # self.mark_text_5.setFont(qtawesome.font('fa',16))
        # self.figure_box5_layout.addWidget(self.mark_text_5,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        # self.mark_show_2=QtWidgets.QPushButton("展示数据图表")
        # self.mark_show_2.clicked.connect(self.show_mark_2)
        # self.figure_box5_layout.addWidget(self.mark_show_2,0,1,1,1)
        
        # # self.mark_clear=QtWidgets.QPushButton("清除")
        # # self.mark_clear.clicked.connect(self.clear_mark)
        # # self.figure_box1_layout.addWidget(self.mark_clear,0,2,1,1)
        
        # self.figureCanvas_5=MyFigureCanvas()
        # self.navigationToolbar_5=NavigationToolbar2QT(self.figureCanvas_5, self)
        # self.figure_box5_layout.addWidget(self.navigationToolbar_5,1,0,1,1)
        # self.form6_layout.addWidget(self.figure_box5,0,0,1,1)
        
        
        
        # #figure_box6
        
        # self.figure_box6=QtWidgets.QWidget()
        # self.figure_box6_layout=QtWidgets.QGridLayout()
        # self.figure_box6.setLayout(self.figure_box6_layout)
        
        # self.mark_text_6=QtWidgets.QLabel("DMI")
        # self.mark_text_6.setFont(qtawesome.font('fa',16))
        # self.figure_box6_layout.addWidget(self.mark_text_6,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        
        
        # # self.boll_clear=QtWidgets.QPushButton("清除")
        # # self.boll_clear.clicked.connect(self.clear_boll)
        # # self.figure_box2_layout.addWidget(self.boll_clear,0,1,1,1)
        
        # self.figureCanvas_6=MyFigureCanvas()
        # self.navigationToolbar_6=NavigationToolbar2QT(self.figureCanvas_6, self)
        # self.figure_box6_layout.addWidget(self.navigationToolbar_6,1,0,1,1)
        # self.form6_layout.addWidget(self.figure_box6,0,1,1,1)
        
        
        # #figure_box7
        
        # self.figure_box7=QtWidgets.QWidget()
        # self.figure_box7_layout=QtWidgets.QGridLayout()
        # self.figure_box7.setLayout(self.figure_box7_layout)
        
        # self.mark_text_7=QtWidgets.QLabel("BRAR")
        # self.mark_text_7.setFont(qtawesome.font('fa',16))
        # self.figure_box7_layout.addWidget(self.mark_text_7,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        
        
        # # self.kdj_clear=QtWidgets.QPushButton("清除")
        # # self.kdj_clear.clicked.connect(self.clear_kdj)
        # # self.figure_box3_layout.addWidget(self.kdj_clear,0,1,1,1)
        
        # self.figureCanvas_7=MyFigureCanvas()
        # self.navigationToolbar_7=NavigationToolbar2QT(self.figureCanvas_7, self)
        # self.figure_box7_layout.addWidget(self.navigationToolbar_7,1,0,1,1)
        # self.form6_layout.addWidget(self.figure_box7,1,0,1,1)
        
        # #figure_box8
        # self.figure_box8=QtWidgets.QWidget()
        # self.figure_box8_layout=QtWidgets.QGridLayout()
        # self.figure_box8.setLayout(self.figure_box8_layout)
        
        # self.mark_text_8=QtWidgets.QLabel("W&R")
        # self.mark_text_8.setFont(qtawesome.font('fa',16))
        # self.figure_box8_layout.addWidget(self.mark_text_8,0,0,1,1,alignment=QtCore.Qt.AlignCenter)
        
        
        # # self.macd_clear=QtWidgets.QPushButton("清除")
        # # self.macd_clear.clicked.connect(self.clear_macd)
        # # self.figure_box4_layout.addWidget(self.macd_clear,0,1,1,1)
        
        # self.figureCanvas_8=MyFigureCanvas()
        # self.navigationToolbar_8=NavigationToolbar2QT(self.figureCanvas_8, self)
        # self.figure_box8_layout.addWidget(self.navigationToolbar_8,1,0,1,1)
        # self.form6_layout.addWidget(self.figure_box8,1,1,1,1)
        
        
        #股票预测呈现界面
        self.form7=QtWidgets.QWidget()
        self.right_stacked_widget.addWidget(self.form7)
        self.form7_layout=QtWidgets.QVBoxLayout(self.form7)
        
        
        self.combo_box=QtWidgets.QWidget()
        self.combo_box_layout=QtWidgets.QHBoxLayout()
        self.combo_box.setLayout(self.combo_box_layout)
        
        self.tip=QtWidgets.QLineEdit()
        self.tip.setText("证券代码请在主界面填写")
        self.tip.setAlignment(QtCore.Qt.AlignCenter)
        self.tip.setReadOnly(True)
        self.combo_box_layout.addWidget(self.tip)
        
        self.select_label=QtWidgets.QLabel("预测天数")
        self.select_label.setFont(qtawesome.font('fa',16))
        self.combo_box_layout.addWidget(self.select_label)
        
        self.combo=QtWidgets.QComboBox(self)
        self.combo.setFixedSize(140, 20)
        self.combo.addItems(['1','2','3','4','5'])
        # 选中一个已经选中的下拉选项时，触发事
        self.combo_box_layout.addWidget(self.combo)
        
        self.fore_start=QtWidgets.QPushButton("开始预测")
        self.fore_start.clicked.connect(self.start_fore)
        self.combo_box_layout.addWidget(self.fore_start)
        
        self.fore_clear=QtWidgets.QPushButton("清除")
        self.fore_clear.clicked.connect(self.clear_fore)
        self.combo_box_layout.addWidget(self.fore_clear)
        
        
        self.form7_layout.addWidget(self.combo_box)
        
        
        
        
        
        
        
        
        #使用QSS Qt StyleSheet和部件属性美化窗口部件
        
        #窗口控制按钮
        #首先使用QPushButton()的setFixedSize()方法设置按钮的大小
        self.left_close.setFixedSize(15,15) # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15) # 设置最小化按钮大小
        
        #通过通过setStyleSheet()方法，设置按钮部件的QSS样式
        #左侧按钮默认为淡绿色，鼠标悬浮时为深绿色
        #中间按钮默认为淡黄色，鼠标悬浮时为深黄色
        #右侧按钮默认为浅红色，鼠标悬浮时为红色
        self.left_close.setStyleSheet('''
        QPushButton{background:#F76677;border-radius:7px;border:none;}
        QPushButton:hover{background:red;}
        ''')
        self.left_visit.setStyleSheet('''
        QPushButton{background:#F7D674;border-radius:7px;border:none;}
        QPushButton:hover{background:yellow;}
        ''')
        self.left_mini.setStyleSheet('''
        QPushButton{background:#6DDF6D;border-radius:7px;border:none;}
        QPushButton:hover{background:green;}
        ''')
        
        #左侧菜单栏
        #将左侧菜单中的按钮和文字设置为白色，并且将按钮的边框去掉
        #且鼠标悬浮时令按钮左端呈现红色
        self.left_widget.setStyleSheet('''
        QPushButton{border:none;color:white;}
        QPushButton#left_label{
            border:none;
            border-bottom:1px solid white;
            font-size:18px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        QWidget#left_widget{
        background:gray;
        border-top:1px solid white;
        border-bottom:1px solid white;
        border-left:1px solid white;
        border-top-left-radius:10px;
        border-bottom-left-radius:10px;
        }
        ''')
        
        #右侧背景顶部搜索栏
        self.frequency.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:50px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.count.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:50px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.end_date.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:50px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        
            
        self.stock_code.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.clear_input.setStyleSheet('''
            QPushButton{
                background-color:LightSteelBlue;
                color:white;
                border:none;
                border-radius:8px;
                padding:2px 4px;
                width:20px
                }
            QPushButton:hover{
                color:black;
                background-color:#767778;
                font-weight:500;}''')
        self.fun_box.setStyleSheet('''
            QPushButton{
                background-color:LightSteelBlue;
                color:white;
                border:none;
                border-radius:8px;
                padding:2px 4px;
                width:30px;
                height:20px;
                }
            QPushButton:hover{
                color:black;
                background-color:#767778;
                font-weight:500;}
                                   
                                   ''')
        self.form5.setStyleSheet('''
            QPushButton{
                background-color:LightSteelBlue;
                color:white;
                border:none;
                border-radius:8px;
                padding:2px 4px;
                }
            QPushButton:hover{
                color:black;
                background-color:#767778;
                font-weight:500;}
                }
            QLineEdit{
                border:1px solid gray;
                width:50px;
                border-radius:10px;
                padding:2px 4px;
                }''')
        self.form6.setStyleSheet('''
            QPushButton{
                background-color:LightSteelBlue;
                color:white;
                border:none;
                border-radius:8px;
                padding:2px 4px;
                }
            QPushButton:hover{
                color:black;
                background-color:#767778;
                font-weight:500;}
                }
            QLineEdit{
                border:1px solid gray;
                width:50px;
                border-radius:10px;
                padding:2px 4px;
                }''')
        self.form7.setStyleSheet('''
            QPushButton{
                background-color:LightSteelBlue;
                color:white;
                border:none;
                border-radius:8px;
                padding:2px 4px;
                }
            QPushButton:hover{
                color:black;
                background-color:#767778;
                font-weight:500;}
            QLineEdit{
                border:1px solid gray;
                width:50px;
                border-radius:10px;
                padding:2px 4px;
                }
            
                                 ''')
        #右侧大背景
        self.right_stacked_widget.setStyleSheet('''
            QWidget#right_stacked_widget{
            color:#232C51;
            background:white;
            border-top:1px solid darkGray;
            border-bottom:1px solid darkGray;
            border-right:1px solid darkGray;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
            }
        ''')
        self.form3.setStyleSheet('''
        QTextEdit{
            border:1px solid gray;
            border-radius:10px;
            max-height:200px;
            font-size:18px;
            font-family:"微软雅黑"
            }
        QPushButton{
            font-size:12px;
            border-radius:2px;
            padding:2px 4px;
            border:1px solid gray;
            height:20px;
            width:40px;
            }         
        QPushButton:hover{
            background-color: LightSteelBlue;
            font-weight:500;}
                                 ''')
        
        #设置窗口背景透明
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        
        #通过窗口的setWindowFlag()属性去除窗口边框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框
        #发现去除边框后，左侧部件没有背景颜色和边框显示，我们再对左侧部件添加QSS属性
        #相关代码添加至self.left_widget.setStyleSheet配置中
        
        #去除图形化界面中左侧部件和右侧部件中的一条缝隙
        
        self.main_layout.setSpacing(0)
        
        
        #窗口最大化与恢复
    def slot_max_or_recv(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def clear_input_f(self):
        self.frequency.setText("")
        self.count.setText("")
        self.end_date.setText("")
        self.stock_code.setText("")
        
    
    def copy(self):
        #copy函数同时作为提取文本框的功能
        text=self.submit_text.toPlainText()
        #放在剪切板
        clipboard=QtWidgets.QApplication.clipboard()
        clipboard.setText(text)
    def paste(self):
        clipboard=QtWidgets.QApplication.clipboard()
        self.submit_text.setPlainText(clipboard.text())
    def clear(self):
        self.submit_text.clear()
    def submit(self):
        text=self.submit_text.toPlainText()
        if text.strip() == "":
            self.submit_text.setFocus()
            QtWidgets.QMessageBox.warning(self, "内容为空", 
                                "建议空空如也,请输入你的宝贵意见", 
                                QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self, "提交成功", 
                                    "你的宝贵意见,我们收到了，谢谢你", 
                                    QtWidgets.QMessageBox.Ok)
            # print(text)
            # 设计为存储到mongodb数据库中
            # data={'time:':time.time(),'feedback_text':text}
            # mongobase_1=MongoBase()
            # mongobase_1.save_feedback_to_mongo(data)
            # save_feedback_to_mongo(data)
            
    #将"主页面"窗口 即默认窗口  加入到窗口主部件中并进行配置
    def Tow_4(self):
        self.right_stacked_widget.setCurrentIndex(0)
    #将"关注我们"窗口加入到窗口主部件中并进行配置
    def Tow_8(self):
        #Index从0开始且按照添加到right_stacked_widget的顺序
        self.right_stacked_widget.setCurrentIndex(1)
    def Tow_7(self):
        #Index从0开始且按照添加到right_stacked_widget的顺序
        self.right_stacked_widget.setCurrentIndex(2)
    def Tow_1(self):
        self.right_stacked_widget.setCurrentIndex(3)
    def static_1(self):
        self.stock_code_text=self.stock_code.text()
        self.frequency_text=self.frequency.text()
        self.count_text=self.count.text()
        self.end_date_text=self.end_date.text()
        
        
        if (self.stock_code_text=="" )|(self.frequency_text=="")|(self.count_text==""):
            QtWidgets.QMessageBox.warning(self, "参数缺失", 
                                "请输入必要的参数内容", 
                                QtWidgets.QMessageBox.Ok)
            self.right_stacked_widget.setCurrentIndex(0)
        else:
            self.count_num=int(self.count_text)
            df=get_price(self.stock_code_text,self.end_date_text,self.count_num,self.frequency_text)
            #print(df)
            # save_dataframe_to_mongo(df)
            self.dataframe_box=QtWidgets.QWidget()
            self.dataframe_box_layout=QtWidgets.QVBoxLayout()
            self.dataframe_box.setLayout(self.dataframe_box_layout)
            self.show_code=QtWidgets.QLineEdit()
            self.show_code.setText("证券代码名："+self.stock_code_text)
            #设置此处文本框为只读
            self.show_code.setReadOnly(True)
            self.dataframe_box_layout.addWidget(self.show_code)
            
            self.model=pandasModel(df)
            self.dataframe_view=QtWidgets.QTableView()
            self.dataframe_box_layout.addWidget(self.dataframe_view)
            self.dataframe_view.setModel(self.model)
            self.form4_layout.addWidget(self.dataframe_box)
        #def get_price(code, end_date='',count=10, frequency='1d'):
        #print(self.df)
            self.show_code.setStyleSheet('''
                QLineEdit{
                    border:1px solid gray;
                    width:50px;
                    border-radius:10px;
                    padding:2px 4px;
                    }
                                         ''')
    
    def clear_one_static(self):
        if self.form4_layout.itemAt(1)==None:
            QtWidgets.QMessageBox.warning(self, "数据异常", 
                                "还没有添加任何数据哦~", 
                                QtWidgets.QMessageBox.Ok)
        else:
            self.form4_layout.itemAt(1).widget().deleteLater()
    def clear_all_static(self):
        if self.form4_layout.itemAt(1)==None:
            QtWidgets.QMessageBox.warning(self, "数据异常", 
                                "还没有添加任何数据哦~", 
                                QtWidgets.QMessageBox.Ok)
        else:
            for i in range(self.form4_layout.count()):
                if i==0:
                    continue
                else:
                    self.form4_layout.itemAt(i).widget().deleteLater()
                
    def Tow_2(self):
        self.right_stacked_widget.setCurrentIndex(4)
    def Tow_3(self):
        self.right_stacked_widget.setCurrentIndex(5)
    def Tow_6(self):
        self.right_stacked_widget.setCurrentIndex(6)
        
    # def __draw_figure__(self):
    #     #该函数中的步骤和调用方法和plot大致相同
    #     self.axes = self.figureCanvas.figure.add_subplot(221)
    #     self.axes.set_title("line chart")
    #     self.axes.set_xlabel("x")
    #     self.axes.set_ylabel("y")
    #     x = range(2, 26, 2)
    #     y = [15, 13, 14.5, 17, 20, 25, 26, 26, 27, 22, 18, 15]
    #     self.axes.plot(x, y, color='red')
    #     #TechCurve('sh600050')
    def generate_figure1(self):
        self.stock_code_text=self.stock_code.text()
        self.frequency_text=self.frequency.text()
        self.count_text=self.count.text()
        self.end_date_text=self.end_date.text()
        
        if (self.stock_code_text=="" )|(self.frequency_text=="")|(self.count_text==""):
            QtWidgets.QMessageBox.warning(self, "生成失败", 
                                "请输入必要的参数内容", 
                                QtWidgets.QMessageBox.Ok)
            self.right_stacked_widget.setCurrentIndex(0)
        else:
            self.count_num=int(self.count_text)
            TechCurve1(self.stock_code_text,self.frequency_text,self.count_num,self.end_date_text)
            # self.original_pic=QtGui.QPixmap('./ORIGINAL.jpg')
            # self.original_label=QtWidgets.QLabel()
            # self.original_label.setStyleSheet("border:1px solid black")
            # self.original_label.setPixmap(self.origianl_pic)
            # self.figure_box1_layout.addWidget(self.original_label,2,0,1,1)
            
    def show_original(self):
        self.original_button=QtWidgets.QToolButton()
        # self.original_button.setText("证券代码："+self.stock_code_text)
        self.original_button.setIcon(QtGui.QIcon('./img/ORIGINAL.jpg'))
        self.original_button.setIconSize(QtCore.QSize(800,560))
        self.original_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form5_layout.addWidget(self.original_button)
    def show_boll(self):
        self.boll_button=QtWidgets.QToolButton()
            # self.boll_button.setText("证券代码："+self.stock_code_text)
        self.boll_button.setIcon(QtGui.QIcon('./img/BOLL.jpg'))
        self.boll_button.setIconSize(QtCore.QSize(800,560))
        self.boll_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form5_layout.addWidget(self.boll_button)
    def show_kdj(self):
        self.kdj_button=QtWidgets.QToolButton()
        # self.kdj_button.setText("证券代码："+self.stock_code_text)
        self.kdj_button.setIcon(QtGui.QIcon('./img/KDJ.jpg'))
        self.kdj_button.setIconSize(QtCore.QSize(800,560))
        self.kdj_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form5_layout.addWidget(self.kdj_button)
    def show_macd(self):
        self.macd_button=QtWidgets.QToolButton()
        # self.macd_button.setText("证券代码："+self.stock_code_text)
        self.macd_button.setIcon(QtGui.QIcon('./img/MACD.jpg'))
        self.macd_button.setIconSize(QtCore.QSize(800,560))
        self.macd_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form5_layout.addWidget(self.macd_button)
    def clear_figure1(self):
        if self.form5_layout.itemAt(1)==None:
            QtWidgets.QMessageBox.warning(self, "数据异常", 
                                "还没有添加任何数据哦~", 
                                QtWidgets.QMessageBox.Ok)
        else:
            self.form5_layout.itemAt(1).widget().deleteLater()
    def generate_figure2(self):
        self.stock_code_text=self.stock_code.text()
        self.frequency_text=self.frequency.text()
        self.count_text=self.count.text()
        self.end_date_text=self.end_date.text()
        
        if (self.stock_code_text=="" )|(self.frequency_text=="")|(self.count_text==""):
            QtWidgets.QMessageBox.warning(self, "生成失败", 
                                "请输入必要的参数内容", 
                                QtWidgets.QMessageBox.Ok)
            self.right_stacked_widget.setCurrentIndex(0)
        else:
            self.count_num=int(self.count_text)
            TechCurve2(self.stock_code_text,self.frequency_text,self.count_num,self.end_date_text)
    def show_rsi(self):
        self.rsi_button=QtWidgets.QToolButton()
        self.rsi_button.setIcon(QtGui.QIcon('./img/RSI.jpg'))
        self.rsi_button.setIconSize(QtCore.QSize(800,560))
        self.rsi_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form6_layout.addWidget(self.rsi_button)
    def show_dmi(self):
        self.dmi_button=QtWidgets.QToolButton()
        self.dmi_button.setIcon(QtGui.QIcon('./img/DMI.jpg'))
        self.dmi_button.setIconSize(QtCore.QSize(800,560))
        self.dmi_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form6_layout.addWidget(self.dmi_button)
    def show_brar(self):
        self.brar_button=QtWidgets.QToolButton()
        self.brar_button.setIcon(QtGui.QIcon('./img/BRAR.jpg'))
        self.brar_button.setIconSize(QtCore.QSize(800,560))
        self.brar_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form6_layout.addWidget(self.brar_button)
    def show_wr(self):
        self.wr_button=QtWidgets.QToolButton()
        self.wr_button.setIcon(QtGui.QIcon('./img/W&R.jpg'))
        self.wr_button.setIconSize(QtCore.QSize(800,560))
        self.wr_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.form6_layout.addWidget(self.wr_button)
    
    def clear_figure2(self):
        if self.form6_layout.itemAt(1)==None:
            QtWidgets.QMessageBox.warning(self, "数据异常", 
                                "还没有添加任何数据哦~", 
                                QtWidgets.QMessageBox.Ok)
        else:
            self.form6_layout.itemAt(1).widget().deleteLater()

            
            
            
    def start_fore(self):
        self.stock_code_text=self.stock_code.text()
        if (self.stock_code_text=="" ):
            QtWidgets.QMessageBox.warning(self, "参数缺失", 
                                "请输入必要的参数内容", 
                                QtWidgets.QMessageBox.Ok)
            self.right_stacked_widget.setCurrentIndex(0)
        else:
            self.forecast_day=self.combo.currentIndex()
            self.forcast_day=self.forecast_day+1
            forecast(self.stock_code_text,self.forecast_day)
            self.forecast_button=QtWidgets.QToolButton()
            self.forecast_button.setIcon(QtGui.QIcon('./img/FORECAST.jpg'))
            self.forecast_button.setIconSize(QtCore.QSize(800,560))
            self.forecast_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            self.form7_layout.addWidget(self.forecast_button)
    def clear_fore(self):
        if self.form7_layout.itemAt(1)==None:
            QtWidgets.QMessageBox.warning(self, "Figure异常", 
                                "还没有添加任何Figure哦~", 
                                QtWidgets.QMessageBox.Ok)
        else:
            self.form7_layout.itemAt(1).widget().deleteLater()
            
def main():
    app=QtWidgets.QApplication(sys.argv)
    gui=MainUi()
    gui.show()#程序运行过程中关闭窗口
    sys.exit(app.exec_())#再次运行无法生成窗口
if __name__=='__main__':
    main()