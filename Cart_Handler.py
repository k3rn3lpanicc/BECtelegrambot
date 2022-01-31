from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def Sakhteman_CartCreate(person_name , ozviat_type , reshte , code_ozviat,chat_id,file_name):
    img = Image.open("sakhteman.jpg")
    img2 = Image.open("prof_pic+"+str(chat_id)+".jpg")
    img2 = img2.resize((150,205))
    img.paste(img2,(90,56))
    I1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('BNAZANB.ttf', 30 , encoding = 'utf-8')
    text = person_name
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((825-(width), 258), bidi_text, font=myFont, fill =(0, 0, 0))
    text = ozviat_type
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((758-(width), 373), bidi_text, font=myFont, fill =(0, 0, 0))
    text = reshte
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((840-(width), 483), bidi_text, font=myFont, fill =(0, 0, 0))
    text = code_ozviat
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((230-(width), 484), bidi_text, font=myFont, fill =(0, 0, 0))    
    img.save(file_name)
def Omran_CartCreate(person_name,semat , reshte , code_ozviat,chat_id,file_name):
    img = Image.open("omran.jpg")
    img2 = Image.open("prof_pic+" + str(chat_id) + ".jpg")
    img2 = img2.resize((150, 205))
    img.paste(img2, (90, 56))
    I1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('BNAZANB.ttf', 30 , encoding = 'utf-8')
    text = person_name
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((825-(width), 205), bidi_text, font=myFont, fill =(0, 0, 0))
    text = semat
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((830-(width), 294), bidi_text, font=myFont, fill =(0, 0, 0))
    text = reshte
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((830-(width), 390), bidi_text, font=myFont, fill =(0, 0, 0))
    text = code_ozviat
    reshaped_txt = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_txt)
    width = myFont.getbbox(text)[2]
    I1.text((710-(width), 486), bidi_text, font=myFont, fill =(0, 0, 0))
    img.save(file_name)
    
