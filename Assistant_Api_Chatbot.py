import openai
import time

# Initialize the client
client = openai.OpenAI(api_key="Add your key here")

#Uncomment the code to run this steps to create an assistant.
#Use that created assistant's id to use it for document chat 
"""
file = client.files.create(
    file=open("FILEPATH TO UPLOAD", "rb"),
    purpose='assistants'
)

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="NAME OF THE ASSISTANT",
    instructions="INSTRUCTIONS GIVEN TO THE ASSISTANT",
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
)
"""
#Replace the assistant.id with the id given after creating the assitant
assistantid = assistant.id

# Step 2: Create a Thread
thread = client.beta.threads.create()

while True:
    usr_content = input("Enter the query: ")
    # Step 3: Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=usr_content
    )

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistantid,
    )

    #print(run.model_dump_json(indent=4))
    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id 
        )
        
    # Retrieve messages added by the assistant
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order="asc"
    )    

    for msg in messages.data:
        if msg.run_id == run.id and msg.role == "assistant":
            print(f"{msg.role}: {msg.content[0].text.value}")

