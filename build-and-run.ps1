.\setEnv.ps1 # set credentials

docker build -t smck83/mimecast-ttp-url-monitor .
docker run -it -e EMAIL_RECIPIENTS=$Env:EMAIL_RECIPIENTS -e SMTP_SERVER=$Env:SMTP_SERVER -e SMTP_USER=$Env:SMTP_USER -e SMTP_PW=$Env:SMTP_PW -e CLIENT_ID=$Env:CLIENT_ID -e CLIENT_SECRET=$Env:CLIENT_SECRET -p 8000:8000 smck83/mimecast-ttp-url-monitor

