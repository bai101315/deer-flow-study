from importlib import import_module

# 1. 先试试能不能导入模块
module = import_module("langchain_openai")
# 2. 再试试能不能拿到 ChatOpenAI
chat_openai_class = getattr(module, "ChatOpenAI")

print(chat_openai_class)  # 如果输出 <class 'langchain_openai.chat_models.ChatOpenAI'>，就说明成功了