# Polar

_A machine learning model to classify suspicious Linux commands based on probability of occurence_

## Dependencies

- Python 3.8+
- PIP3
- TensorFlow 2.0+
- Numpy
- Keras

## Notes

The occurrences.json and users.json were removed and purged to protect user information and credentials. occurrences.json can be genereted by declaring an "Occurrences" object with a JSON array of commands. users.json needs to be a JSON array with a index-user format for each user.

- users.json format

```json
[
  "1" : "user1",
  "2" : "user2",
  "3" : "user3",
      ...
  "N" : "userN",
]
```

- occurrences.json typical format

```json
[
  "ls" : 11597,
  "chmod" : 267,
  "cd" : 3695,
  ".." : 1548
]
```

## Install

```bash
# Clone repository
git clone git@github.com:alexantoniades/polar.py.git
# Change directory
cd polar.py
# Install dependencies
sudo pip3 install -r requirements.txt
```

## Usage

Train a model

```bash
$ python3 train.py -i ./data/inputs.json -o ./data/outputs.json
```

```bash
# Optional arguments
$ python3 train.py --help
usage: train.py [-h] -i INPUTS -o OUTPUTS [-es EVALUATION_SPLIT] [-vs VALIDATION_SPLIT] [-e EPOCHS] [-b BATCH_SIZE]

Train a neural network model.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTS, --inputs INPUTS
                        Path of JSON with model inputs
  -o OUTPUTS, --outputs OUTPUTS
                        Path of JSON with model outputs
  -es EVALUATION_SPLIT, --evaluation_split EVALUATION_SPLIT
                        Percentage of evaluation split. (default: 0.1)
  -vs VALIDATION_SPLIT, --validation_split VALIDATION_SPLIT
                        Percentage of validation split. (default: 0.25)
  -e EPOCHS, --epochs EPOCHS
                        Number of epochs. (default: 30)
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        Number of batch size. (default: 64)
```

Predict a value

```bash
$ python3 predict.py -v "mpirun -o hello hello.txt" -u 71
```

```bash
# Optional arguments
$ python3 predict.py --help
usage: predict.py [-h] [-m MODEL] [-w WEIGHTS] [-v VALUE] [-u USER]

Predict using a neural network model.

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Path of model.json file
  -w WEIGHTS, --weights WEIGHTS
                        Path of model_weights.h5 file
  -v VALUE, --value VALUE
                        Value to predict
  -u USER, --user USER  Command user
```

Produce SVG image from model

```bash
$ python3 model_to_svg.py -m ./model/model.json -w ./model/model_weights.h5 -s ./model.svg
```

```bash
# Optional arguments
$ python3 model_to_svg.py --help
usage: model_to_svg.py [-h] [-m MODEL] [-w WEIGHTS] [-s SVG]

Create an SVG file from a neural network model.

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Path of model.json file
  -w WEIGHTS, --weights WEIGHTS
                        Path of model_weights.h5 file
  -s SVG, --svg SVG     Path to save produced SVG file
```

Run web app demo using Theano back-end. Go to http://localhost:5000 for interface.

```bash
$ python3 app.py
Using Theano backend.
WARNING (theano.tensor.blas): Using NumPy C-API based implementation for BLAS functions.
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

To change Keras back-end, the keras config file needs to be altered, changing the "tensorflow" value to "theano".

```bash
$ sudo nano $HOME/.keras/keras.json
# From this ->
{
    "floatx": "float32",
    "epsilon": 1e-07,
    "backend": "tensorflow",
    "image_data_format": "channels_last"
}
# To this ->
{
    "floatx": "float32",
    "epsilon": 1e-07,
    "backend": "theano",
    "image_data_format": "channels_last"
}
```

Run TensorBoard with the log folder specified as an argument

```bash
$ tensorboard --logdir .\logs\fit
Serving TensorBoard on localhost; to expose to the network, use a proxy or pass --bind_all
TensorBoard 2.2.0 at http://localhost:6006/ (Press CTRL+C to quit)
```
