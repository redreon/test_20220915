import os
from pathlib import Path
import string
from typing import List
from random import randint, choice
import xml.etree.ElementTree as ET


BASE_PATH = os.path.join('.', 'some_folder')
XML_FILE = os.path.join('xml_data.xml')

FILES_NUM = 10
MIN_NAME_PART_LEN = 4
MAX_NAME_PART_LEN = 10
NAME_PARTS_NUM = 3
NAME_PARTS_SEP = '_'
SYMBS_TO_SKIP = 'j'


def generate_files() -> None:
    # start it once for generate files

    abc_list = string.ascii_letters

    for _ in range(FILES_NUM):
        name_parts: List[str] = []
        for i in range(NAME_PARTS_NUM):
            part_len: int = randint(MIN_NAME_PART_LEN, MAX_NAME_PART_LEN)
            part_name: str = ''.join(choice(abc_list) for l in range(part_len))
            name_parts.append(part_name)

        full_name: str = os.path.join(BASE_PATH, NAME_PARTS_SEP.join(name_parts) + '.pdf')
        with open(full_name, "w") as file:
            file.write("hello world")


def rename_file() -> None:
    data = ET.Element('data')

    for file_name in os.listdir(BASE_PATH):
        file_data: List[str] = file_name.split('.')
        ext: str = file_data.pop(-1)
        file_data: List[str] = file_data[0].split(NAME_PARTS_SEP)

        if SYMBS_TO_SKIP in file_data[-1].lower():
            continue

        item = ET.SubElement(data, 'item')
        item.set('origin_name', file_name)

        old_by_parts_node = ET.SubElement(item, 'old_by_parts')
        old_by_parts_node.set('value', '['+', '.join(file_data)+']')

        file_s = Path(os.path.join(BASE_PATH, file_name)).stat()

        attr = ET.SubElement(item, 'attr')
        for atr in file_s.__dir__():
            if atr.startswith('st'):
                attr.set(str(atr), str(file_s.__getattribute__(atr)))

        file_data.insert(0, file_data.pop(-1))

        new_by_parts_node = ET.SubElement(item, 'new_by_parts')
        new_by_parts_node.set('value', '[' + ', '.join(file_data) + ']')

        new_name = f'{NAME_PARTS_SEP.join(file_data)}.{ext}'
        item.set('new_name', new_name)
        os.rename(os.path.join(BASE_PATH, file_name), os.path.join(BASE_PATH, new_name))

    xml_file = ET.ElementTree(data)
    xml_file.write(XML_FILE)


rename_file()
