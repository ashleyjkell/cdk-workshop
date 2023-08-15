# Github Workflow with CDK

In this series of exercises we'll create, update, and improve a Github workflow that builds and deploys a CDK stack using an AWS role we'll create.

Each exercise has a simple set of objectives that you can solve in your own way or you can follow the instructions that will guide you through the process. As we get deeper into the exercises the instructions will rely on previous instructions and using that knowledge to proceed. If you get stuck, check the previous exercise or as always; ask for help.

The final exercise is a bonus one and has no instructions at all! You'll need to use everything you've learnt to that point and some of your own research to find the solution.

Remember when creating resources in AWS to add your own name or some other unique identifier to avoid conflicts.

***

## Exercise 0 - Set up GitHub Repository

### Objectives

- Create new GitHub repo for CDK project

### Instructions:

1. Sign into your GitHub account
2. Click the + button and select "New repository"
3. Give the repo a name like "CDK-Workshop", make it Public, and click Create repository
4. Open your terminal and navigate to where you want the local copy of the repo to be
5. Clone the repo with:  `git clone https://github.com/<your-username>/CDK-Workshop.git`
6. Cd into the local repo:  `cd CDK-Workshop`

***

## Exercise 1 - Setup AWS Permissions and Credentials

### Objectives

- Create IAM role for CDK deployment
- Generate access keys
- Save keys as GitHub secrets

### Instructions

1. Sign into the AWS console and go to the IAM service
2. Click "Users" and then "Create user"
3. Click Next
4. Attach the following permissions:
     - AmazonS3FullAccess
     - CloudformationFullAccess
     - IAMFullAccess
     - AmazonSSMReadOnlyAccess
5. Give the User a name like "GitHubCDKDeployUser" and create the User
6. After creating the user, select it and go to the Security Credentials tab
7. Click "Create access key", select CLI, accept the creation and click Next
8. Copy the Access key ID and Secret
9. In your GitHub repo, go to Settings, Secrets and Variables and click Actions
10. Create a new repository secret called `AWS_ACCESS_KEY`
11. Paste in the access key ID value and save
12. Create another repository secret called `AWS_SECRET_KEY`
13. Paste in the secret access key value and save

***

## Exercise 2 - Create CDK Stack & Starter Workflow

### Objectives

- Create CDK app with S3 bucket
- Create a Github workflow
- Use Actions to do the following:
  - Install Python and CDK requirements
  - Setup AWS credentials
- Add a synth step to check your code and credentials work

### Instructions

1. In your local repo, create a new directory called  `cdk-app`
2. In  `cdk-app`  initialize a new Python CDK app by running the usual:

```sh
 cdk init app --language python
 source .venv/bin/activate
 pip install -r requirements.txt
```

3. Replace the entire code in `cdk-app/cdk-app_stack.py` with:

```python
from aws_cdk import (
Stack, 
aws_s3 as s3  
)

class CdkAppStack(Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        s3.Bucket(
        self, 
        "MyBucket",
        versioned=True
        )
```

4. Save the file.
5. Do a quick check the code works by using:  `cdk synth`
6. If everything is ok commit the code:
  `git add .`
  `git commit -m "Create CDK app"`
7. Create the necessary folders and new file at path `.github/workflows/pipeline.yml`.
8. Add the following YAML contents to it to define a workflow:

```yaml
name: CDK Workshop
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Install CDK CLI
      run: |
        npm install -g aws-cdk

    - name: Set up Python 3.9
      uses: actions/setup-python@v4
      with: 
        python-version: '3.9'

    - name: Install Python dependencies
      working-directory: cdk-app
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install aws-cdk-lib

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
        aws-region: "eu-north-1"

    - name: CDK Synth
      working-directory: cdk-app
      run: cdk synth
```

9. Commit the workflow file:
  `git add .`
  `git commit -m "Add workflow"`

10. Push the code changes to GitHub: `git push`

11. In GitHub, go to the Actions tab, your pipeline should be running automatically.
12. Check the logs for any errors or outputs

***

## Exercise 3 - Update Workflow with a Diff

### Objectives

- Make some changes to the CDK stack
- Update initial pipeline to add a diff step to see changes from previous version

### Instructions:

1. Add a `cdk diff` step to your `build` job
2. Commit and push your code
3. Check the run log for your workflow for any errors and to see your diff

***

## Exercise 4 - Implement Deployment

### Objectives

- Update pipeline to deploy CDK stack
- Install Python and setup AWS again
- Restrict deployments to only occur when approved

### Instructions:
1. Add a `deploy` job to your workflow
2. Make the `deploy` job require the `build` job to be completed first
3. You'll need to install CDK, Python, requirements, and configure your AWS credentials again.
4. Commit and push your code
5. Check workflow logs for any errors
6. Check AWS to see if your changes were successful.

***

## Exercise 5 (Extra) - Tidy Up

### Objectives

- Get `build` and `deploy` to use same code to setup python and configure AWS credentials
- Remove unnecessary duplication by using cache action
- Cache the pip modules folder
- Cache the aws-credentials file

### Instructions:

You're on your own, good luck!
