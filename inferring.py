import os
import openai
from IPython.display import display, HTML
from dotenv import dotenv_values

config = dotenv_values(".env")

openai.api_key = config['OPENAI_API_KEY']


def get_completion(prompt, model="gpt-3.5-turbo"):
    "get completion"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # this is the degree of randomness of the model's output
        temperature=0,
    )
    return response.choices[0].message["content"]


# Product reviw text
lamp_review = """
Needed a nice lamp for my bedroom, and this one had \
additional storage and not too high of a price point. \
Got it fast.  The string to our lamp broke during the \
transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put \
together.  I had a missing part, so I contacted their \
support and they very quickly got me the missing piece! \
Lumina seems to me to be a great company that cares \
about their customers and products!!
"""

# Setiment (positive/negative)
prompt1 = f"""
What is the sentiment of the following product review,
which is delimited with triple backticks?

Review text: '''{lamp_review}'''
"""
response1 = get_completion(prompt1)
print(response1)

prompt2 = f"""
What is the sentiment of the following product review,
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: '''{lamp_review}'''
"""
response2 = get_completion(prompt2)
print(response2)

# Identify types of emotions
prompt3 = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: '''{lamp_review}'''
"""
response3 = get_completion(prompt3)
print(response3)

# Identify anger
prompt4 = f"""
Is the writer of the following review expressing anger?\
The review is delimited with triple backticks. \
Give your answer as either yes or no.

Review text: '''{lamp_review}'''
"""
response4 = get_completion(prompt4)
print(response4)

# Extract product and company name from customer reviews
prompt5 = f"""
Identify the following items from the review text:
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.

Review text: '''{lamp_review}'''
"""
response5 = get_completion(prompt5)
print(response5)

# Doing multiple tasks at once
prompt6 = f"""
Identify the following items from the review text:
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''{lamp_review}'''
"""
response6 = get_completion(prompt6)
print(response6)

# Infering Topics
story = """
In a recent survey conducted by the government,
public sector employees were asked to rate their level
of satisfaction with the department they work at.
The results revealed that NASA was the most popular
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings,
stating, "I'm not surprised that NASA came out on top.
It's a great place to work with amazing people and
incredible opportunities. I'm proud to be a part of
such an innovative organization."

The results were also welcomed by NASA's management team,
with Director Tom Johnson stating, "We are thrilled to
hear that our employees are satisfied with their work at NASA.
We have a talented and dedicated team who work tirelessly
to achieve our goals, and it's fantastic to see that their
hard work is paying off."

The survey also revealed that the
Social Security Administration had the lowest satisfaction
rating, with only 45% of employees indicating they were
satisfied with their job. The government has pledged to
address the concerns raised by employees in the survey and
work towards improving job satisfaction across all departments.
"""

# Infer 5 topics
prompt7 = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long.

Format your response as a list of items separated by commas.

Text sample: '''{story}'''
"""
response7 = get_completion(prompt7)
print(response7)

response7.split(sep=',')

topic_list = [
    "nasa", "local government", "engineering",
    "employee satisfaction", "federal government"
]

# Make a news alert for certain topics
prompt8 = f"""
Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.\

List of topics: {", ".join(topic_list)}

Text sample: '''{story}'''
"""
response8 = get_completion(prompt8)
print(response8)

topic_dict = {
    i.split(': ')[0]: int(i.split(': ')[1]) for i in response8.split(sep='\n')
}
if topic_dict['nasa'] == 1:
    print("ALERT: New NASA story!")
