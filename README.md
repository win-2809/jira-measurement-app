# Jira Dashboard
**Jira Dashboard** provides a solution that allows users follow the statistics of Jira over time not only in one sprint. **Jira Dashboard** pulls data via Jira API based on the information is provided by user and does not store or collect any user information.

## Installation
The scripts are written in python 3.7.9. So it's best to install this version or later one.

Run below command to install package dependencies:

```
$ pip install -r requirements.txt
```

## Usage
Run below command to open **Jira Dashboard**:

```
$ streamlit run main.py
```
Then, enter Jira information to show the statistics in **Jira Dashboard**:

- Username: enter your email on Jira (Example: example@example.com)
- Token: enter your token on Jira. If you don't have it yet, please follow [this documentation](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- Domain: enter your Jira domain
- Project key: enter your Jira project key