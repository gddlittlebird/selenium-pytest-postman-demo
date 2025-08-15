#csv_reader.py

from pathlib import Path
import csv
import pytest


# 读取 CSV 数据
def load_csv_data(filename:str) -> list[dict]:
    """
    从tests 目录下加载指定的CSV文件，并以字典形式返回数据列表。
    :param filename: CSV文件名
    :return: List[Dict] 每行数据为一个 dict
    """
    try:
        #获取当前文件位置,回到项目根目录，再进入tests
        csv_path = Path(__file__).resolve().parents[1]/"tests"/filename

        if not csv_path.exists():
            pytest.fail(f"文件不存在：{csv_path}")

        #不指定 newline=""，Python 的 open() 会先把 Windows的\r\n 转换成 \n，
        # 导致 csv.reader() 再处理一次换行符，最终就会出现多一行空行。
        with open(csv_path,newline="",encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return  list(reader)

    except Exception as e:
        pytest.fail(f"加载CSV文件失败:{str(e)}")

