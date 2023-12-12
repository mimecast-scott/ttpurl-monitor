````
DISCLAIMER: This is an unsupported, unofficial, experimental workflow leveraging the Mimecast 2.0 API.

Mimecast TTP URL logs are collected and cross-checked so that administrators can be made aware if a malicious URL clicked in the the past 20 mins, was previously(in the past 30 days) clicked by an end user and allowed. Current resposne is an e-mail notification, but this could easily be to remediate the e-mail and add sender to 'Blocked Senders' profile group.

https://developer.services.mimecast.com/docs/securityevents/1/routes/api/ttp/url/get-logs/post

NOTE: This script (1st Dec 23) does not yet support pagination, but can easily be added to handle collection of 30 days worth of TTP URL logs.
````

# ttpurl-monitor
A dockerized python script that grabs the latest URLs that were blocked and classified malicious and cross checks them against the past 30 days of clicked and allowed (i.e. clean) URL. If there is a match, take action (e.g. send an e-mail notification).


| ENV VAR     | Description |
| ----------- | ----------- |
| CLIENT_ID | Mimecast API 2.0 Client ID |
| CLIENT_SECRET | Mimecast API 2.0 Client Secret |
| SMTP_SERVER   | The SMTP server (or hostname) able to accept connect via TLS (TCP/587)       |
| SMTP_USER   | The username of the SMTP user for the purpose of auth and SMTP FROM:        |
| SMTP_PW   | The password of the SMTP user        |
| EMAIL_RECIPIENTS      | A space seperated list of recipients, e.g. `recipient1@gmail.com recipient2@gmail.com`       |


Try it yourself
````
docker run -it -e EMAIL_RECIPIENTS="recipient1@gmail.com recipient2@gmail.com" -e SMTP_SERVER="192.168.89.1" -e SMTP_USER="sender@mydomain.com" -e SMTP_PW="YourP@ssw0rd" -e CLIENT_ID="<--Your Mimecast API Client ID-->" -e CLIENT_SECRET=<--Your Mimecast API Client Secret--> smck83/mimecast-ttp-url-monitor
````

Example showing stdout when check is `True`
![Example behaviour when a URL previously allowed is recently considered malicious](https://github.com/mimecast-scott/ttpurl-monitor/blob/main/ttpurlmonitor.png?raw=true)

Example e-mail notification
![Example E-mail response](https://github.com/mimecast-scott/ttpurl-monitor/blob/main/ttpurlmonitorEmail2.png?raw=true)
