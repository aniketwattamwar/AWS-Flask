import streamlit as st #all streamlit commands will be available through the "st" alias
import rag_chatbot_lib as glib #reference to local lib script
import boto3
from botocore.exceptions import ClientError

st.set_page_config(page_title="RAG Chatbot") #HTML title
st.title("RAG Chatbot with Bedrock and AWS knowledge base") #page title

# Function to upload file to S3
def upload_to_s3(file, bucket_name, object_name=None):
    if object_name is None:
        object_name = file.name
    session = boto3.Session(
        aws_access_key_id='<your-key-id>',
        aws_secret_access_key='<your-access-key>',
        region_name='us-east-1'
    )
    s3_client = session.client('s3')
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        st.success(f"File {file.name} uploaded to S3 bucket {bucket_name} successfully.")
    except ClientError as e:
        st.error("Credentials not available.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# File uploader
uploaded_file = st.file_uploader("Upload a file")

# Add Knowledge button
if st.button("Add Knowledge"):
    if uploaded_file is not None:
        upload_to_s3(uploaded_file, 'rag-aws-bedrock')
    else:
        st.warning("Please upload a file first.")

if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history


chat_container = st.container()

input_text = st.chat_input("Chat with your bot here") #display a chat input box

if input_text:
    glib.chat_with_model(message_history=st.session_state.chat_history, new_text=input_text)


#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with chat_container.chat_message(message.role): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message.text) #display the chat content

