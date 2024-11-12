import os
from tools.config.manager import ConfigManager

# 服务配置项示例，完整配置位于config/base.yml,转换为变量
# 记录变量
h3c_address = ""
h3c_flag = ""


def set_constant(name, value):
    # 环境变量优先级高
    env_value = os.getenv(name)
    if env_value:
        value = env_value

    globals()[name] = value


# 自定义变量规则
def load_config_to_vars(conf, parent_key=""):
    for key, value in conf.items():
        # 创建新的变量名
        variable_name = f"{parent_key}_{key}" if parent_key else key

        if isinstance(value, dict):
            # 如果值是字典，则递归调用
            load_config_to_vars(value, variable_name)
        elif isinstance(value, list):
            # 如果值是列表，直接赋值
            set_constant(variable_name, value)
        elif isinstance(value, int):
            # 如果是整型，转换为字符串
            set_constant(variable_name, str(value))
        else:
            # 其他类型，直接赋值
            set_constant(variable_name, value)


config = ConfigManager()

# 调用函数覆盖现有配置变量
load_config_to_vars(config.get_configuration())
