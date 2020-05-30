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
    try:
        response = workspaces.terminate_workspaces(
            TerminateWorkspaceRequests=[
                {
                    'WorkspaceId': item[0]
                },
            ]
        )
        if response:
            result.append([response['FailedRequests'][0]['WorkspaceId'], response['FailedRequests'][0]['ErrorCode'], 
            response['FailedRequests'][0]['ErrorMessage']])
    except Exception as e:
        print(e)

print(result)

if length(result) > 0:
    result_data = pd.DataFrame(result)
    w = pd.ExcelWriter('./{}.xlsx'.format((datetime.datetime.isoformat(datetime.datetime.today()).split('.')[0]).replace(':','-')))
    result_data.to_excel(w)
    w.save()
else:
    break