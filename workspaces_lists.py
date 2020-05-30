import boto3
import pandas as pd
import datetime


session = boto3.Session(profile_name="anli_workspaces", region_name="cn-northwest-1") # profile_name 保存在默认.aws 目录中的配置
workspaces = session.client('workspaces')
anli_workspaces = workspaces.get_paginator('describe_workspaces') # # 单次请求上限是25 个用户，因此需要使用paginator 模块迭代读取所有资源
lists = []
directory_list = ['d-836732a930', 'd-836732452c', 'd-8367324646', 'd-836732584b'] # 多个目录直接添加目录id 到该列表
# directory_list = ['d-836732a930']
for directory in directory_list:
    anli_workspaces_pages = anli_workspaces.paginate(DirectoryId=directory) # 单次请求上限是25 个用户，因此需要使用paginator 模块迭代读取所有资源
    """
    请求返回值如下
{
   "NextToken": "string",
   "Workspaces": [ 
      { 
         "BundleId": "string",
         "ComputerName": "string",
         "DirectoryId": "string",
         "ErrorCode": "string",
         "ErrorMessage": "string",
         "IpAddress": "string",
         "ModificationStates": [ 
            { 
               "Resource": "string",
               "State": "string"
            }
         ],
         "RootVolumeEncryptionEnabled": boolean,
         "State": "string",
         "SubnetId": "string",
         "UserName": "string",
         "UserVolumeEncryptionEnabled": boolean,
         "VolumeEncryptionKey": "string",
         "WorkspaceId": "string",
         "WorkspaceProperties": { 
            "ComputeTypeName": "string",
            "RootVolumeSizeGib": number,
            "RunningMode": "string",
            "RunningModeAutoStopTimeoutInMinutes": number,
            "UserVolumeSizeGib": number
         }
      }
   ]
}
    """
    # 根据返回值添加需要的返回结果到一个列表，请按需进行
    for workspaces_pages in anli_workspaces_pages:
        for workspaces in workspaces_pages['Workspaces']:
            lists.append([workspaces['WorkspaceId'], workspaces['UserName'], workspaces['IpAddress'],workspaces['ComputerName'],
                        workspaces['State'],workspaces['WorkspaceProperties']['RunningMode'],workspaces['WorkspaceProperties']['ComputeTypeName']])

data = pd.DataFrame(lists)

print(data)

# 保存到一个表格到脚本所在文件夹，文件名为创建时的时间
w = pd.ExcelWriter('./{}.xlsx'.format((datetime.datetime.isoformat(datetime.datetime.today()).split('.')[0]).replace(':','-')))
data.to_excel(w)
w.save()

# 注意，在运行过程中可能会提醒IpAddress 不识别，目前看来是bug，等一会重试一般就能成功读取所有ws 了