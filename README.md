# AWS PoC

A script to list the aws accounts

## Requirements
* A python environment with all libraries installed defined in [requirements.txt](./requirements.txt)
* An AWS Organization
* A group or user with the policy [AWSOrganizationsReadOnlyAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSOrganizationsReadOnlyAccess.html) configured

## Features

* By default list all AWS Organizations
* `--list-all-sso-accounts SSO-PROFILE` Listing all sso accounts for SSO-PRIFLE given
* `--list-local-profiles` Listing all local profiles configured on `~/.aws/config` file
* `--validate-sso` Validating all local profiles upon the AWS Organizations accounts
* `--list-credentials` Listing all credentials secrets

