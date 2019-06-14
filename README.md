# Web-Based Password Manager


Simple web-based password manager. Share passwords with your friends

## Tasks
1. Store passwords in a database
    - Site name
    - Site URL
    - Login account name
    - Login password (stored securely)
    
2. User Interface
    - List all entries
    - Add & Delete entries
    - Click an entry to view & update details
    - Click a link in details to open a site in a new window 

3. Ok to cut corners on login/accounts/UI/etc
    - e.g. you could just use a single hardcoded account for all actions
    
4. Password entry has a button to generate a link. The link can be copied and sent in the email. The link is active for 5 minutes
    
### Help in the implementation of the task

* [Django] - http://docs.python-guide.org/en/latest/writing/style/
* [Django-bootstrap4] - https://django-bootstrap.readthedocs.io/en/latest/
* [Django-tables2] - https://django-tables2.readthedocs.io/en/latest/
* [Django-filter] - https://django-filter.readthedocs.io/en/master/
* [PostgreSQL] - https://www.postgresql.org/docs/

### Installation
The installation is done by running the script. Before running the script, you must have PostgreSQL database installed.

##### Script

 1. Open the terminal and then enter the following command:
 2. Go to the directory with the downloaded files by typing:
```sh
$ sh install.sh
```
#### That's all!

