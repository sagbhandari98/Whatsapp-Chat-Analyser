import pandas as pd
import re
def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Strip square brackets from 'message_date' column and convert to datetime
    try:
        df['message_date'] = pd.to_datetime(df['message_date'].str.strip(), format='[%d/%m/%Y, %H:%M:%S]')
        df.rename(columns={'message_date': 'dates'}, inplace=True)
    except ValueError as e:
        print("ValueError:", e)

    df['dates'] = df['dates'].astype(str)

        # Remove brackets and comma from 'dates' column
    df['dates'] = df['dates'].str.replace(r'[\[\],]', '', regex=True)

        # Convert the strings back to datetime objects
    df['dates'] = pd.to_datetime(df['dates'])

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute

    return df



