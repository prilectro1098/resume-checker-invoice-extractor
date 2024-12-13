import streamlit as st
from dotenv import load_dotenv
import os


load_dotenv()


st.set_page_config(page_title="AI Products", page_icon=":robot:", layout="wide")


st.sidebar.title("AI Products")
option = st.sidebar.radio("Choose a Product:", ["ATS", "Invoice Extractor"])

if option == "ATS":
    # ATS Code
    import google.generativeai as genai
    import PyPDF2 as pdf

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

# elif option == "YT Summarizer":
#     import google.generativeai as genai
#     from youtube_transcript_api import YouTubeTranscriptApi
#     from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

#     genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#     prompt = """You are a YouTube video summarizer. You will take the transcript text
#     and summarize the entire video, providing the important points within 250 words.
#     Please provide the summary of the text given here: """

    # def extract_transcript_details(youtube_video_url):
    #     try:
    #         video_id = youtube_video_url.split("v=")[1].split("&")[0]
            # transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

    #         transcript = " ".join([i["text"] for i in transcript_text])
    #         return transcript

    #     except ConnectionError:
    #         st.error("Network issue: Unable to connect to YouTube servers. Please try again later.")
    #     except TranscriptsDisabled:
    #         st.error("This video does not have transcripts enabled.")
    #     except NoTranscriptFound:
    #         st.error("No transcripts available for this video.")
    #     except Exception as e:
    #         st.error(f"An unexpected error occurred: {e}")
    #     return None

    # def generate_gemini_content(transcript_text, prompt):
    #     try:
    #         model = genai.GenerativeModel("gemini-pro")
    #         response = model.generate_content(prompt + transcript_text)
    #         return response.text
    #     except Exception as e:
    #         st.error(f"Error generating summary: {e}")
    #         return None

    # st.title("YouTube Transcript to Detailed Notes Converter")
    # youtube_link = st.text_input("Enter YouTube Video Link:")

    # if youtube_link:
    #     try:
    #         video_id = youtube_link.split("v=")[1].split("&")[0]
    #         st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    #     except IndexError:
    #         st.error("Invalid YouTube link. Please ensure it contains 'v=' followed by the video ID.")

    # if st.button("Get Detailed Notes"):
    #     transcript_text = extract_transcript_details(youtube_link)

    #     if transcript_text:
    #         summary = generate_gemini_content(transcript_text, prompt)
    #         if summary:
    #             st.markdown("## Detailed Notes:")
    #             st.write(summary)


elif option == "Invoice Extractor":
    # Invoice Extractor Code
    from PIL import Image
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
