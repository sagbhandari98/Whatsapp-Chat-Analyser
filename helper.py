from urlextract import URLExtract
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



