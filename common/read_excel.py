# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/11/29

E-mail: zh13997821732@163.com


================================================================================

"""

import openpyxl


class Case(object):
    def __init__(self, attrs):
        for item in attrs:
            # print(item)
            setattr(self, item[0], item[1])


class ReadExcel(object):

    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def open(self):
        self.wb = openpyxl.load_workbook(self.file_path)
        self.sheet = self.wb[self.sheet_name]

    def close(self):
        self.wb.close()

    def read_line_data(self):
        # 按行读取数据
        self.open()
        # 按行获取数据 并转换成列表
        rows_data = list(self.sheet.rows)
        # print(rows_data)





        # 处理titles
        titles = []
        for title in rows_data[0]:
            if title.value is not None:
                titles.append(title.value)
        # print(titles)

        # 处理用例数据
        cases = []
        # 从第二行开始到最后 都是用例数据
        for case in rows_data[1:]:
            # data用来临时存放每行的数据
            data = []
            for cell in case:
                data.append(cell.value)
            # print(data)
            # 将titles与每行数据进行打包
            case_data = zip(titles, data)
            # 创建对象 设置属性
            case_obj = Case(case_data)
            # print(case_obj.case_id)
            cases.append(case_obj)
        self.close()
        return cases

    def write_data(self, row, column, value):
        self.open()
        # 指定位置写入数据
        self.sheet.cell(row=row, column=column, value=value)
        self.wb.save(self.file_path)
        self.close()


if __name__ == '__main__':

    import os
    from common.constant import DATA_DIR

    file_path = os.path.join(DATA_DIR, 'api_automation_course.xlsx')

    wb = ReadExcel(file_path, 'login')
    cases = wb.read_line_data()
    for i in cases:
         print(i.case_id, i.title)

    wb.write_data(2, 9, '2412412421')



