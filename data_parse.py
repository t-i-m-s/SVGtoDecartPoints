import re
from abc import ABC, abstractmethod


COMM_SYMS = r'\w=,.() \-\"\'\n\t'


class Tag(ABC):
    tag_name: str
    pattern: str

    founded_tags = {}

    @abstractmethod
    def __init__(self, tag_body):
        self.data = []
        self.tag_body = tag_body

    @classmethod
    def find(cls, row_dt: str) -> None:
        tag_l = re.findall(cls.pattern, row_dt)
        if tag_l:
            tags_list = cls.founded_tags.get(cls.tag_name)
            for tag_b in tag_l:
                tag_b = re.sub('[\n\t]+', ' ', tag_b)
                tag_b = re.sub(' +', ' ', tag_b)
                tag_b = re.sub(' +"', '"', tag_b)
                tag_b = re.sub(' +\'', '\'', tag_b)
                tag_b = re.sub(' +"', '"', tag_b)
                tag_b = re.sub('" +', '"', tag_b)
                tag_b = re.sub('\' +', '\'', tag_b)
                if tags_list:
                    tags_list.append(cls(tag_b))
                else:
                    cls.founded_tags[cls.tag_name] = [cls(tag_b)]
                    tags_list = cls.founded_tags[cls.tag_name]
        else:
            print(f'{cls.tag_name} tags not find ...')

    @abstractmethod
    def parse(self):
        pass


class Polygon(Tag):
    tag_name = 'polygon'
    pattern = f'<{tag_name}[{COMM_SYMS}]* points=[\"\'][\d\n\t,. ]+[\"\'][{COMM_SYMS}]*\/>'

    def __init__(self, tag_body):
        super().__init__(tag_body)

    def parse(self):
        row_xy = re.search(r'points=[\"\'](.*)[\"\']', self.tag_body).group(1)
        self.data.append([])
        if row_xy.find(',') != -1:
            for xy in row_xy.split(' '):
                xy = xy.split(',')
                self.data[0].append((float(xy[0]), float(xy[1])))
        else:
            row_xy = row_xy.split(' ')
            for i, x in enumerate(row_xy):
                if i % 2 == 0:
                    try:
                        self.data[0].append((float(x), float(row_xy[i + 1])))
                    except IndexError:
                        break
        self.data[0].append(self.data[0][0])


class Path(Tag):
    tag_name = 'path'
    pattern = f'<{tag_name}[{COMM_SYMS}]* d=[\"\'][\w,. \-\n\t]+[\"\'][{COMM_SYMS}]*\/>'

    def __init__(self, tag_body):
        super().__init__(tag_body)

    def parse(self):
        row_params = re.search(r'd=[\"\'](.*)[\"\']', self.tag_body).group(1)
        row_commands = re.findall(r'[MmLlHhVvAaCcSsQqTtZz][^A-Za-z]*', row_params)
        commands = []
        for row_cmd in row_commands:
            commands.append(row_cmd[0])
            if len(row_cmd) != 1:
                commands.append(re.findall(r'[-+]?(?:\d*\.\d+|\d+)', row_cmd))
        print(commands)
        # params: list[str] = re.findall(r'[Mm][^Mm]+', row_params)
        # for param in params:
        #     param = re.findall(r'[A-Za-z][\d\-., ]*', param)
        #     for cmd in param:
        #         cmd = re.sub(r' +$', '', cmd)
        #         print(cmd)
        #         cmd, prm = cmd[0], cmd[1:]
        #         if cmd.lower() == 'z':
        #             print("Closing the line...")
        #             break


work_tags = (Polygon,)

if __name__ == '__main__':
    with open('house-2374925.svg', 'r') as svg:
        row_data = svg.read()

    Path.find(row_data)
    Tag.founded_tags['path'][0].parse()
