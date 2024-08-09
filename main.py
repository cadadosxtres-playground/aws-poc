import boto3
import argparse

def list_aws_accounts(profile_name: str) -> list:
    # Create a boto3 session using the specified AWS SSO profile
    session = boto3.Session(profile_name=profile_name)

    try:
        # Create a client for the AWS Organizations service
        client = session.client('organizations')

        # Initialize a list to store account information
        accounts = []

        # Paginate through the list_accounts API to retrieve all accounts
        paginator = client.get_paginator('list_accounts')
        for page in paginator.paginate():
            for account in page['Accounts']:
                accounts.append({
                    'AccountId': account['Id'],
                    'AccountName': account['Name']
                })

        return accounts
    except Exception as e:
        print(f'ERROR!!: Something unexpected happend. More information bellow:\n'
              f'{e}\n'
              f'Please check your permissions'
              )

def arguments() -> object:
    parser = argparse.ArgumentParser(description='A helper script to gather information from AWS accounts')

    parser.add_argument('-p', '--profile', type=str, default='default', help='Provide an aws-cli profile')

    args = parser.parse_args()
    return args



def main():

    args = arguments()
    try:
        if args.profile:
            # Get the list of accounts
            accounts = list_aws_accounts(profile_name=args.profile)

            if accounts is None:
                raise Exception(f'ERROR!!! getting list of aws accounts')
            # Print account details
            print(f'Account ID, Account Name')
            for account in accounts:
                print(f"{account['AccountId']}, {account['AccountName']}")
    except Exception as e:
        print(f'{e}')

if __name__ == "__main__":
    main()
