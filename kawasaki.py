import tweepy
import time
import urllib.request
import os
from os import environ
from PIL import Image, ImageFilter, ImageDraw, ImageFont

consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
access_token = environ['ACCESS_KEY']
access_token_secret = environ ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def cancelamento(since_id):
    novo_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        novo_since_id = max(tweet.id, novo_since_id)
        if tweet.in_reply_to_status_id is not None:
            if ('cancela aqui' in tweet.text.lower()):
                tweetDoCancelado = api.get_status(tweet.in_reply_to_status_id)
                nomeDoCancelado = tweetDoCancelado.user.name
                url = tweetDoCancelado.user.profile_image_url.replace('normal', '400x400')
                fullpath = str(since_id)+'.jpg'
                urllib.request.urlretrieve(url, fullpath)
                cancelado = Image.open('cancelado.png')
                cancelado = cancelado.resize((400,400))
                manipula = Image.open(fullpath).convert('LA').convert('RGBA')
                manipula = manipula.filter(filter=ImageFilter.BLUR)
                manipula = Image.alpha_composite(manipula, cancelado)
                mensagem = nomeDoCancelado + ', teje canceladx'
                if ('por' in tweet.text.lower()):
                    motivo = tweet.text.lower().replace('@naooanjo cancela aqui', '')
                    arroba = tweetDoCancelado.user.screen_name.lower()
                    motivo = motivo.replace('@'+arroba, '')
                    mensagem += motivo
                    print(mensagem)
                    motivo = motivo.replace(' por ', '')
                    escrita = ImageDraw.Draw(manipula)
                    fonte = ImageFont.truetype('arial.ttf', size=28)
                    escrita.text((20,370), 'Motivo: '+motivo, fill=(255,0,0), font = fonte)
                manipula.save('upload.png')
                media = api.media_upload('upload.png').media_id_string
                media = str(media)
                api.update_status(mensagem, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata=True, media_ids = [media])
                os.remove('upload.png')
                os.remove(fullpath)
                print('replied to '+nomeDoCancelado)

    return novo_since_id

def main():
    since_id = 1259214359022063616
    while True:
        print('searching')
        since_id = cancelamento(since_id)
        print('waiting')
        time.sleep(60)

if __name__ == '__main__':
    main()
    
