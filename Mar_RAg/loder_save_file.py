import os
import shutil
from langchain_community.document_loaders import UnstructuredFileLoader


class LoderFile(object):
    # 定义允许处理的文件后缀列表，作为类属性
    file_extensions = ['.txt', '.pdf', '.docx', '.xml']

    def __init__(self, file_path):
        self.file_path = file_path

    # 获取文件后缀
    def get_file_extension(self):
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower()  # 将后缀转换为小写

    def read_file(self):
        # 获取文件后缀
        file_extension = self.get_file_extension()
        # 检查文件后缀是否在允许处理的列表中
        if file_extension in self.file_extensions:
            loder = UnstructuredFileLoader(self.file_path)
            doc = loder.load()
            return doc
        else:
            return "对不起，目前不支持该格式文件，请按要求上传文件"


    def save_file(self):
        # 检查文件路径是否存在
        save_dir = "file_data"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        # 获取文件名
        file_name = os.path.basename(self.file_path)  # 直接使用os.path.basename获取文件名
        save_file_name = os.path.join(save_dir, file_name)  # 使用os.path.join正确拼接路径

        # 判断文件是否已经存在于目标路径
        if os.path.abspath(self.file_path) == os.path.abspath(save_file_name):
            return save_file_name  # 如果文件已经存在，则直接返回文件名

        # 判断文件类型并复制文件
        file_extension = self.get_file_extension()
        if file_extension in self.file_extensions:
            shutil.copy(self.file_path, save_file_name)
            return save_file_name  # 返回保存的文件路径
        else:
            return "不支持的文件格式"



if __name__ == '__main__':
    file_path = "data/基于YOLO的智慧景区人流密度统计系统设计与实现_宁毅.pdf"
    processor = LoderFile(file_path)
    test = processor.read_file()
    save_text = processor.save_file()
    print(test)
    print(save_text)
