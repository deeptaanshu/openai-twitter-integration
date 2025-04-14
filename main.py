import json
import random
import openai
import tweepy

def load_credentials(file_path='keys.json'):
    """
    Reads a JSON file containing both OpenAI and Twitter API keys.
    """
    with open(file_path, 'r') as f:
        credentials = json.load(f)
    return credentials

def get_random_question():
    """
    Returns a random question from a predefined list.
    You can add as many questions as you like.
    """
    questions = [
        "What is the meaning of life, please answer in 30 characters or less?",
        "If you could travel anywhere, where would you go, please answer in 30 characters or less?",
    ]
    return random.choice(questions)

def ask_chatgpt_test(question, api_key):
    """
    Uses OpenAI's ChatCompletion API to get an answer to the provided question.
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.5-preview",   # or another model if you prefer
        messages=[
            {"role": "user", "content": question}
        ],
        temperature=0.7  # Adjust the creativity of the answer if desired
    )
    # Extracting the answer text from the response
    answer = response.choices[0].message['content'].strip()
    return answer

def chatgpt_short_answer(api_key):
    """
    This prompt will focus on a post related to Lithium in approximately 150 characters.
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.5-preview",
        messages=[
            {"role": "user", "content": "Assume the role of a Lithium industry professional and please create an informative and attention-grabbing post for Twitter with a length of exactly 150 characters about the latest developments in the field of Lithium, such as Lithium mining, Lithium processing, and Lithium sales."}
        ],
        temperature=0.7  # Adjust the creativity of the answer if desired
    )
    # Extracting the answer text from the response
    answer = response.choices[0].message['content'].strip()
    return answer

def chatgpt_long_answer(api_key):
    """
    This prompt will focus on a post related to Lithium in approximately 250 characters.
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.5-preview",
        messages=[
            {"role": "user", "content": "Assume the role of a Lithium industry professional and please create an informative and attention-grabbing post for Twitter with a length of exactly 250 characters about the latest developments in the field of Lithium, such as Lithium mining, Lithium processing, and Lithium sales."}
        ],
        temperature=0.7  # Adjust the creativity of the answer if desired
    )
    # Extracting the answer text from the response
    answer = response.choices[0].message['content'].strip()
    return answer

def chatgpt_link_answer(api_key):
    """
    This prompt will focus on a post that contains a link to an article, potentially with an embedded image as well.
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o-search-preview", # need to use this model since 4.5-preview api doesn't allow for searching web for results
        messages=[
            {"role": "user", "content": "Assume you are the Head of Social Media of a Lithium company and are instructed to only post a working URL to a real article that is less than 200 characters long and discusses the latest developments in the field of Lithium, such as Lithium mining, Lithium processing, and Lithium sales."}
        ],
    )
    # Extracting the answer text from the response
    answer = response.choices[0].message['content'].strip()
    return answer

def chatgpt_tech_answer(api_key):
    """
    This model will serve as an experimental "control" and will post about any Tech-related topic
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.5-preview",   # or another model if you prefer
        messages=[
            {"role": "user", "content": "Assume the role of a Tech industry professional and please create an informative and attention-grabbing post for Twitter with a length of exactly 250 characters about the latest developments in the field of Tech."}
        ],
        temperature=0.7  # Adjust the creativity of the answer if desired
    )
    # Extracting the answer text from the response
    answer = response.choices[0].message['content'].strip()
    return answer

def post_to_twitter(tweet_text, twitter_creds):
    """
    Uses the Tweepy client to post a tweet with the given text.
    """
    # Initialize the Tweepy client with your credentials
    client = tweepy.Client(
        consumer_key=twitter_creds["twitter_api_key"],
        consumer_secret=twitter_creds["twitter_api_secret_key"],
        access_token=twitter_creds["twitter_access_token"],
        access_token_secret=twitter_creds["twitter_access_token_secret"],
        bearer_token=twitter_creds["bearer_token"]
    )

    # Post a tweet and return the API response
    tweet_response = client.create_tweet(text=tweet_text)
    return tweet_response

def main():
    # Load all API credentials from the file
    # CHANGE STRING TO THE LOCATION OF YOUR FILE WITH THE KEYS
    credentials = load_credentials("/Users/deeptaanshukumar/keys_isp.json")

    # Extract the OpenAI API key
    chatgpt_api_key = credentials["openai_api_key"]
    print("Got ChatGPT credentials")

#     # Get a random question from our predefined list
#     question = get_random_question()
#     print(f"Random Question: {question}")
#
#     # Ask ChatGPT the random question
#     answer = ask_chatgpt(question, chatgpt_api_key)
#     print(f"ChatGPT's Response: {answer}")

#     # Expect a 150-character response
#     answer = chatgpt_short_answer(chatgpt_api_key)
#     print(f"ChatGPT's Response: {answer}")

#     # Expect a 250-character response
#     answer = chatgpt_long_answer(chatgpt_api_key)
#     print(f"ChatGPT's Response: {answer}")

#     # Expect a response with an article link, and potentially and embedded image
#     answer = chatgpt_link_answer(chatgpt_api_key)
#     print(f"ChatGPT's Response: {answer}")

    # Expect a response about Tech, will serve as experiment control
    answer = chatgpt_tech_answer(chatgpt_api_key)
    print(f"ChatGPT's Response: {answer}")

    # Use the ChatGPT answer to post a tweet
    tweet_text = answer

    # Post the tweet using Twitter API keys from the same file
    twitter_response = post_to_twitter(tweet_text, credentials)
    print("Tweet posted successfully:")
    print(twitter_response)

if __name__ == "__main__":
    main()
