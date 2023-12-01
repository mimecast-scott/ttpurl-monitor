# ttpurl-monitor
A dockerized python script that collects the last 30 days of clicked and 'allowed' TTP URL logs and checks if any URLs clicked and blocked(malicious) in the past 20 minutes were previously clicked and allowed and takes action.

| ENV VAR     | Description |
| ----------- | ----------- |
| CLIENT_ID | Mimecast API 2.0 Client ID |
| CLIENT_SECRET | Mimecast API 2.0 Client Secret |
| CLIENT_SECRET | Mimecast API 2.0 Client Secret |
| SMTP_SERVER   | The SMTP server (or hostname) able to accept connect via TLS (TCP/587)       |
| SMTP_USER   | The username of the SMTP user for the purpose of auth and SMTP FROM:        |
| SMTP_PW   | The password of the SMTP user        |
| EMAIL_RECIPIENTS      | A space seperated list of recipients, e.g. `recipient1@gmail.com recipient2@gmail.com`       |


Try it yourself
````
docker run -it -e EMAIL_RECIPIENTS="recipient1@gmail.com recipient2@gmail.com" -e SMTP_SERVER="192.168.89.1." -e SMTP_USER="sender@mydomain.com" -e SMTP_PW="YourP@ssw0rd" -e CLIENT_ID="<--Your Mimecast API Client ID-->" -e CLIENT_SECRET=<--Your Mimecast API Client Secret--> smck83/mimecast-ttp-url-monitor
````
