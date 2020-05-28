import json, argparse, os
from IPython.display import SVG
from keras.utils import plot_model, model_to_dot
from tools import load_model, importJSON
# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#-------------------------------[ on script execution ]----------------------------------#
if __name__ == "__main__":
    # Declare parser
    parser = argparse.ArgumentParser(
        description='Create an SVG file from a neural network model.'
    )
    # Add model arguemnt
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='./model/model.json',
        help='Path of model.json file',
    )
    # Add weights arguemnt
    parser.add_argument(
        '-w', '--weights',
        type=str,
        default='./model/model_weights.h5',
        help='Path of model_weights.h5 file',
    )
    # Add data arguemnt
    parser.add_argument(
        '-s', '--svg',
        type=str,
        default='./model.svg',
        help='Path to save produced SVG file'
    )
    # Parse arguments
    args = parser.parse_args()
    # Import model
    model = load_model(args.model, args.weights)
    # Generate SVG
    image = SVG(model_to_dot(model).create(prog='dot', format='svg'))
    # Save SVG image
    with open(args.svg, 'w') as f:
        f.write(image.data)
