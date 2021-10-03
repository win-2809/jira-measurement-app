import pandas as pd
import numpy as np
import utils
import collections
import utils

def load_data(username, token, domain, projectKey):
    rawData = utils.getApiPagination(username, token, domain, projectKey)

    df = pd.DataFrame(columns=["id","key","summary","status","assignee","created","updated","issuetype","priority","creator","versions","labels","components"])

    issueList = rawData.get("issues")

    for issue in issueList:
        utils.replace_none(issue)
        issueInfo = {
                        "id": issue.get("id"), 
                        "key": issue.get("key"),
                        "summary": issue.get("fields").get("summary", None),
                        "status": issue.get("fields").get("status", None).get("name", None),
                        "assignee": issue.get("fields").get("assignee", None).get("displayName", None),
                        "created": issue.get("fields").get("created", None),
                        "updated": issue.get("fields").get("updated", None),
                        "issuetype": issue.get("fields").get("issuetype", None).get("name", None),
                        "priority": issue.get("fields").get("priority", None).get("name", None),
                        "creator": issue.get("fields").get("creator", None).get("displayName", None),
                        "versions": issue.get("fields").get("versions", None),
                        "labels": issue.get("fields").get("labels", None),
                        "components": issue.get("fields").get("components", None)
                    }
        df = df.append(issueInfo, ignore_index=True)
        
    return df