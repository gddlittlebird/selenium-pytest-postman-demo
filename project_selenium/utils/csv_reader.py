#csv_reader.py

from pathlib import Path
import csv
import pytest
from utils.config_manager import ConfigManager


# 读取 CSV 数据
def load_csv_data(filename:str, encoding="utf-8") -> list[dict]:
    """
    从tests 目录下加载指定的CSV文件，并以字典形式返回数据列表。
    :param filename: CSV文件名
    :param encoding: 文件编码
    :return: List[Dict] 每行数据为一个 dict
    """

    project_dir = Path(ConfigManager.get_project_dir())
    csv_path = project_dir / "tests" / filename


    try:
        '''
        不指定 newline=""，Python 的 open() 会先把 Windows的\r\n 转换成 \n，
        导致 csv.reader() 再处理一次换行符，最终就会出现多一行空行。
        '''
        with open(csv_path,newline="",encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            return  list(reader)

    except FileNotFoundError:
        pytest.fail(f"CSV文件{csv_path}不存在")
    except Exception as e:
        pytest.fail(f"加载CSV文件失败:{e}")


