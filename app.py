from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def calculator():
    # Retrieve instance metadata
    try:
        token_response = requests.put("http://169.254.169.254/latest/api/token", headers={"X-aws-ec2-metadata-token-ttl-seconds": "3600"})
        token = token_response.text.strip()
        instance_id_response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", headers={"X-aws-ec2-metadata-token": token})
        instance_id = instance_id_response.text.strip()
        local-ipv4_response = requests.get("http://169.254.169.254/latest/meta-data/placement/local-ipv4", headers={"X-aws-ec2-metadata-token": token})
        local-ipv4 = local_ipv4_response.text.strip()
    except requests.exceptions.RequestException as e:
        print("Error fetching instance metadata:", e)
        instance_id = "Error"
        local-ipv4 = "Error"
    
    # Render the template with instance metadata
    return render_template('calculator.html', instance_id=instance_id, local-ipv4=local-ipv4)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

