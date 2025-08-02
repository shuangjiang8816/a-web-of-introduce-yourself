import json
import os
import time

textbook_list = os.listdir("./课本")

# 读取函数
def read():
    textbook_number = 0
    print("课本列表：\n请选择课本编号")
    for textbook in textbook_list:
        textbook_number += 1
        textbook = f"{textbook_number},{textbook}"
        print(textbook)
    book_choose = input()
    try:
        book_choose = int(book_choose) - 1
        if len(textbook_list) < book_choose or book_choose < 0:
            book_choose = "error"
            print("无效的序号")
    except ValueError or FileNotFoundError:
        print("无效的序号")
        book_choose = "error"
    return book_choose

# 判断是否存在可读取文件
if os.path.exists("./课本"):
    book = read()
    while book == "error":
        if book == "error":
            book = read()
else:
    print("未找到可读取文件，3秒后退出...")
    time.sleep(3)
    os.exit()

# 此上book表示选择序号，此下表示选择的文件
# noinspection PyUnboundLocalVariable
book = textbook_list[book]
try:
    with open(f"./课本/{book}",encoding="utf-8") as f:
        # 此处的information是json文件的内容，以字典呈现
        information = json.load(f)
except Exception as e:
    print(f"{e},文件可能损坏")

# 单元目录选择
def choose_unit():
    print(f"单元数：{information['number']}\n单元列表")
    # 初始化
    unit_number = 0
    unit_list = []
    textbook_word_list = []
    # 遍历单元和单词
    for key,values in information['unit_list'].items():
        unit_number += 1
        print(f"{unit_number}、{key}")
        textbook_word_list.append(values)
        unit_list.append(key)
    error = True
    # 检测序号是否在正常范围内，如果不在就重新选择
    while error:
        error = False
        try:
            choose = int(input("请选择单元序号:")) - 1
            if choose > len(unit_list) or choose < 0:
                error = True
                print("无效的序号，请重新选择")
        except Exception:
            print("无效的序号，请重新选择")
            error = True
    # noinspection PyUnboundLocalVariable
    for values in textbook_word_list[choose].values():
        for words in values:
            for word in words.values():
                print(f"{word}")
    q = input("输入q以退出，回车键继续")
    return q

q = ""
while q != "q":
    q = choose_unit()
