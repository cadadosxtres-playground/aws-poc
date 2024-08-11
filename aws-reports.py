import boto3
import argparse
import pandas as pd
from aws_accounts.aws_accounts import AWSAccounts


def arguments() -> object:
    parser = argparse.ArgumentParser(description='A helper script to gather information from AWS aws_accounts')

    parser.add_argument('-p', '--profile', type=str,
                        default='aws-organizations-reader', help='Provide an aws-cli profile')

    ## Mutually excluded
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--user-profile', type=str, default='', help='A user profile to list all sso '
                                                                    'accounts related to the user profile')
    group.add_argument('--list-local-profiles', action='store_true',
                       help="Listing the local profiles configured\n"
                            "WARNING!! Please, be aware that you need to have configured "
                            "the aws-organizations-reader and at least a SSO profile")

    group.add_argument('--validate-sso', type=str,
                       help='Validate all sso user access upon organizations '
                            'sso and local profile. By default a USER SSO PROFILE NEEDS TO BE CONFIGURED')

    args = parser.parse_args()
    return args



def main():

    args = arguments()
    try:
        if args.profile:
            # Get the list of aws_accounts
            accounts = AWSAccounts(profile_name=args.profile).get_organization_accounts()

            if accounts is None:
                raise Exception(f'ERROR!!! getting list of aws aws_accounts')
        if args.user_profile:
            accounts = AWSAccounts(profile_name=args.profile).get_user_sso_accounts(user_profile_name=args.user_profile)
        if args.list_local_profiles:
            accounts = AWSAccounts(profile_name=args.profile).get_local_profiles()

        if args.validate_sso:
            accounts = AWSAccounts(profile_name=args.profile).validate_sso(user_sso_profile=args.validate_sso)

        # Print account details
        print(accounts)
    except Exception as e:
        print(f'{e}')

if __name__ == "__main__":
    main()
