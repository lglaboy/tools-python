import os
import yaml
import shutil

# 系统配置项
config_name = ".tools_config"


# 转换yaml配置格式
def config_to_custom(conf, parent_key="") -> dict:
    ret = {}
    for key, value in conf.items():
        # 创建新的变量名
        variable_name = f"{parent_key}_{key}" if parent_key else key

        if isinstance(value, dict):
            # 如果值是字典，则递归调用
            ret.update(config_to_custom(value, variable_name))
        elif isinstance(value, list):
            # 如果值是列表，直接赋值
            ret[variable_name] = value
        elif isinstance(value, int):
            # 如果是整型，转换为字符串
            ret[variable_name] = str(value)
        else:
            # 其他类型，直接赋值
            ret[variable_name] = value
    return ret


class ConfigManager(object):
    def __init__(self, conf_file=None):
        self._conf_file = conf_file
        self._base_conf_file = "%s/base.yml" % os.path.dirname(__file__)

        if self._conf_file is None:
            home_dir = os.path.expanduser("~")
            self._config_file = os.path.join(home_dir, config_name)

    def get_base_configuration_definitions_raw(self) -> dict:
        ret = {}
        if os.path.isfile(self._base_conf_file):
            with open(self._base_conf_file, "r") as f:
                ret = yaml.safe_load(f)
        return ret

    def get_base_configuration_definitions(self) -> dict:
        return config_to_custom(self.get_base_configuration_definitions_raw())

    # 返回配置项
    # 1.如果用户家目录存在配置文件，首先解析
    # 2.如果存在环境变量，则覆盖配置文件中定义的内容
    # 3.命令行参数优先级最高
    def get_configuration_definitions_raw(self) -> dict:
        """
        返回用户配置原始数据(yaml_to_dict)
        :return:
        """
        ret = {}
        if os.path.isfile(self._config_file):
            with open(self._config_file, "r") as f:
                ret = yaml.safe_load(f)
        else:
            shutil.copyfile(self._base_conf_file, self._config_file)
            print(self._config_file, "not exist,", "已基于模板创建，请修改内容。")
            exit(1)
        return ret

    def get_configuration_definitions(self) -> dict:
        """
        获取用户自定义配置项
        :return:
        """
        return config_to_custom(self.get_configuration_definitions_raw())

    def get_configuration(self) -> dict:
        """
        获取调整格式后的配置项
        :return:
        """
        ret = self.get_base_configuration_definitions()
        user_config = self.get_configuration_definitions()

        for key, value in user_config.items():
            if key in ret:
                ret[key] = value
        return ret

    # 获取配置项名称列表
    def get_base_configuration_names(self) -> list:
        ret = []
        conf = self.get_base_configuration_definitions()
        for key in conf:
            ret.append(key)
        return ret
