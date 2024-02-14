from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_instance_metadata():
    try:
        # Retrieve instance metadata
        token_response = requests.put("http://169.254.169.254/latest/api/token", headers={"X-aws-ec2-metadata-token-ttl-seconds": "3600"})
        token = token_response.text.strip()
        instance_id_response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", headers={"X-aws-ec2-metadata-token": token})
        instance_id = instance_id_response.text.strip()
        local_ipv4_response = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4", headers={"X-aws-ec2-metadata-token": token})
        local_ipv4 = local_ipv4_response.text.strip()
        return instance_id, local_ipv4
    except requests.exceptions.RequestException as e:
        print("Error fetching instance metadata:", e)
        return "Error", "Error"

@app.route('/')
def calculator():
    # Retrieve instance metadata
    instance_id, local_ipv4 = get_instance_metadata()
    return render_template('calculator.html', instance_id=instance_id, local_ipv4=local_ipv4)

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']
    
    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return 'Error: Division by zero'
    
    # Retrieve instance metadata
    instance_id, local_ipv4 = get_instance_metadata()
    return render_template('result.html', num1=num1, num2=num2, operation=operation, result=result, instance_id=instance_id, local_ipv4=local_ipv4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
