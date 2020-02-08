import hashlib
import os
from termcolor import *


class Checker:
    """
    Check the file through md5 and grant low permissions to new files
    """
    def __init__(self):
        ##############################
        # CONFIG AREA
        ##############################
        # Site root
        self.site_root = "/var/www/html"

        # New file permission
        self.permission = "773"

        # black list
        # The program will check to see if the suffix name contains following character
        self.black_list = ['php']

        # Prompt message font color
        # Opitons: red, green, yellow, blue, magenta, cyan, white.
        self.prompt_color = 'green'
        self.dangerous_file_increase_color = 'red'
        self.ordinary_file_increase_color = 'yellow'
        self.file_decrease_color = 'blue'
        self.file_changed_color = 'white'
        self.error_color = 'red'
        ##############################
        # CONFIG AREA END
        ##############################

        # Location of all files
        self.path = []
        # Store md5 encrypted files and paths.Format is {path:md5(file)}
        self.file_info = {}
        # Found files.
        self.found_info = {}
        # Start init
        self.file_info = self.calc(self.file_finder())
        print(colored("[*] Initialization complete", self.prompt_color))

    def start(self):
        """
        Monitor file status in real time
        :return:
        """
        print(colored("[*] Monitoring file status....", self.prompt_color))
        while True:
            self.found_info = self.file_finder()
            for added in self.increase_finder():
                # If the file is dangerous
                if not self.type_check(added):
                    os.system("chmod {permission} {file}".format(permission=self.permission, file=added))
                    print(colored("[!] Find dangerous file: {file}.Its permission has been changed to {permission}".format(file=added, permission=self.permission), self.dangerous_file_increase_color))
                else:
                    print(colored("[*] Find common file: {file}".format(file=added), self.ordinary_file_increase_color))
            for deleted in self.decrease_finder():
                print(colored("[*] Has been deleted: {file} ".format(file=deleted), self.file_decrease_color))
            for changed in self.changes_finder():
                print(colored("[*] Has been changed: {file}".format(file=changed), self.file_changed_color))
            # Check complete.
            self.file_info = self.found_info

    def type_check(self, file):
        """
        Determines if the suffix name contains characters from the blacklist
        :param file: filename
        :return: safe:True,dangerous:False
        """
        suffix = file.split('.')[-1]
        for item in self.black_list:
            if item in suffix:
                return False
        return True

    def md5(self, info, _type='other'):
        """
        :param info: File path or string
        :param _type: info type, string or file
        :return: md5(info), type:str
        """
        md5_obj = hashlib.md5()
        if _type == 'string':
            info = str(info).encode(encoding='utf8')
        elif _type == 'other':
            info = open(info, 'rb').read()
        else:
            print(colored("[!] MD5 error: Type error!", self.error_color))
            exit()
        md5_obj.update(info)
        return md5_obj.hexdigest()

    def file_finder(self):
        """
        Find all files in path
        :return: {path:md5(file)}
        """
        files_info = os.walk(self.site_root)
        file_paths = []
        for root, dirs, files in files_info:
            for file in files:
                file_paths.append("{root}{sep}{filename}".format(root=root, sep=os.sep, filename=file))
        res = self.calc(file_paths)
        return res

    def calc(self, paths):
        """
        Calculate md5 for files
        :return: {path):md5(file)},type:dict
        """
        res = {}
        if isinstance(paths, str):
            res[paths] = self.md5(paths)
        elif isinstance(paths, list):
            for path in paths:
                res[path] = self.md5(path)
        elif isinstance(paths, dict):
            for path in paths:
                res[path] = self.md5(path)
        else:
            print(colored("[!] Calc Error: Wrong input type: {type}".format(type=type(paths)), self.error_color))
            print(paths)
            exit()
        return res

    def increase_finder(self):
        """
        Checks for new file generation
        :return: increased:{path:md5(file)}; otherwise:{},type:dict
        """
        res = dict()
        if len(self.file_info) < len(self.found_info):
            increased_files = self.file_info.keys() ^ self.found_info.keys()
            for path in increased_files:
                res[path] = self.calc(path)
        return res

    def decrease_finder(self):
        """
        Checks for file deletion
        :return: deleted: {path:'has been delete'};otherwise: {},type:dict
        """
        res = dict()
        if len(self.file_info) > len(self.found_info):
            deleted_files = self.file_info.keys() ^ self.found_info.keys()
            for path in deleted_files:
                res[path] = "has been delete"
        return res

    def changes_finder(self):
        """
        Checks for file changes
        :return: changed:{path:md5(file)}; otherwise: {},type:dict
        """
        res = dict()
        same_keys = self.found_info.keys() & self.file_info
        for same_key in same_keys:
            # Determine whether the values corresponding to the same key are equal
            if self.found_info[same_key] != self.file_info[same_key]:
                res[same_key] = self.found_info[same_key]
        return res

if __name__ == "__main__":
    r0co = Checker()
    r0co.start()
