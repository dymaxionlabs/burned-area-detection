import keras


def load_model(model_path):
    return keras.models.load_model(model_path)
