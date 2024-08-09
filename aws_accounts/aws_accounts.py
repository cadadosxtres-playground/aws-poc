import configparser

import boto3
import pandas as pd
import os
import json

class AWSAccounts:
    def __init__(self, profile_name: str):
        self.session = boto3.Session(profile_name=profile_name)

    # TODO creatinga a method to parse local config and return a list of dict with keys AccountId, ProfileName
    # TODO refactoring the validate sso method to validate upon the method that parses the config file

    def validate_sso(self, user_sso_profile: str) -> pd.DataFrame:
        org_accounts = self.get_organization_accounts()
        user_sso_accounts = list(self.get_user_sso_accounts(user_profile_name=user_sso_profile)['accountId'])
        if not user_sso_accounts:
            raise Exception(f'ERROR!!: Unexpected error happened with profile {user_sso_profile}. '
                      f'Please, check out that you have the SSO profile {user_sso_profile} correctly configured\n'
                      f'More information\n'
                      f'{e}')
        user_local_profiles = [ profile['AccountId'] for profile in self.get_sso_profiles()]

        ### Adding new two columns based on the user sso accounts and local profiles
        has_user_access = []
        has_user_local_profile = []
        for index, row in org_accounts.iterrows():
            if row['AccountId'] in user_sso_accounts:
                has_user_access.append(True)
            else:
                has_user_access.append(False)

            if row['AccountId'] in user_local_profiles:
                has_user_local_profile.append(True)
            else:
                has_user_local_profile.append(False)

        org_accounts['has_user_access'] = has_user_access
        org_accounts['has_user_local_profile'] = has_user_local_profile

        return org_accounts

    def get_local_profiles(self) -> list:
        session = boto3.Session()
        return session.available_profiles


    def get_sso_profiles(self, sso_config_path: str = '~/.aws/config') -> list:
        aws_config_path = os.path.expanduser(sso_config_path)
        if not os.path.expanduser(aws_config_path):
            raise Exception(f"ERROR!! configuration file {sso_config_path} doesn't exist")

        config = configparser.ConfigParser()
        config.read(aws_config_path)
        result = []

        for section in config.sections():
            profile = {}
            if section.startswith('profile'):
                profile['AccountName'] = section.split()[1]
            if 'sso_session' in config[section]:
                profile['AccountId'] = config[section].get('sso_account_id','Unknown')
                profile['RoleName'] = config[section].get('sso_role_name', 'Unknown')
                profile['Region'] = config[section].get('sso_region', 'Unknown')
                profile['SSOUrl'] = config[section].get('sso_start_url', 'Unknown')
                result.append(profile)

        return result

    def get_organization_accounts(self):
        try:
            # Create a client for the AWS Organizations service
            client = self.session.client('organizations')

            # Initialize a list to store account information
            accounts = []

            # Paginate through the list_accounts API to retrieve all aws_accounts
            paginator = client.get_paginator('list_accounts')
            for page in paginator.paginate():
                for account in page['Accounts']:
                    accounts.append({
                        'AccountId': account['Id'],
                        'AccountName': account['Name']
                    })

            df = pd.DataFrame.from_records(accounts)

            return df
        except Exception as e:
            print(f'ERROR!!: Something unexpected happend. More information bellow:\n'
                  f'{e}\n'
                  f'Please check your permissions'
                  )

    def get_user_sso_accounts(self, user_profile_name: str) -> pd.DataFrame:
        session = boto3.Session(profile_name=user_profile_name)
        client = session.client('sso')
        accessToken = self.__get_accesstoken()
        paginator = client.get_paginator('list_accounts')
        accounts = [page for page in paginator.paginate(accessToken=accessToken)]

        df = pd.DataFrame().from_records(accounts[0]['accountList'])
        return df

    def __get_accesstoken(self) -> str:
        cache_dir = os.path.expanduser('~/.aws/sso/cache')

        json_files = [json_file for json_file in os.listdir(cache_dir) if json_file.endswith('.json')]

        for file in json_files:
            file_path = '/'.join([cache_dir,file])
            with open(file_path) as file:
                data = json.load(file)
                if 'accessToken' in data:
                    return data['accessToken']