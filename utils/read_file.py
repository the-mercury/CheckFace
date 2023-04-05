import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class ReadFile:

    @staticmethod
    def read_style_sheet(style_path):
        style_sheet = open(os.path.join(os.path.abspath(root_path), style_path)).read()

        return style_sheet
