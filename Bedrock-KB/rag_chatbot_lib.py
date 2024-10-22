import itertools
import boto3
import chromadb
from botocore.exceptions import ClientError
from oauthlib.uri_validate import query

# Model id list: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html

MAX_MESSAGES = 10

class ChatMessage(): #create a class that can store image and text messages
    def __init__(self, role, text):
        self.role = role
        self.text = text


def chat_with_model(message_history, new_text=None):
    session = boto3.Session(
        aws_access_key_id='<your-key-id>',
        aws_secret_access_key='<your-access-key>',
        region_name='us-east-1'
    )

    # bedrock = session.client(service_name='bedrock-runtime',region_name="us-east-1")
    # bedrock_agent_client = session.client('bedrock-agent', region_name='us-east-1')
    # get_kb_response = bedrock_agent_client.get_knowledge_base(knowledgeBaseId='9QFLGYP5BZ')

    bedrock_agent_runtime_client = session.client("bedrock-agent-runtime", region_name='us-east-1')

    model_arn = f'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-premier-v1:0'


    new_text_message = ChatMessage('user', text=new_text)
    message_history.append(new_text_message)

    number_of_messages = len(message_history)

    if number_of_messages > MAX_MESSAGES:
        del message_history[
            0: (number_of_messages - MAX_MESSAGES) * 2]  # make sure we remove both the user and assistant responses

    # input_text = " ".join([msg.text for msg in message_history]) + " " + new_text

    response = bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': new_text
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': '9QFLGYP5BZ',
                'modelArn': model_arn
            }
        },
    )

    generated_text = response['output']['text']

    response_chat_message = ChatMessage('assistant', generated_text)

    message_history.append(response_chat_message)
    # print(message_history)

    res = bedrock_agent_runtime_client.retrieve(
        knowledgeBaseId = '9QFLGYP5BZ',
        retrievalQuery = {
        'text': new_text
        }
    )
    print(res)



    return
