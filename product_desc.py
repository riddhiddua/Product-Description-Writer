import os
import streamlit as st
import google.generativeai as genai

# Set your Google Generative AI API key
genai.configure(api_key="AIzaSyCB3eGaCYtBEYznObWrDvZkJmbSi1c5N30")  # Replace "YOUR_API_KEY" with your actual API key

# Model setup
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

model1 = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit app
st.title("Product Description Writer")

# Create tabs for text and image input
tab1, tab2 = st.tabs(["Product Description by Text", "Product Description by Image"])

# Product Description by Text Tab
with tab1:
    st.header("Generate Product Description from Text")
    product_title = st.text_input("Product Title")
    product_url = st.text_input("Product URL")
    user_description = st.text_area("Product Description (in your own words)")
    num_words = st.slider("Number of Words", 0, 1000, 250)  # Default to 250 words

    if st.button("Generate Description"):
        if product_title and user_description:
            prompt_parts = [
                f"Write an SEO-optimized, engaging product description of about {num_words} words for the product: '{product_title}'.",
                f"Here is some information about the product: {user_description}",
                f"If relevant, you can also mention the product URL: {product_url}"
            ]

            response = model.generate_content(prompt_parts)
            st.write("**Generated Product Description:**")
            st.write(response.text)
        else:
            st.warning("Please provide the Product Title and your own Product Description.")

# Product Description by Image Tab
with tab2:
    st.header("Generate Product Description from Image")
    uploaded_image = st.file_uploader("Upload Product Image", type=["jpg", "png", "jpeg"])
    num_words1 = st.slider("Number of Words for article", 0, 1000, 250)
    print(uploaded_image)

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
          # Default to 250 words
        # **Important:** The code below for image-based descriptions is a placeholder!
        #  You need to replace this logic with the appropriate way to send the image to the "gemini-1.0-pro-vision-latest" model. 
        #  Consult the Google Generative AI documentation for how to use image inputs with the model.
        if st.button("Generate Description through image"):
            # st.warning("Image-based description generation is not yet implemented. Please refer to Google Generative AI documentation for how to use images with the model.") 
            file_name = uploaded_image.name
            directory_path = "./images/"  # Change this path to your desired directory
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            # Concatenate directory path and file name to get the file path
            file_path = os.path.join(directory_path, uploaded_image.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_image.getvalue())
            # *** Replace the placeholder code below with the actual image processing and prompt generation logic ***
            img = genai.upload_file(file_path)
            prompt_parts = [
                f"Write an SEO-optimized, engaging product description of about {num_words1} words for the product image.", 
                "It should be in a format that is easily usable on a website, it should be in a paragraph style with bold and italics.",
                genai.upload_file(file_path)
            ]
            response = model1.generate_content(prompt_parts)
            st.write("**Generated Product Description:**")
            st.write(response.text)
