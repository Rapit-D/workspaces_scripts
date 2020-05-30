该文档是在workspaces 运维过程中总结的几个脚本。
workspaces_lists.py 是为了抓取用户目前所有运行workspaces 的信息
modify_properties.py 是为了批量修改ws 的相关参数，例如，计费模式。

后续如果有更多需求，会继续更新在本项目中。

packages.txt 包含了运行脚本所需要的所有库，请通过`pip install -r packages.txt` 进行安装。

新增delete_workspaces.py 用来根据workspaceId来终止workspaces 用。

新增delete_example.xlsx 为delete_workspaces.py 所用文件的模板。

新增modify_example.xlsx 为modify_workspaces.py 所用文件的模板。