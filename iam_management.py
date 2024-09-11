# Created by:- Wasim

# Importing required modules
import boto3
import random
import string


# loging to aws console to IAM user console
aws_console = boto3.session.Session(profile_name = "default")
iam_console = aws_console.client("iam")


# generating random password
def random_password(length):
    # length = int(input("Enter the length: "))
    chars = string.ascii_letters
    chars += string.digits
    chars += string.punctuation

    return "".join([random.choice(chars) for i in range(length)])


def create_iam_user(user_name, pwd):
    try:
      
      # creating user
       response = iam_console.create_user(
           UserName= user_name,    
       )

      # creating loging profile aka: password
       login_create = iam_console.create_login_profile(
            UserName=user_name,
            Password=pwd,
            PasswordResetRequired=True, #Forcing to change password when loging for first time
        )
       

       user = response['User']

      # printing needed outputs
       print("User have been Created! \n")
       print("UserName:- " , user['UserName'])
       print("UserId:- ", user['UserId'])
       print("Password is:- ", pwd)  #this will print the password as well but don't use it for security 
       print("UserARN:- ", user['Arn'])

    except iam_console.exceptions.EntityAlreadyExistsException:
       print(f"user {user_name} already exists")

    except Exception as e:
       print(f"Error creating user: {e}")


# creating policy [So new user can loging and change password]
def create_policy(policy_name, policy_document):
    try:   

        create_policy = iam_console.create_policy(
            PolicyName = policy_name,
            PolicyDocument = policy_document,
        )

        arn = create_policy['Policy']

        print("Policy arn:- ", arn['Arn'])

    except Exception as e:
        print(f"Error creating policy: {e}")


# Attaching the policy we created to user 
def attach_policy(user_name, policy_arns):
    
    # loolping because in this script we attaching 2 policies
    for policy_arns in policy_arns:
    
      try: 

          attach_policy = iam_console.attach_user_policy(
              UserName=user_name,
              PolicyArn=policy_arns,
              
          )
      except Exception as e:
          print(f"Error creating policy: {e}")




def delete_user(user_name, policy_arns):
# Detach policies from the user
    for policy_arn in policy_arns:

        try:
            iam_console.detach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn,
            )

            print(f"Successfully detached policy for User {user_name}")

        except iam_console.exceptions.NoSuchEntityException: 
            print(f"Error: Policy {policy_arns} or user {user_name} does not exist.")
        
        except Exception as e:
            print("An unexpected error ocure while detaching policy")

# Delete the user login profile
    try:

        iam_console.delete_login_profile(
            UserName= user_name,
        )

        print(f"Successfully deleted login profile for user {user_name}.")

    except iam_console.exceptions.NoSuchEntityException:
        print(f"Error: No login profile exists for user {user_name}.")

    except Exception as e:
        print("An unexpected error ocure while deleting loging profile")

# Delete the user
    try:

        iam_console.delete_user(
            UserName=user_name,
        )

        print(f"Successfully deleted user {user_name}.")

    except iam_console.exceptions.NoSuchEntityException:
        print(f"Error: User {user_name} does not exist.")
    
    except Exception as e:
        print(f"An unexpected error occurred while deleting the user: {e}")

# listing all the iam user
def list_user():
    try:
        response = iam_console.list_users()

        for users in response['Users']:
            print(users['UserName'])

    except Exception as e:
        print("An unexpected error occurred while printing User List")


# the policy name 
policy_name = 'IAMUserManagementPolicy'

# policy json code
policy_document = '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:CreateUser",
        "iam:CreateLoginProfile",
        "iam:ChangePassword"
      ],
      "Resource": "*"
    }
  ]
}'''

# asking user what they wanna do
action = input("List, Create, Delete? ").lower()

# use the policy maker only for one time after once policy is created just ATTACH it with any user using ARN mention down
# if u make this everytime will show error [comment it out] 

# policy_arn = create_policy(policy_name, policy_document)

# for IAMUserManagementPolicy don't create everytime use as shown down after created once 
# 2 polies 2nd one provieds full access to EC2 instance
policy_arns = [ # multiple policies
    'arn:aws:iam::864981749658:policy/IAMUserManagementPolicy', # This is the policy we creating above use this everytime after created once
    'arn:aws:iam::aws:policy/AmazonEC2FullAccess', #{EC2 Instance permission}  A policy which exist in aws [just attaching it]
]

if action == "list":
    list_user()

elif action == "create":
    length = int(input("Enter the length: "))
    pwd = random_password(length)
    user_name = input("Enter User Name: ")
    create_iam_user(user_name, pwd)
    attach_policy(user_name, policy_arns)

elif action == "delete":
    user_name = input("Enter User Name: ")
    delete_user(user_name, policy_arns)

else:
    print("Invalid Option!")
