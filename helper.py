from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re

import emoji
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch no. of media messages
    #num_media_messages = df[df['message'] == ' image omitted\n'].shape[0]
    # Fetch the number of media messages
    # Fetch the number of media messages
    num_media_messages = df[df['message'].str.contains('image omitted', na=False)].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user,df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != 'media omitted\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)



    wc= WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    temp['message']= temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc




def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != 'media omitted\n']  # Update this line to filter out media omitted messages

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    def extract_emojis(text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return ''.join(emoji_pattern.findall(text))

    # Example usage:
    emojis = []
    for message in df['message']:
        emojis.extend(extract_emojis(message))

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline["year"][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby("only_date").count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index="day_name", columns="period", values="message", aggfunc='count').fillna(0)

    return user_heatmap



