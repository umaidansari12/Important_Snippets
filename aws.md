
## AWS Commands

* ### Install AWS CLI
```
sudo apt-get update
sudo apt-get install awscli
```
* ### Check  versioning of AWS
`aws --version`

* ### To check identity of user in AWS CLI
`aws sts get-caller-identity`

* ### List users in AWS CLI
`aws iam list-users`

* ### To check credentials that are present in hidden ~/.aws directory

```
ls -la ~/
ls ~/.aws/
cd ~/.aws
ls
cat config
cat credentials
```

* ### Configure AWS 
```
aws configure
enter access key id
enter secret access key
enter region name
enter output format out of these 3 : json/text/table
```

* ### To check EC2 instances
`aws ec2 describe-instances`

* ### To list buckets
```
aws s3api list-buckets
OR
aws s3 ls
```

* ### To query a specific bucket

`aws s3 ls s3://<bucket_name>`

* ### To Copy files from bucket to local

```
aws s3 cp s3://<bucket_name>/<folder_name>/<file_name>.<extension> <download_folder>/<file_name>.<extension>
```

* ### To delete an object in an AWS S3 bucket

```
import boto3

s3 = boto3.resource('s3')
s3.Object('your-bucket', 'your-key').delete()

OR 

import boto3

client = boto3.client('s3')
client.delete_object(Bucket='mybucketname', Key='myfile.whatever')

OR 

from boto.s3.connection import S3Connection, Bucket, Key

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECERET_KEY)

b = Bucket(conn, S3_BUCKET_NAME)

k = Key(b)

k.key = 'images/my-images/'+filename

b.delete_key(k)

OR 

from django.conf import settings 
import boto3   
s3 = boto3.client('s3')
s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"media/{item.file.name}")
```

* ### AWS S3 Utilities

```
import os

import boto3
import botocore
from botocore.exceptions import ClientError

from app_config import AppConfig


class S3Utils:
    def __init__(self, config_file_path=None):
        if config_file_path:
            app_config = AppConfig.get_app_config(config_file_path)
        else:
            app_config = AppConfig.get_app_config()
        self.bucket_name = app_config.get_s3_bucket_name()
        access_key, secret_key, region_name = app_config.get_s3_credentials()
        self.set_env_vars(access_key, secret_key, region_name)
        self.s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)


    def set_env_vars(self, access_key, secret_key, region_name):
        '''
        required for docker setup
        '''
        os.environ['BOTO_CONFIG'] = '/dev/null'
        os.environ['AWS_ACCESS_KEY_ID'] = access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
        os.environ['AWS_DEFAULT_REGION'] = region_name

    def get_all_buckets(self):
        buckets = []
        for bucket in self.s3.buckets.all():
            buckets.append(bucket.name)
        return buckets

    def get_bucket_keys(self):
        '''
        every file is stored by a key in s3
        '''
        bucket = self.s3.Bucket(self.bucket_name)
        for bucket_object in bucket.objects.all():
            yield bucket_object.key

    def download_file(self, key, download_path):
        try:
            self.s3.Bucket(self.bucket_name).download_file(key, download_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise Exception(e)

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            return False
        return True

    def upload_file(self, file_path, key):
        """Upload a file to an S3 bucket

        :param file_path: File to upload
        :param bucket: Bucket to upload to
        :return: True if file was uploaded, else False
        """

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(file_path, self.bucket_name, key)
        except ClientError as e:
            raise Exception(f"S3 upload error for file : {file_path}")
        return True

    def get_download_link(self,object_key):
        # return f'https://{self.bucket_name}.s3.amazonaws.com/{object_key}'
        s3_client = boto3.client('s3')
        url_expiration_in_seconds = 604800
        url = s3_client.generate_presigned_url(ClientMethod='get_object',
                                                    Params={'Bucket': self.bucket_name,
                                                            'Key': object_key},
                                                    ExpiresIn=url_expiration_in_seconds)
        return url


if __name__ == '__main__':
    s3_util = S3Utils(config_file_path="/home/umaid/Vahan_Codes/Data-Engineering/staffing/conf/default.config")
    #s3_util.upload_file("/home/rishav/repo/vahan/Data-Engineering/staffing/conf/test.json", "test")
    #s3_util.download_file("test", "test.json")
    # s3_util.upload_file("/home/umaid/Downloads/shadowfax3pl_daily_login_2022-04-12_0503.csv","de/test/daily_login/2022-04-12_0503.csv")
    # s3_util.download_file("de/test/daily_login/2022-04-12_0503.csv","shadowfax3pl_daily_login_2022-04-12_0504.csv")
    # s3 = boto3.resource('s3')
    # s3.Object('vahan-staffing','de/test/order_base/2022-03-29_0943.csv').delete()

    for file in s3_util.get_bucket_keys():
        print(file)
        print(s3_util.get_download_link(file))


```