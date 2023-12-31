import requests
import json
import auth
import datetime
import time
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

SMTPserver = os.getenv("SMTP_SERVER")
SMTPsender = os.getenv("SMTP_USER")
SMTPuser = os.getenv("SMTP_USER")
SMTPpassword = os.getenv("SMTP_PW")
emailRecipients = list((os.getenv("EMAIL_RECIPIENTS")).split(" "))

includeDomains = True # check for the domain of a recently clicked URL that was malicious, e.g. my.domain.com in https://my.domain.com/abc123
allowedURLHistory = 30 # days - How far back (days), to check recently clicked URLs that were previously allowed
checkMaliciousURLs = 20 # minutes - Check the last X minutes of clicked malicious URLs against {allowedURLHistory} days worth of allowed clicked URL

# 43200 mins = 30 days
# 10800 mins =  7 days
# 1440 mins = 1 day

def getURLS(bearer,scanResult="all",timeDelta=(60 * allowedURLHistory)):
    startDate = (datetime.datetime.now()-datetime.timedelta(minutes=timeDelta)).strftime("%Y-%m-%dT%H:%M:%S+0000") #"2023-10-01T14:49:18+0000"
    #
    # add logic to handle pagination - relevant when collecting lots od URL e.g, 30 days worth.
    #
    url = "https://api.services.mimecast.com/api/ttp/url/get-logs"

    payload = json.dumps({
    "data": [
        {
        "from": f"{startDate}",
        "scanResult": scanResult
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {bearer}'

    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        return []
    else:
        response = json.loads(response.text)
        return response["data"][0]["clickLogs"]

def sendEmail(receivers=emailRecipients,subject="Empty",emailbody='Empty'):
    msg = EmailMessage()
    #msg = MIMEMultipart('alternative')
    msg['Subject'] = f"TTP URL Log Monitor - {subject}"
    msg['From'] = SMTPsender
    msg['To'] = list(receivers)
    #text = emailbody
    #html = emailbody
    msg.set_content(emailbody)
    #part1 = MIMEText(text, 'plain')
    #part2 = MIMEText(html, 'html')
    #msg.attach(part1)
    #msg.attach(part2)
    s = smtplib.SMTP(SMTPserver,25)
    print(datetime.datetime.now(),"Trying to send e-mail notification")
    try:
        s.connect(SMTPserver,587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(SMTPuser, SMTPpassword)
        s.send_message(msg)

    except Exception as e:
        print(datetime.datetime.now(),"Something went wrong:",e)
        s.quit()
    else:
        print(datetime.datetime.now(),"Success! - E-mail response sent to ",receivers)
        s.quit()


def runMe(bearer):
    maliciousURL = getURLS(bearer,"malicious",checkMaliciousURLs) # get malicious URLs clicked and blocked in the past 20 minutes
    maliciousURL = { each['url'] : each for each in maliciousURL }.values() # remove duplicates
    if len(maliciousURL) > 0:
        print("Found:",len(maliciousURL),"malicious URL clicked in the past",checkMaliciousURLs,"minutes")
        allowedClickedURL = getURLS(bearer,"clean") # get list of URLs previously allowed for the past 30 days
        print("--------------------------------")
        print(f"!! Found some bad URL clicked in teh past {checkMaliciousURLs} minutes.")
        for badUrl in maliciousURL:
            badURLCount =0
            print(f"Checking if bad URL: {badUrl['url']} has been previously clicked (in the past {allowedURLHistory} days) and allowed:")
            if "/" in badUrl["url"]:
                badUrl["domain"] = badUrl["url"].split("/")[2]
            else:
                badUrl["domain"] = badUrl["url"]
            emailBody = ["Malicious URL clicked(" + badUrl["date"] + "):\n" + badUrl["url"].replace(".","(.)").replace("http","hxxp") + "\n\nPreviously clicked and allowed:\nTimestamp\t \t \t Username \t \t \t  URL\t \t \t messageId"]
            for allowedUrl in allowedClickedURL: 
                if includeDomains and (badUrl["url"] == allowedUrl["url"] or badUrl["domain"] in allowedUrl["url"]) and badUrl["date"] > allowedUrl["date"]:
                    print(f"Oops URL:{badUrl['url']} or Domain:{badUrl['domain']} has been clicked previously ({allowedUrl['url']})\n by {allowedUrl['userEmailAddress']}) \n URL was blocked on click:{badUrl['date']}\n URL was previously allowed on click:{allowedUrl['date']}")
                    print(f" Remediating {allowedUrl['messageId']}")
                    #
                    # add some code to remediate the messageID
                    #
                    emailBody.append(f"{allowedUrl['date']}\t\t\t{allowedUrl['userEmailAddress']}\t\t\t{allowedUrl['url'][:36]}...\t\t\t {allowedUrl['messageId']}")
                    #
                elif (badUrl["url"] == allowedUrl["url"] and badUrl["date"] > allowedUrl["date"]):
                    print(f"Oops :{badUrl['url']} {badUrl['domain']} | \n bad time:{badUrl['date']}\n is in {allowedUrl['url']}\n good time:{allowedUrl['date']}")
                    print(f" Remediating {allowedUrl['messageId']}")
                    #
                    # add some code to remediate the messageID
                    #
                    emailBody.append(f"{allowedUrl['date']}\t\t\t{allowedUrl['userEmailAddress']}\t\t\t{allowedUrl['url'][:36]}...\t\t\t {allowedUrl['messageId']}")
                    #
                else:
                    badURLCount += 1
            if SMTPserver and SMTPuser and SMTPpassword and emailRecipients and len(emailBody) > 1:
                
                sendEmail(emailRecipients,"Previously allowed URLs now malicious","\n".join(emailBody))              
            if badURLCount > 0:
                if includeDomains:
                    print(f"Bad domain or URLs found, though: {badUrl['domain']} or {badUrl['url']} have not been previously clicked and allowed")
                else:
                    print(f"Bad URLs found, though: {badUrl['url']} has not been previously clicked and allowed")
    else:
        print(f"No malicious URL found in the past {checkMaliciousURLs} minutes")
def main():

    bearer = auth.get_bearer_token() #request initial token
    
    while True:
        try:
            runMe(bearer)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                # If the token is expired, refresh it
                bearer = auth.get_bearer_token()
            elif e.response.status_code == 429:
                print("Rate limiting - backing off for",e.response.headers['X-RateLimit-Reset'],"milliseconds")
                time.sleep(e.response.headers['X-RateLimit-Reset']/1000)

        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            break
       
        print(f"Waiting {checkMaliciousURLs} minutes before checking again")
        time.sleep(checkMaliciousURLs*60)

if __name__ == "__main__":
        main()

