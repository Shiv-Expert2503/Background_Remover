import base64
import requests

import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates as im_coordinates
import cv2
import numpy as np

import os

st.set_page_config(layout='wide')

api_endpoint = 'https://shivanshsingh.ap-south-1.modelbit.com/v1/remove_background/latest'

col01, col02 = st.columns(2)

file = col02.file_uploader("", type=['jpg', 'jpeg', 'png'])
if file is not None:
    image = Image.open(file).convert('RGB')

    image = image.resize((685, int(image.height * 685 / image.width)))

    col1, col2 = col02.columns(2)

    placeholder0 = col02.empty()
    with placeholder0:
        value = im_coordinates(image)
        if value is not None:
            print(value)

    if col1.button('Original', use_container_width=True):

        placeholder0.empty()
        placeholder1 = col02.empty()

        with placeholder1:
            col02.image(image, use_column_width=True)

    if col2.button('Remove Background', type='primary', use_container_width=True):

        placeholder0.empty()
        placeholder2 = col02.empty()

        file_name = '{}_{}_{}.png'.format(file.name, value['x'], value['y'])
        if os.path.exists(file_name):
            cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
        else:

            _, image_bytes = cv2.imencode('.png', np.asarray(image))

            image_bytes = image_bytes.tobytes()

            image_bytes_encoded_base64 = base64.b64encode(image_bytes).decode('utf-8')

            api_data = {"data": [image_bytes_encoded_base64, value['x'], value['y']]}
            response = requests.post(api_endpoint, json=api_data)

            result_image = response.json()['data']

            result_image_bytes = base64.b64decode(result_image)

            result_image = cv2.imdecode(np.frombuffer(result_image_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            cv2.imwrite(file_name, result_image)

            with placeholder2:
                col02.image(result_image, use_column_width=True)