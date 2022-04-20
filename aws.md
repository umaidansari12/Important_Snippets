## AWS Commands

* ### Install AWS CLI
```
sudo apt-get update
sudo apt-get install awscli
```
* ### Check  versioning of AWS
`aws --version`

* ### Top check identity of user in AWS CLI
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