#!/bin/bash
sudo yum update -y
sudo yum install git python3-pip -y
sudo pip3 install requests
sudo pip3 install flask
git clone https://github.com/ashbsl/flask-app.git /home/ec2-user/flask-app
cd /home/ec2-user/flask-app
nohup python3 app.py >/dev/null 2>&1 &
