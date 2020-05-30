import boto3
import pandas as pd
import numpy as np
import datetime


file = input("enter file name:") #导入excel 表格，详见example2.xlsx
sheet = pd.read_excel(io=file)

# 将表格数据转换为python list
np_data = np.array(sheet)
data = np_data.tolist()

# 创建boto3 session，注意profile 和region 跟随项目更换
session = boto3.Session(profile_name='anli_admin', region_name='cn-northwest-1')
workspaces = session.client('workspaces')

result = []

for item in data:

    """
    boto3 提供的modify_workspace_properties 一次只能修改一个ws 的一个参数
    可修改的参数有
    "RunningMode": "AUTO_STOP"|"ALWAYS_ON",
    "RunningModeAutoStopTimeoutInMinutes": integer,
    "RootVolumeSizeGib": integer,
    "UserVolumeSizeGib": integer,
    "ComputeTypeName": "VALUE"|"STANDARD"|"PERFORMANCE"|"POWER"|"GRAPHICS"|"POWERPRO"|"GRAPHICSPRO"
    """
    try:
        response = workspaces.modify_workspace_properties(
            WorkspaceId=item[0],
            WorkspaceProperties={
                'RunningMode':item[1]
            }
        )
        # 读取response 返回值，200 为成功，400 为失败，可通过下面创建的表格判断对哪些ws 的操作失败了
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            result.append([item[0], item[1], 'successful'])
        else:
            result.append([item[0], item[1], 'failed'])
    except Exception as e:
        print(e)

print(result)

# 将response 返回结果保存进一个新的表格，表格会在脚本所在目录创建，文件名为创建时间，可以通过表格确认所有修改返回值均标识成功
result_data = pd.DataFrame(result)

w = pd.ExcelWriter('./{}.xlsx'.format((datetime.datetime.isoformat(datetime.datetime.today()).split('.')[0]).replace(':','-')))
result_data.to_excel(w)
w.save()