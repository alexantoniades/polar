from flask import Flask, render_template, request, jsonify
from tools import Occurrences, load_model
from numpy import asarray
#--------------------------[ Load model and occurrences ]------------------------------#
# Load model
model = load_model('./model/model.json', './model/model_weights.h5')
# Initialise occurrence object
o = Occurrences()
# Wrapper function to predict value
def predict(command, user):
    global model
    global o
    result = model.predict(asarray([o.encode(str(command), str(user))]))
    return(result)
# Declare Web App
app = Flask(__name__, static_folder='assets')

@app.route('/')
def home():
    return("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/assets/sass/style.css">
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <title>Project demo</title>
</head>
<body>
    <div class="container">
        <h1 class="label">
            Classification of Malicious Unix Commands
        </h1>
        <div class="form">
            <input type="text" id="command" class="txt" placeholder="Type a command...">
            <input type="button" id="submit-btn" class="btn" value="Predict!">
        </div>
        <canvas id="chart-bar" class="canvas"></canvas>
        <canvas id="chart-doughnut" class="canvas"></canvas>
        <canvas id="chart-pie" class="canvas"></canvas>
    </div>
    <script src="/assets/js/main.js"></script>
</body>
</html>
""")
#----------------------------------[ App route ]----------------------------------------#
@app.route('/api', methods=['GET'])
def api():
    # Predict value
    results = predict(request.args['command'], request.args['user'])
    # Return response
    return(jsonify(
        command=request.args['command'],
        suspicious=float(results[0][0]),
        neutral=float(results[0][1]),
        totalCommands=o.total,
        occurrencesInteger=[o.find(word) for word in request.args['command'].split(' ')],
        occurrencesAverage=o.sentence(request.args['command']),
        occurrencesFloat=[o.ratio(word) for word in request.args['command'].split(' ')]
    ))
#------------------------------[ on script execution ]---------------------------------#
if __name__ == '__main__':
    app.run()