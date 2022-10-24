import re
import pandas as pd

# assign csv files for cleansing use
df_alay = pd.read_csv(r'D:/Binar Data Science/simple_api1/datasets/new_kamusalay.csv', names=[
                      'Kata_alay', 'Kata_ganti'], encoding='latin')
df_stop = pd.read_csv(
    r'D:/Binar Data Science/simple_api1/datasets/stopwordbahasa.csv', names=['stopword'])


def remove_chars(text):
    # convert to string to be able to replace
    text = re.sub(r'[^a-zA-Z0-9]', ' ', str(text))
    text = text.lower()  # lowercase all text
    text = text.strip()  # strip trailing or leading characters
    text = re.sub('\\n', ' ', text)  # remove \n
    text = re.sub('user', ' ', text)  # remove user
    text = re.sub('https\S+', '', text)  # remove links and whitespaces
    text = re.sub('(rt) | (RT)', ' ', text)  # remove RTs
    text = re.sub('  +', ' ', text)  # remove space lebih
    text = re.sub('USER', ' ', text)  # remove the word user
    # remove hashtags, @, links
    text = ' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    text = re.sub('tweet', ' ', text)  # remove tweet
    text = re.sub('hs', ' ', text)  # remove hs
    text = re.sub('abusive', ' ', text)  # remove abusive
    text = re.sub('x[a-z0-9]{2}', ' ', text)  # remove emoticons
    text = re.sub(';', ' ', text)
    text = re.sub(':', ' ', text)
    return text


# assign dictionary variable to hold kata_alay and kata_ganti
alay_dict = dict(zip(df_alay['Kata_alay'], df_alay['Kata_ganti']))


def clean_alay(text):
    return ' '.join([alay_dict[alay] if alay in alay_dict else alay for alay in text.split(' ')])


def clean_stop(text):
    text = ' '.join(
        ['' if stop in df_stop.stopword.values else stop for stop in text.split(' ')])
    text = text.strip()  # strip trailing or leading characters
    text = re.sub('  +', ' ', text)  # remove space lebih
    return text


def full_clean(text):
    text = remove_chars(text)
    text = clean_alay(text)
    text = clean_stop(text)
    return text
