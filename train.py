import argparse, json, os, datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from numpy import asarray
from tools import importJSON, save_model, split_by_percentage
# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#--------------------------------[ Logger directory ]------------------------------------#
log_directory = "logs/fit/" + datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
#-------------------------[ TensorBoard callback function ]------------------------------#
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_directory, histogram_freq=1)
#------------------------------[ Train model function ]----------------------------------#
def train_model(
    inputs=[], 
    outputs=[], 
    evaluation_split=0.15, 
    validation_split=0.25, 
    epochs=5, 
    batch_size=64
    ):
    try:
        training_inputs, evaluation_inputs = split_by_percentage(inputs, evaluation_split)
        training_outputs, evaluation_outputs = split_by_percentage(outputs, evaluation_split)
        input_size = len(training_inputs[0])
        model = Sequential([
            Dense(2048, input_shape=(input_size,)),
            Dense(1024, activation='relu'), Dropout(0.2),
            Dense(512, activation='tanh'), Dropout(0.2),
            Dense(256, activation='relu'), Dropout(0.2),
            Dense(2, activation='softmax')
        ])
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        model.summary()
        history = model.fit(
            asarray(inputs),
            asarray(outputs),
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[tensorboard_callback]
        )
        scores = model.evaluate(
            asarray(evaluation_inputs),
            asarray(evaluation_outputs)
        )
        print(f"Loss: {scores[0]}, Accuracy: {scores[1]}")
        return(model)
    except Exception as error:
        print(f"Error: train_model(...) -> {error}")
#------------------------------[ on script execution ]----------------------------------#
if __name__ == '__main__':
    # Declare parser
    parser = argparse.ArgumentParser(
        description='Train a neural network model.'
    )
    # Add inputs arguemnt
    parser.add_argument(
        '-i', '--inputs',
        type=str,
        help='Path of JSON with model inputs',
        required=True
    )
    # Add outputs arguemnt
    parser.add_argument(
        '-o', '--outputs',
        type=str,
        help='Path of JSON with model outputs',
        required=True
    )
    # Add evaluation_split arguemnt
    parser.add_argument(
        '-es', '--evaluation_split',
        type=float,
        default=0.15,
        help='Percentage of evaluation split. (default: 0.1)'
    )
    # Add validation_split arguemnt
    parser.add_argument(
        '-vs', '--validation_split',
        type=float,
        default=0.25,
        help='Percentage of validation split. (default: 0.25)'
    )
    # Add epochs arguemnt
    parser.add_argument(
        '-e', '--epochs',
        type=int,
        default=30,
        help='Number of epochs. (default: 30)'
    )
    # Add batch_size arguemnt
    parser.add_argument(
        '-b', '--batch_size',
        type=int,
        default=64,
        help='Number of batch size. (default: 64)'
    )
    # Parse arguments
    args = parser.parse_args()
    # Train model
    model = train_model(
        inputs=importJSON(args.inputs), 
        outputs=importJSON(args.outputs),
        evaluation_split=args.evaluation_split,
        validation_split=args.validation_split,
        epochs=args.epochs,
        batch_size=args.batch_size
    )
    # Save model process
    if input('Save model?[y/N]: ').lower() in ('y', 'yes'):
        model_path = input('Path for model?[model/]: ')
        if model_path == '':
            model_path = './model'
        save_model(model, model_path)
        print('Model saved')
    else:
        print('Model not saved')
