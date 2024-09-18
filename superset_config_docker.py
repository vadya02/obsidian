#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This is an example "local" configuration file. In order to set/override config
# options that ONLY apply to your local environment, simply copy/rename this file
# to docker/pythonpath/superset_config_docker.py
# It ends up being imported by docker/superset_config.py which is loaded by
# superset/config.py
#
from celery.schedules import crontab
from superset.tasks.types import ExecutorType
from flask_appbuilder.security.manager import AUTH_LDAP

WTF_CSRF_ENABLED = False
ROW_LIMIT = 5000
SECRET_KEY='rMSlEsn8VV/zJt7+F8GThjxfz9WEYO69AOym92imrRCbgdYMCb16iCjp'

SMTP_HOST = "172.16.57.70"
SMTP_PORT = 25
SMTP_STARTTLS = True
SMTP_SSL_SERVER_AUTH = False
SMTP_SSL = False
SMTP_USER = ""
SMTP_PASSWORD = ""
SMTP_MAIL_FROM = "superset@enplus.digital"
EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset] "

#Internal address 
WEBDRIVER_BASEURL = "http://localhost:8088/"
#External address
WEBDRIVER_BASEURL_USER_FRIENDLY = "http://localhost:8088/"
THUMBNAIL_SELENIUM_USER = "admin"
ALERT_REPORTS_EXECUTE_AS = [ExecutorType.SELENIUM]



# AUTH_TYPE = AUTH_LDAP
# #AUTH_TYPE = 2
# AUTH_LDAP_SERVER = "ldap://172.16.60.8"
# AUTH_LDAP_SEARCH = "DC=ie,DC=corp"
# AUTH_LDAP_UID_FIELD = "sAMAccountName"
# AUTH_LDAP_FIRSTNAME_FIELD = "givenName"
# AUTH_LDAP_LASTNAME_FIELD = "sn"
# AUTH_LDAP_EMAIL_FIELD = "mail"
# AUTH_LDAP_BIND_USER = "CN=LDAP binding (srv-ldapbind),OU=Service accounts,DC=ie,DC=corp"
# AUTH_LDAP_BIND_PASSWORD = "2M0*3kHzn%21^s"
# # AUTH_USER_REGISTRATION = True
# # AUTH_USER_REGISTRATION_ROLE = 'Admin'
# #AUTH_LDAP_ALLOW_SELF_SIGNED = True

# # AUTH_ROLES_MAPPING = {
# #     "CN=FS-App-BI-W,OU=DFS,OU=App,OU=NetworkFolders,DC=ie,DC=corp": ["Admin"],
# # }
# # AUTH_ROLES_SYNC_AT_LOGIN = True
# # AUTH_LDAP_GROUP_FIELD = "memberOf"
