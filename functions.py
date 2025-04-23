import json
import os
from datetime import datetime
import subprocess
import requests
class Function:
    def __init__(self, tool_json, custom_function):
        self.tool_json = tool_json
        self.custom_function = custom_function

    # 动态成员函数
    def execute(self, *args, **kwargs):
        return self.custom_function(*args, **kwargs)

all_functions = []

get_weather_tool_json = {"type": "function",
            "function": {
                "description": "获取城市的最近7天的天气信息(返回列表中第一项表示今天)",
                "name": "get_weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名"
                        }
                    },
                    "required": ["city"]
                }
            }}

def get_weather_func(args):
    # 天气API
    base_url = "https://v2.api-m.com/api/weather"
    # 参数
    params = {
        'city' : args["city"]
    }
    try:
        # 发送GET请求
        response = requests.get(base_url, params=params)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析JSON响应
            weather_data = response.json()
            return json.dumps(weather_data)
        else:
            return f"请求失败，状态码: {response.status_code}"
    except Exception as e:
        return f"发生错误: {e}"



get_weather = Function(get_weather_tool_json, get_weather_func)

all_functions.append(get_weather)

get_current_time_tool_json = {"type": "function",
            "function": {
                "description": "获取当前时间",
                "name": "get_current_time",
                "parameters": {
                    "type": "",
                    "properties": {},
                    "required": []
                }
            }}

def get_current_time_func(args):
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

get_current_time = Function(get_current_time_tool_json, get_current_time_func)

all_functions.append(get_current_time)

def launch_exe(exe_path):
    if not os.path.exists(exe_path):
        return "未找到软件：" + exe_path
    try:
        subprocess.Popen([exe_path])
        return "成功打开软件：" + exe_path
    except subprocess.CalledProcessError as e:
        return "运行出现错误"

open_qatar_tool_json = {"type": "function",
            "function": {
                "description": "打开Qatar软件",
                "name": "open_qatar",
                "parameters": {
                    "type": "",
                    "properties": {},
                    "required": []
                }
            }}
def open_qatar_func(args):
    qatar_path = "D:\\Qatar\\Debug\\QaTar.exe"
    return launch_exe(qatar_path)
# 打开Qatar软件
open_qatar = Function(open_qatar_tool_json, open_qatar_func)

all_functions.append(open_qatar)

open_dingding_tool_json = {"type": "function",
            "function": {
                "description": "打开钉钉",
                "name": "open_dingding",
                "parameters": {
                    "type": "",
                    "properties": {},
                    "required": []
                }
            }}
def open_dingding_func(args):
    dingding_path = "D:\\Software\\DingDing\\DingtalkLauncher.exe"
    return launch_exe(dingding_path)
# 打开钉钉
open_dingding = Function(open_dingding_tool_json, open_dingding_func)

all_functions.append(open_dingding)

import platform


# 获取文件夹下的文件列表
get_folder_files_tool_json = {
    "type": "function",
    "function": {
        "description": "获取指定文件夹下的所有文件和子文件夹列表",
        "name": "get_folder_files",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "要获取文件列表的文件夹路径"
                }
            },
            "required": ["folder_path"]
        }
    }
}


def get_folder_files_func(args) -> str:
    folder_path = args["folder_path"]
    try:
        if not os.path.exists(folder_path):
            return json.dumps({"status": "error", "message": "文件夹路径不存在"})

        if not os.path.isdir(folder_path):
            return json.dumps({"status": "error", "message": "提供的路径不是文件夹"})

        files = os.listdir(folder_path)
        return json.dumps({
            "status": "success",
            "folder_path": folder_path,
            "files": files
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


get_folder_files = Function(get_folder_files_tool_json, get_folder_files_func)
all_functions.append(get_folder_files)

# 打开文件
open_file_tool_json = {
    "type": "function",
    "function": {
        "description": "打开指定路径的文件",
        "name": "open_file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "要打开的文件的完整路径"
                }
            },
            "required": ["file_path"]
        }
    }
}


def open_file_func(args) -> str:
    file_path = args["file_path"]
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{file_path}'")
        else:  # Linux
            os.system(f"xdg-open '{file_path}'")
        return json.dumps({"status": "success", "message": f"已打开文件: {file_path}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


open_file = Function(open_file_tool_json, open_file_func)

all_functions.append(open_file)

# 获取文件详细信息
get_file_info_tool_json = {
    "type": "function",
    "function": {
        "description": "获取文件的详细信息",
        "name": "get_file_info",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "要获取信息的文件的完整路径"
                }
            },
            "required": ["file_path"]
        }
    }
}


def get_file_info_func(args) -> str:
    file_path = args["file_path"]
    try:
        stat_info = os.stat(file_path)
        file_info = {
            "file_path": file_path,
            "size": stat_info.st_size,  # 文件大小（字节）
            "last_modified": datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "last_accessed": datetime.fromtimestamp(stat_info.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
            "creation_time": datetime.fromtimestamp(stat_info.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "is_file": os.path.isfile(file_path),
            "is_directory": os.path.isdir(file_path)
        }
        return json.dumps(file_info)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


get_file_info = Function(get_file_info_tool_json, get_file_info_func)

all_functions.append(get_file_info)

functions_map = {
}



tool_json_list = [
]

for function in all_functions:
    func_name = function.tool_json["function"]["name"]
    functions_map[func_name] = function
    tool_json_list.append(function.tool_json)

