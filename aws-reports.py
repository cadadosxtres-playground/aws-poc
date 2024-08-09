import boto3
import argparse
import pandas as pd
from aws_accounts.aws_accounts import AWSAccounts


def arguments() -> object:
    parser = argparse.ArgumentParser(description='A helper script to gather information from AWS aws_accounts')

    parser.add_argument('-p', '--profile', type=str, default='default', help='Provide an aws-cli profile')

    args = parser.parse_args()
    return args



def main():

    args = arguments()
    try:
        if args.profile:
            # Get the list of aws_accounts
            accounts = AWSAccounts(profile_name=args.profile).get_organization_accouonts()

            if accounts is None:
                raise Exception(f'ERROR!!! getting list of aws aws_accounts')
            # Print account details
            print(accounts)
    except Exception as e:
        print(f'{e}')

if __name__ == "__main__":
    main()
