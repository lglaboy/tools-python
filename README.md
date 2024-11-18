# 打包
```shell
# 创建虚拟环境
python -m venv .venv
# 进入虚拟环境
source .venv/bin/activate
# 安装build
pip install build
# 打包
python -m build

# build后会生成一个dist目录，里面存在whl和tar.gz文件
```

# 部署
```shell
# 可以创建一个虚拟环境
python3 -m venv .venv

# 进入虚拟环境
. .venv/bin/activate

# 安装whl文件
pip install dist/tools-0.1.0-py3-none-any.whl
```

# 安装
```shell
# 安装whl文件
pip install dist/tools-0.1.0-py3-none-any.whl

# 运行命令，若没有配置文件，首次执行，自动根据模板创建，位于 ~/.tools_config
# (test-cli-venv) $ tools -h
# /home/whoami/.tools_config not exist, 已基于模板创建，请修改内容。
```

## 自动补全

将生成的脚本写入文件，通过加载文件实现

bash 环境

```shell
# 1.将脚本保存在某处
_TOOLS_COMPLETE=bash_source tools > ~/.tools-complete.bash
# 2.在~/.bashrc中获取文件，添加
. ~/.tools-complete.bash
```

# 配置
## 用户配置文件
Linux: ~/.tools_config

Windows: ~\.tools_config

MacOS: ~/.tools_config

## 配置示例
```yaml
h3c:
  # 访问地址
  address: https://192.168.x.x:8443
  # 加密后的认证信息
  flag: xxxxxxxxxxxxxxxxxxxxxxx
```

## 环境变量

| 环境变量        | 说明           | 示例                       |
|-------------|--------------|--------------------------|
| h3c_address | h3c防火墙地址     | https://192.168.x.x:8443 |
| h3c_flag    | 登录认证信息(加密后的） | xxxxxxxxxxxxxxxxxxxxxxx  |

设置环境变量

Windows（Powershell）:
```
# 设置环境变量
$env:h3c_address="https://192.168.x.x:8443"
# 查看
$env:h3c_address
# 取消
$env:h3c_address=""
```

Linux:
```shell
# 设置环境变量
export h3c_address="https://192.168.x.x:8443"

# 取消
unset h3c_address
```
## 优先级

环境变量 > 用户配置文件 -> 默认配置

# 功能说明

## h3c
针对 H3C 防火墙 H3C SecPath F100-S-G3 开发的管理命令



## grafana

# 示例

查看帮助

```
(test-cli-venv) $ tools -h
Usage: tools [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  h3c
  show  查看配置信息
```

查看h3c用户

```
(test-cli-venv) $ tools h3c get user
+-----------------------------+-----+-----------+-------+-------+-------+-----------+--------+-------+--------+
|             Name            | UID | GroupName | ADVPN |  IKE  |  IPoE | LanAccess | Portal |  PPP  | SSLVPN |
+-----------------------------+-----+-----------+-------+-------+-------+-----------+--------+-------+--------+
|         xxxxxxxx0011        | 120 |   system  | false | false | false |   false   | false  | false |  true  |
|             xxx             |  4  |   system  | false | false | false |   false   | false  | false |  true  |
```
