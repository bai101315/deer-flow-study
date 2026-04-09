# from importlib import import_module

# # 1. 先试试能不能导入模块
# module = import_module("langchain_openai")
# # 2. 再试试能不能拿到 ChatOpenAI
# chat_openai_class = getattr(module, "ChatOpenAI")

# print(chat_openai_class)  # 如果输出 <class 'langchain_openai.chat_models.ChatOpenAI'>，就说明成功了

storage_class_path = "deerflow.agents.memory.storage.FileMemoryStorage"
module_path, class_name = storage_class_path.rsplit(".", 1)
print(f"module_path: {module_path}, class_name: {class_name}")