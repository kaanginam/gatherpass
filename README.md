# gatherpass
//{
        //    "site": "pastebin.com",
        //    "dl": "raw/"
        //},



## TODO
- password heuristic: how big password list? determine how accurate it is in every leak I have, test until each leak is flagged
- forum gathering: replies + subsequent leak gathering
- word splitting
- 
```sh
az webapp config storage-account add \
--resource-group <resource-group> \
--name <function-app-name> \
--custom-id az-files-001 \
--storage-type AzureFiles \
--account-name <storage-account-name> \
--share-name <file-share-name> \
--access-key <storage-account-access-key> \
--mount-path /fx-files
```