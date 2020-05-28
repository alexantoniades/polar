import argparse
from numpy import asarray
from tools import Occurrences, importJSON, load_model 
global model
global o
global results
#-------------------------------[ on script execution ]----------------------------------#
if __name__ == '__main__':
    # Declare parser
    parser = argparse.ArgumentParser(
        description='Predict using a neural network model.'
    )
    # Add model arguemnt
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='./model/model.json',
        help='Path of model.json file',
    )
    # Add model arguemnt
    parser.add_argument(
        '-w', '--weights',
        type=str,
        default='./model/model_weights.h5',
        help='Path of model_weights.h5 file',
    )
    # Add data arguemnt
    parser.add_argument(
        '-v', '--value',
        type=str,
        help='Value to predict',
        required=False
    )
    # Add data arguemnt
    parser.add_argument(
        '-u', '--user',
        type=str,
        help='Command user',
        required=False
    )
    # Parse arguments
    args = parser.parse_args()
    # Load model
    model = load_model(args.model, args.weights)
    # Initialise occurrence object
    o = Occurrences()
    # Predict value
    results = model.predict(asarray([o.encode(args.value, args.user)]))
    # Print results
    print(f"Suspicious: {round(results[0][0]*100, 2)}%")
    print(f"Neutral: {round(results[0][1]*100, 2)}%")