import json
from openai import OpenAI

from functions import functions_map, tool_json_list
messages_g = []
isFirst = True
client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-a90528958d5d4abb8621ef0886f85f7f",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
def request():
    # print("messages_g:", messages_g)
    if len(messages_g) < 1:
        print("message is empty")
        return

    # 打印请求体
    # print("\n=== 请求体 ===")
    # request_body = {
    #     "model": "qwen-plus",
    #     "messages": messages_g,
    #     "tools": tool_json_list
    # }
    # print(json.dumps(request_body, indent=2, ensure_ascii=False))
    # print("=============\n")

    completion = client.chat.completions.create(
        model="qwen-plus",
        # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages_g,
        tools=tool_json_list,
    )

    print("输入token：",completion.usage.prompt_tokens)
    print("输出token：",completion.usage.completion_tokens)
    reply = json.loads(completion.model_dump_json())
    msg = reply['choices'][0]['message']
    if msg["tool_calls"]:
        for call in msg["tool_calls"]:
            args = json.loads(call["function"]["arguments"])
            funcName = call["function"]["name"]
            print("调用函数：", funcName)
            messages_g.append(buildMessage("", "assistant", msg["tool_calls"]))
            toolMsg = buildMessage(functions_map[funcName].execute(args), "tool", None, funcName, call["id"])
            messages_g.append(toolMsg)
            msg = request()
    return msg

def buildMessage(message, msgType, toolCalls=None, name='', toolId=0):
    if msgType == "system":
        return {"role": "system", "content": message}
    elif msgType == "user":
        return {"role": "user", "content": message}
    elif msgType == "assistant":
        if toolCalls:
            return {"role": "assistant", "content": message, "tool_calls": toolCalls}
        return {"role": "assistant", "content": message}
    elif msgType == "tool":
        return {"role": "tool", "content": message, "name": name, "id": toolId}
    else:
        return None

if __name__ == "__main__":
    messages_g.append(buildMessage("你是一个精简的AI，用尽可能简短的话回答", "system"))
    print("请询问AI：")
    while True:
        # 用户输入
        input_msg = input()
        if "exit" == input_msg:
            break
        messages_g.append(buildMessage(input_msg, "user"))
        reply_msg = request()
        messages_g.append(buildMessage(reply_msg["content"], "assistant"))
        print(reply_msg["content"])




