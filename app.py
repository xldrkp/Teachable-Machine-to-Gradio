from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import gradio as gr

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("model/keras_model.h5", compile=False)

# Load the labels
class_names = open("model/labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def image_class(image):

    # Replace this with the path to your image
    # image = Image.open(image).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return [class_name[2:], (float(confidence_score) * 100)]


demo = gr.Interface(
    image_class,
    gr.Image(type="pil"),
    [
        gr.Textbox(label="Klasse"), 
        gr.Textbox(label="Sicherheit der Vorhersage (confidence)")
    ],
    flagging_options=["incorrect"],
    examples=[
        "data/cats_test/101.jpg",
        "data/dogs_test/111.jpg",
        "data/cats_test/102.jpg",
        "data/dogs_test/112.jpg",
    ],
    description="""
    # Verwendung eines Modells aus Teachable Machine in Gradio
    """
)

if __name__ == "__main__":
    demo.launch(share=False)
