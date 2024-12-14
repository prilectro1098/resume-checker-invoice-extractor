import streamlit as st
from dotenv import load_dotenv
import os
from textblob import TextBlob
from deep_translator import GoogleTranslator
from PIL import Image
import PyPDF2 as pdf
import google.generativeai as genai

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Products", page_icon=":robot:", layout="wide")

# Sidebar options
st.sidebar.title("AI Products")
option = st.sidebar.radio("Choose a Product:", ["ATS", "Invoice Extractor", "Sentiment Analysis"])

# Configure Google API for generative model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ATS System
if option == "ATS":
    def get_gemini_response(input):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input)
        return response.text

    def input_pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text

    input_prompt = """
    Hey Act Like a skilled or very experienced ATS(Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analyst
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving the resumes. Assign the percentage Matching based 
    on JD and
    the missing keywords with high accuracy
    resume:{text}
    description:{jd}

    I want the response in multipe lines string having the prettier structure
    {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
    """

    st.title("AI ATS SYSTEM")
    st.text("Improve Your Resume ATS")
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload your Resume", type="pdf", help="Please upload the PDF file")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt.format(text=text, jd=jd))
            st.subheader("Response")
            st.write(response)

# Invoice Extractor
elif option == "Invoice Extractor":
    def get_gemini_response(input, image, prompt):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([input, image[0], prompt])
        return response.text

    def input_image_setup(uploaded_file):
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")

    st.header("Gemini Image Application")

    input = st.text_input("Input Prompt:", key="input", placeholder="Enter a question or prompt here...")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=False, width=600)

    submit = st.button("Tell me about the image", key="submit", help="Click to analyze the image")

    input_prompt = """
        You are an expert in understanding invoices.
        You will receive input images as invoices &
        you will have to answer questions based on the input image.
    """

    if submit:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input)
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")

# Sentiment Analysis for Multilingual Reviews
elif option == "Sentiment Analysis":
    st.title("Multilingual Sentiment Analysis for Reviews")

    def translate_text(text, target_language="en"):
        try:
            # Translate the text to the target language (English by default)
            translated = GoogleTranslator(source="auto", target=target_language).translate(text)
            return translated
        except Exception as e:
            return f"Error translating text: {e}"

    def analyze_sentiment_gemini(text):
        input_prompt = f"""
        You are a sentiment analysis expert.
        Please evaluate the sentiment of the following text:
        Text: {text}
        I want the response to be Positive, Negative, or Neutral based on the text's sentiment.
        """
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input_prompt)
        return response.text.strip()

    st.text("Analyze Reviews in Any Language")

    # Text input for manual review entry
    review_text = st.text_area("Enter review text for sentiment analysis:")

    submit = st.button("Submit Review")

    if submit and review_text:
        # Translate text to English for consistent sentiment analysis
        translated_review = translate_text(review_text)

        st.subheader("Translated Review (if necessary)")
        st.write(translated_review)

        # Perform sentiment analysis using Google's API
        sentiment = analyze_sentiment_gemini(translated_review)

        st.subheader(f"Sentiment Analysis Result: {sentiment}")
