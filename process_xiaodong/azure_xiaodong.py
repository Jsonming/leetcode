#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/7 15:39
# @Author  : yangmingming
# @Site    : 
# @File    : azure.py
# @Software: PyCharm
import re
import datetime
from azure.storage.blob import generate_blob_sas

url = "https://datamallwangpan.blob.core.chinacloudapi.cn/mycontainer/blobname.txt?sv=2019-02-02&st=2020-07-09T06%3A29%3A35Z&se=2020-07-10T06%3A29%3A35Z&sr=b&sp=r&sig=mTDlSQggwNq79RVR1u9eMMGb6ftw5YuODNklSu8Mjms%3D"
url = "https://datamallwangpan.blob.core.chinacloudapi.cn/mycontainer/blobname.txt?sv=2019-02-02&st=2020-07-09T08%3A27%3A48Z&se=2020-07-10T08%3A27%3A48Z&sp=r&sr=b&sig=ZfuOdeR0wgSbeKrp2KQYv9f3l2raln%2BHDB5ALPqoQW0%3D"

class BlobSample(object):

    def auth_shared_blob_signature(self):
        account_name = "datamallwangpan"
        container_name = "mycontainer"
        blob_name = "blobname.txt"
        account_key = "kmz/CvWMaWq9jTG7M2nD8KOrzfc13Z7q4fJe6IygGF3e2JIdNjCu7a4FrsMyBtWr0g5lsM9CjEsjqsBRbSBetw=="
        account_key = "AccountName=datamallwangpan;AccountKey=kmz/CvWMaWq9jTG7M2nD8KOrzfc13Z7q4fJe6IygGF3e2JIdNjCu7a4FrsMyBtWr0g5lsM9CjEsjqsBRbSBetw==;EndpointSuffix=core.chinacloudapi.cn;DefaultEndpointsProtocol=https;"
        utctime_s = datetime.datetime.utcnow().isoformat().split(".")[0] + "Z"
        utctime_e = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        utctime_e = utctime_e.isoformat().split(".")[0] + "Z"

        sas_token = generate_blob_sas(
            account_name,  # type: str
            container_name,  # type: str
            blob_name,  # type: str
            snapshot=None,  # type: Optional[str]
            account_key=account_key,  # type: Optional[str]
            user_delegation_key=None,  # type: Optional[UserDelegationKey]
            permission='r',  # type: Optional[Union[BlobSasPermissions, str]]
            expiry=utctime_e,  # type: Optional[Union[datetime, str]]
            start=utctime_s,  # type: Optional[Union[datetime, str]]
            policy_id=None,  # type: Optional[str]
            ip=None,  # type: Optional[str]
        )
        base_url = "https://{}.blob.core.chinacloudapi.cn/{}/{}?{}".format(account_name, container_name, blob_name,
                                                                           sas_token)
        new_url = re.sub("sv=(.*?)&", "sv=2019-02-02&", base_url)
        print(new_url)


if __name__ == '__main__':
    sample = BlobSample()
    sample.auth_shared_blob_signature()
