import boto3
import pandas as pd

class AWSAccounts:
    def __init__(self, profile_name: str):
        try:
            self.session = boto3.Session(profile_name=profile_name)
        except Exception as e:
            print(f'ERROR!!: Something unexpected happend. More information bellow:\n'
                  f'{e}\n'
                  f'Please check your permissions'
                  )
    def get_organization_accouonts(self):
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
