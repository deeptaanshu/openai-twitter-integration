import json
import random
import openai
import tweepy
import time
import threading

def load_credentials(file_path='keys.json'):
    """
    Reads a JSON file containing both OpenAI and Twitter API keys.
    """
    with open(file_path, 'r') as f:
        credentials = json.load(f)
    return credentials

def chatgpt_short_answer(api_key):
    """
    This prompt will focus on a post related to Lithium in approximately 150 characters.
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
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
        model="gpt-4.1",
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
    credentials = load_credentials("/Users/deeptaanshukumar/keys_isp.json")

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.1",   # or another model if you prefer
        messages=[
            {"role": "user", "content": "Assume the role of a Tech industry professional and please create an informative and attention-grabbing post for Twitter with a length of exactly 250 characters about the latest developments in the field of Tech."}
        ],
        temperature=0.7  # Adjust the creativity of the answer if desired
    )
    # Extracting the answer text from the response
    answer = response.choices[0].message['content'].strip()

    twitter_response = post_to_twitter(answer, credentials)
    print("Tweet posted successfully:")
    print(twitter_response)
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
    time.sleep(180)

    # Expect a 150-character response
    answer = chatgpt_short_answer(chatgpt_api_key)
    print(f"ChatGPT's Response: {answer}")
    twitter_response = post_to_twitter(answer, credentials)
    print("Tweet posted successfully:")
    time.sleep(180)

    # Expect a 250-character response
    answer = chatgpt_long_answer(chatgpt_api_key)
    print(f"ChatGPT's Response: {answer}")
    twitter_response = post_to_twitter(answer, credentials)
    print("Tweet posted successfully:")
    time.sleep(180)

    # Expect a response with an article link, and potentially and embedded image
    answer = chatgpt_link_answer(chatgpt_api_key)
    print(f"ChatGPT's Response: {answer}")
    twitter_response = post_to_twitter(answer, credentials)
    print("Tweet posted successfully:")
    time.sleep(180)

    # Use the ChatGPT answer to post a tweet
    tweet_text = answer

    # Post the tweet using Twitter API keys from the same file


def print_epoch():
    while True:
        # Print the current epoch timestamp every 15 seconds
        print(f"Epoch timestamp: {int(time.time())}")
        time.sleep(15)

def call_function_every_4_hours():
    counter = 0
    while True:
        print(f"main() called at epoch: {int(time.time())}")
        main()
        answer = chatgpt_tech_answer(chatgpt_api_key)
        print(f"ChatGPT's Response: {answer}")

        # Sleep for 4 hours (4*3600 seconds)
        if counter % 3 == 0:
            # Expect a response about Tech, will serve as experiment control
            answer = chatgpt_tech_answer(chatgpt_api_key)
            print(f"ChatGPT's Response: {answer}")
        time.sleep(6 * 3600)
        counter = counter + 1

if __name__ == "__main__":
    # Create two threads: one for printing the epoch timestamp,
    # and another for calling the function every 4 hours.
    epoch_thread = threading.Thread(target=print_epoch)
    function_thread = threading.Thread(target=call_function_every_4_hours)

    # Optionally, set daemon=True if you want the threads to exit when the main thread terminates.
    epoch_thread.daemon = True
    function_thread.daemon = True

    # Start the threads
    epoch_thread.start()
    function_thread.start()

    # Keep the main thread alive indefinitely. This loop can be adjusted if you prefer another exit strategy.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
