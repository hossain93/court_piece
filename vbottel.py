import json
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import nest_asyncio
import requests
import datetime
import logging
import threading
import re
import zipfile
from bs4 import BeautifulSoup
TOKEN = '6419485590:AAGlyMYRR7NQJihSv0uZq270KEQ5_M1fND4'
# TOKEN='6925658239:AAGRpl68t7_uAY6iQdRUbu4DpdzVx6jagEk'
# proxy = 'http://localhost:10809/'
# bot = Bot(TOKEN, proxy=proxy)
bot = Bot(TOKEN)
dp = Dispatcher(bot)
try:
    propertis={'telegram_username':'','is_bot':None,'exdate':None,'stdate':None,'admin':'','user':'','text':''}
    profile_account = json.load(open('profile_account.json'))
    for k,v in propertis.items():
        for kk,vv in profile_account.items():
            if k not in vv:
                profile_account[kk][k]=v
except Exception as error:
    profile_account={}

try:
    propertislink={'ChatInviteLink1':'','ChatInviteLink2':'','daysallow':15,'users':[],'memberlimit':50,'date_product':None }
    InviteLink = json.load(open('InviteLink.json'))
except Exception as error:
    InviteLink={}

@dp.message_handler(commands=['start'])
async def registration(message: types.Message):
    global propertis
    global profile_account
    if str(message.from_id) not in profile_account:
        profile_account[str(message.from_id)]=propertis.copy()
        profile_account[str(message.from_id)]['telegram_username']=message.from_user['username']
        profile_account[str(message.from_id)]['is_bot']=message.from_user['is_bot']
        profile_account[str(message.from_id)]['exdate']=str((datetime.datetime.utcnow() + datetime.timedelta(days=5)))
        profile_account[str(message.from_id)]['stdate']=str(datetime.datetime.utcnow())
        json.dump(profile_account, open('profile_account.json', 'w'))
    await bot.send_message(message.from_id,"خوشحال هستیم که انتخاب شماییم. برای ادامه لطفا به کانالهای مورد نظر مراجعه کنید و از دنیای آزاد اینترنت لذت ببرید. فراموش نکنید که نیاز به حمایتهای مالی شما داریم"\
                          + "\r\n" + "شما به صورت رایگان میتوانید از این کانال به مدت 5 روز استفاده کنید")
    await bot.send_message(message.from_id,"راهنمایی راه اندازی نرم افزارهای مورد نظر:"+"\r\n"+"https://t.me/+wy98--az1K9iMThk"+"\r\n"+ "منبع کانفیگ ها:"+"\r\n"+"https://t.me/+y0ewNYXA3VpmOWU0")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['ایجاد لینک دعوت','مقدار باقی مانده اشتراک','صحبت با ادمین','خرید اشتراک','بررسی لینک ها','راهنمای ربات','بازی']
    keyboard.add(*buttons)
    await message.answer('یکی از گزینه های زیر را انتخاب کنید',reply_markup=keyboard)

@dp.chat_join_request_handler()
async def echo(message: types.Message):
    global profile_account
    global InviteLink
    linkurl = str(message.invite_link.invite_link)
    found_keys = {k:{p:h for p,h in v.items() if linkurl==h} for k, v in InviteLink.items() if linkurl in v.values()}
    if (str(message.from_user.id) not in InviteLink) and ( str(message.from_user.id) not in InviteLink[[*found_keys][0]]['users']):
        InviteLink[[*found_keys][0]]['memberlimit']=InviteLink[[*found_keys][0]]['memberlimit']-1
        InviteLink[[*found_keys][0]]['users'].append(str(message.from_user.id))
        if InviteLink[[*found_keys][0]]['memberlimit']<=0:
            try:
                await bot.unban_chat_member(chat_id=-1001563687795, user_id=int([*found_keys][0]),only_if_banned=True)

                profile_account[[*found_keys][0]]['exdate']=str((datetime.datetime.utcnow() + datetime.timedelta(days=180)))
                profile_account[[*found_keys][0]]['stdate']=str(datetime.datetime.utcnow())
                json.dump(profile_account, open('profile_account.json', 'w'))

                await bot.send_message(message.from_id , "حساب شما شارژ شد")
            except Exception as error:
                await bot.send_message(328660186 , error + '----'+'section join request')
            del InviteLink[[*found_keys][0]]
            await bot.send_message(message.from_id, "با تشکر از تلاش شما برای دعوت دوستان خودتان. شما هم اکنون ارتقا پیدا کردید. خوشحال میشیم حمایت خودتان را از ما ادامه دهید")
            await bot.send_message(328660186, "عضو @%s با آیدی %s ارتقا پیدا کرد با دعوت دوستان خودش"  % (message.from_user.username,message.from_user.id) )
        json.dump(InviteLink, open('InviteLink.json', 'w'))

    await bot.approve_chat_join_request(message.chat.id,message.from_user.id)
    await bot.send_message(message.from_user.id, "خوش آمدید به کانال")
    await bot.send_message(message.from_user.id, "https://t.me/+y0ewNYXA3VpmOWU0")
    await bot.send_message(message.from_user.id, "هر شبکه تلفن مانند ایرانسل یا همراه اول و یا خطوط تلفن ثابت باید یک وی پی ان مخصوص خودش را تهیه کرد و در این کانال کلی کانفیگ هست که در همه شبکه ها جواب میدن و فقط شما باید تست کنید")

@dp.message_handler(lambda message: message.text in ["بازی"])
async def registration(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['بازی حکم']
    keyboard.add(*buttons)
    await message.answer('یکی از گزینه های زیر را انتخاب کنید',reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["بازی حکم"] or profile_account[str(message.from_id)]['text'] in ["بازی حکم"])
async def registration(message: types.Message):
    global players
    global games


            # انتخاب کارتها برای فرد
            # اول باید یار کشی کرد
            # دوم باید حاکم را مشخص کرد
            # سوم باید به حاکم اینلاین کیبورد بفرستم تا حکم انتخاب کنه
            # یه روشی باید پیدا کنم که بشه رده بندی کرد کارتها را
            # طرف وقتی از یه رنگ تموم میکنه باید بتونه از کارتهای دیگش استفاده کنه
            # جهت چرخش بازی باید مشخص بشه

        else:
            # start game


    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['لغو بازی','انتخاب بازی دیگر']
    keyboard.add(*buttons)
    await message.answer('یکی از گزینه های زیر را انتخاب کنید',reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["ایجاد لینک دعوت"])
async def registration(message: types.Message):
    global InviteLink
    global propertislink
    limit=propertislink['memberlimit']/2
    daysallow=propertislink['daysallow']
    check=str(message.from_id) not in InviteLink
    chekk=True
    if message.from_id in InviteLink:
        da=datetime.datetime.fromisoformat(InviteLink[str(message.from_id)]['date_product'])
        if (datetime.datetime.utcnow()-da).days>daysallow:
            del InviteLink[str(message.from_id)]
            chekk=True
        else:
            chekk=False
    if chekk==True and check==True:
        datet=datetime.datetime.utcnow()
        ChatInviteLink1 = await bot.create_chat_invite_link(chat_id='-1001563687795', creates_join_request= True)
        ChatInviteLink2 = await bot.create_chat_invite_link(chat_id='-1001915653280', creates_join_request= True)

        InviteLink[str(message.from_id)]=propertislink.copy()
        InviteLink[str(message.from_id)]['date_product']=str(datet)
        InviteLink[str(message.from_id)]['ChatInviteLink1']=ChatInviteLink1["invite_link"]
        InviteLink[str(message.from_id)]['ChatInviteLink2']=ChatInviteLink2["invite_link"]
        json.dump(InviteLink, open('InviteLink.json', 'w'))
        await bot.send_message(message.from_id, 'لطفا برای مشاهده لینکها و انقضای لینکها روی دکمه های پایین بزنید')
        await bot.send_message(message.from_id, "تعداد افرادی که باید دعوت کنید %s نفر میباشد" % (limit))
        await bot.send_message(message.from_id, 'آیدی ربات:'+'\r\n'+'@Govpn405bot')
        await bot.send_message(message.from_id, "فراموش نکنید که این لینکها به مدت 15 روز اعتبار دارند.  بعد از تکمیل آنها به ادمین پیام دهید. برای اطلاع از فرآیند تعداد اعضایی که عضو شده با لینکهای شما لطفا دکمه  بررسی لینکها را انتخاب کنید.")

    else:
        await bot.send_message(message.from_id, "لینکهای شما هنوز منقضی نشده است و یا اینکه تعداد افراد مورد نظر با لینکهای خودتان دعوت نکردید")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['/start','انقضای لینک ها','مشاهده لینک ها','بررسی لینک ها']
    keyboard.add(*buttons)
    await message.answer('یکی از گزینه های زیر را انتخاب کنید',reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ['راهنمای ربات'])
async def registrationlink(message: types.Message):
    await bot.send_message(message.from_id,'با استارت ربات شما یک سری کلیدها در پایین ربات میبینید که توضیحات آنها به شرح زیر هست')
    await bot.send_message(message.from_id,'ایجاد لینک دعوت: برای حمایت از کانال و یا گرفتن اشتراک کانال کانفیگها روی این دکمه بزنید')
    await bot.send_message(message.from_id,'بررسی لینک ها: برای اینکه اطلاعات کسب کنید از لینکهایی که ساختید و تعداد اعضایی که با آنها دعوت کردید')

@dp.message_handler(lambda message: message.text in ['انقضای لینک ها','مشاهده لینک ها'])
async def registrationlink(message: types.Message):
    global InviteLink
    if str(message.from_id) in InviteLink:
        if message.text=='مشاهده لینک ها':
            await bot.send_message(message.from_id, 'کانال کانفیگها:'+"\r\n"+InviteLink[str(message.from_id)]['ChatInviteLink1']+\
                                   "\r\n"+'کانال عمومی:'+"\r\n"+InviteLink[str(message.from_id)]['ChatInviteLink2'])
        if message.text=='انقضای لینک ها':
            da=datetime.datetime.fromisoformat(InviteLink[str(message.from_id)]['date_product'])
            day=(datetime.datetime.utcnow()-da).days
            mandeh=InviteLink[str(message.from_id)]['daysallow']-day
            if mandeh>0:
                await bot.send_message(message.from_id,'شما هنوز %s روز اعتبار دارید برای لینکها' % (mandeh))

            if mandeh<0:
                await bot.send_message(message.from_id,'لینکهای شما منقضی شده')

    else:
         await bot.send_message(message.from_id,'شما لینکی ندارید')

@dp.message_handler(lambda message: message.text in ['hossain','Hossain'])
async def registration(message: types.Message):
    if message.from_user.id in [328660186, 91652281]:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['banex',"userall",'giveconfigs','help','/start',\
                  'ایجاد لینک دعوت','مقدار باقی مانده اشتراک','صحبت با ادمین','خرید اشتراک','بررسی لینک ها']
        keyboard.add(*buttons)
        await message.answer('یکی از گزینه های زیر را انتخاب کنید',reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ['برگشت'])
async def registration(message: types.Message):
    global profile_account
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['ایجاد لینک دعوت','مقدار باقی مانده اشتراک','صحبت با ادمین','خرید اشتراک','بررسی لینک ها','راهنمای ربات']
    keyboard.add(*buttons)
    await message.answer('فعلا',reply_markup=keyboard)
    if profile_account[str(message.from_id)]['text']=='صحبت با ادمین':
        profile_account[str(message.from_id)]['text']=''
    json.dump(profile_account, open('profile_account.json', 'w'))

@dp.errors_handler()
async def global_error_handler(update, exception):
    await bot.send_message(328660186, exception)

@dp.message_handler(content_types=['document'])
async def photo_handler(message: types.Message):
    if profile_account[str(message.from_id)]['text']=='صحبت با ادمین':
        admins=[328660186, 91652281]
        for i in admins:
            await bot.send_document(str(i),document=message.document.file_id)
            await bot.send_message(str(i),str(message.from_user.id)+"\r\n"+'@'+str(message.from_user.username))
@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message, allowed_updates=None):

    if profile_account[str(message.from_id)]['text']=='صحبت با ادمین':
        admins=[328660186, 91652281]
        for i in admins:
            await bot.send_photo(str(i),photo=message.photo[0].file_id)
            await bot.send_message(str(i),str(message.from_user.id)+"\r\n"+'@'+str(message.from_user.username))

@dp.message_handler(regexp='[\w|\W]')
async def savefilters(message: types.update):
    global InviteLink
    global msgs
    global profile_account
    id_user="328660186" #'91652281'HS

    if message.text=="userall" and (message.from_user.id in [328660186, 91652281]):
        await bot.send_message(message.from_id, "start")
        zip = zipfile.ZipFile("profile_account.zip", "w", zipfile.ZIP_DEFLATED)
        zip.write('profile_account.json')
        zip.close()
        profile_ac=open('profile_account.zip','rb')
        await bot.send_document(message.from_id, document=profile_ac)

        zip = zipfile.ZipFile("InviteLink.zip", "w", zipfile.ZIP_DEFLATED)
        zip.write('InviteLink.json')
        zip.close()
        InviteL=open('InviteLink.zip','rb')
        await bot.send_document(message.from_id, document=InviteL)
        await bot.send_message(message.from_id, "finish")
    # برای اعضایی که با لینک وارد عضو گیری وارد میشن
    elif message.text in InviteLink:

        if str(message.from_id) not in profile_account:
            InviteLink[str(message.text)]['users'].append(str(message.from_id))
            await bot.send_message(message.from_id, "با تشکر از انتخاب و حمایت شما هدف ما ایجاد بستری برای دسترسی به اینترنت آزاد هست. هم در زمینه آموزش و هم در زمینه ارائه سیستم")
            await bot.send_message(message.from_id, "کانال کانفیگ ها:")
            await bot.send_message(message.from_id, InviteLink[str(message.text)]['ChatInviteLink2'])
            await bot.send_message(message.from_id, "کانال عمومی:")
            await bot.send_message(message.from_id, InviteLink[str(message.text)]['ChatInviteLink2'])

        else:
            await bot.send_message(message.from_id, "شما قبلا تایید شدید")

    elif message.text=='بررسی لینک ها':
        mem=InviteLink[str(message.from_id)]['memberlimit']
        if round(mem/2)<1:
            mem=1
        else:
            mem=round(mem/2)
        InviteLink[str(message.from_id)]['memberlimit']=mem
        await bot.send_message(message.from_id , " %s نفر دیگر عضو کنید تا بتوانید اشتراک تهیه کنید" % (mem))


    elif message.text=='banex' and (message.from_user.id in [328660186, 91652281]):
        await bot.send_message(message.from_id, "start")
        for i in profile_account:
            day=(datetime.datetime.fromisoformat(profile_account[i]['exdate'])\
                    -datetime.datetime.fromisoformat(profile_account[i]['stdate'])).days
            if day==1 or day==2:
                await bot.send_message(message.from_id, "از اشتراک شما فقط %s روز مانده. برای تمدید اشتراک اقدام کنید لطفا" % (day))
                continue
            if datetime.datetime.fromisoformat(profile_account[i]['exdate'])<datetime.datetime.utcnow():
                if i=='328660186':
                    continue
                try:
                    await bot.ban_chat_member(chat_id=-1001563687795, user_id=int(i))
                    await bot.send_message(i, "با عرض پوزش برای اینکه در کانال کانفیگ ها در ادامه حضور داشته باشید لطفا یا حق اشتراک پرداخت کنید یا با ایجاد لینک مخصوص خودتان از طریق منو زیر و دعوت 25 نفر، دوباره وارد کانال شوید. ")
                except Exception as error:
                    await bot.send_message(message.from_id, "خطا داد")



        for i in InviteLink:

            da=datetime.datetime.fromisoformat(InviteLink[str(i)]['date_product'])
            if str(datetime.datetime.utcnow()-da).split(' ')[0]>InviteLink[str(i)]['daysallow']:
                del InviteLink[message.text]
        json.dump(InviteLink, open('InviteLink.json', 'w'))

        await bot.send_message(message.from_id, "finish")

    elif message.text=='صحبت با ادمین' or (profile_account[str(message.from_id)]['text']=='صحبت با ادمین'):
        if message.text=='صحبت با ادمین':
            profile_account[str(message.from_id)]['text']='صحبت با ادمین'
            json.dump(profile_account, open('profile_account.json', 'w'))
            await bot.send_message(message.from_id,"لطفا پیام خود را به صورت کامل نوشته و ارسال کنید همینجا.")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ['برگشت']
            keyboard.add(*buttons)
            await message.answer('برای خروج گزینه برگشت را بزنید',reply_markup=keyboard)
        else:
            admins=[328660186, 91652281]
            for i in admins:
                await bot.send_message(str(i),message.text+"\r\n"+'@'+str(message.from_user.username)+"\r\n"+'<code>%s</code>' % (str(message.from_id)), parse_mode="HTML" )

    elif message.text=='خرید اشتراک':
        await bot.send_message(message.from_id,"5859-8311-4502-5762" + "\r\n"+"\r\n" + "لطفا مبلغ مورد نظر را به این شماره کارت واریز کنید و به ادمین فیش واریزی را بفرستید")
        await bot.send_message(message.from_id, "یا با فشردن دکمه ایجاد لینک دعوت  به تعداد 25 نفر به کانالهای ما دعوت کنید تا اشتراک رایگان دریافت کنید")
        await bot.send_message(message.from_id, 'بعد از تهیه شرایط لازم برای اشتراک لطفا گزینه صحبت با ادمین را بزنید و به ادمین فیش واریزی را ارسال کنید')
        await bot.send_message((328660186), message.from_user)

    elif message.text.split(":")[0]=="user" and  (message.from_user.id in [328660186, 91652281]): #"user:id"
        await bot.send_message(message.from_id, "start")
        iduser=message.text.split(":")[1]

        try:
            await bot.unban_chat_member(chat_id=-1001563687795, user_id=int(iduser),only_if_banned=True)

            profile_account[str(iduser)]['exdate']=str((datetime.datetime.utcnow() + datetime.timedelta(days=180)))
            profile_account[str(iduser)]['stdate']=str(datetime.datetime.utcnow())
            json.dump(profile_account, open('profile_account.json', 'w'))
            await bot.send_message(iduser,"کانال کانفیگها: "+"\r\n"+"https://t.me/+y0ewNYXA3VpmOWU0"+"\r\n"+"\r\n"+"با تشکر از خرید شما")
            await bot.send_message(message.from_id, "finish")
        except Exception as error:
            await bot.send_message(message.from_id, "گاگول درست بنویس")

    elif message.text=='مقدار باقی مانده اشتراک':
        day=(datetime.datetime.fromisoformat(profile_account[str(message.from_id)]['exdate'])\
                -datetime.datetime.fromisoformat(profile_account[str(message.from_id)]['stdate'])).days
        await bot.send_message(message.from_id, "%s روز از اشتراک شما باقی مانده" % (day))

    elif message.text=='giveconfigs' and (message.from_user.id in [328660186, 91652281]):
        await bot.send_message(message.from_id, "start")
        threads=[]
        try:
            thread=threading.Thread(target=search())
            thread.start()
            threads.append(thread)
            for thread in threads:
                thread.join()
            await bot.send_message('-1001563687795',"کانفیگ های جدید در تاریخ "+ str(datetime.datetime.utcnow()))
            for m in msgs:
                await bot.send_message('-1001563687795','<code>%s</code>' % m, parse_mode="HTML" )
            await bot.send_message(message.from_id, "finish")
        except Exception as error:

            await bot.send_message(message.from_id, "دوباره بفرست"+"\r\n"+" طول پیام:"+"\r\n"+len(m))

    elif message.text=='help' and (message.from_user.id in [328660186, 91652281]):
        await bot.send_message(message.from_id,\
                               'giveconfig  , userall  ,  user:iduser ,  banex  ,  speak:... , speak:userid:..., id:text (or block)')

    elif message.text.split(":")[0]=="speak" and (message.from_user.id in [328660186, 91652281]):
        await bot.send_message(message.from_id, "start")
        if len(message.text.split(':'))==2:
            for i in profile_account:
                await bot.send_message(int(i),message.text.split(":")[1] )
        elif len(message.text.split(':'))==3:
            await bot.send_message(int(i),message.text.split(":")[1] )
        await bot.send_message(int(message.text.split(":")[1]), message.text.split(":")[3])
        await bot.send_message(message.from_id, "finish")

    elif (message.from_id in [328660186, 91652281]) and ((message.text.split(":")[0]).isdigit()):
        await bot.send_message(message.from_id, "start")
        #profile_account['admin'] for block admins and speak users
        # this section is for speak with user from admins
        try:
            if profile_account[str(message.from_id)]['admin']!='bl':
                await bot.send_message(int(message.text.split(":")[0]), message.text.split(":")[1])
                await bot.send_message(328660186, message.text.split(":")[0]+':'+\
                                       message.text.split(":")[1])
            if (message.text.split(":")[1]=='bl' or message.text.split(":")[1]=='Bl') and ((message.from_id in [328660186, 91652281])):
                profile_account[message.text.split(":")[0]]['admin']='bl'

            if (message.text.split(":")[1]=='rem' or message.text.split(":")[1]=='Rem') and ((message.from_id in [328660186, 91652281])):
                profile_account[message.text.split(":")[0]]['admin']=''
            json.dump(profile_account, open('profile_account.json', 'w'))
            await bot.send_message(message.from_id, "finish")
        except Exception as error:
            await bot.send_message(message.from_id, error)

msgs=[]
def search():
    global msgs
    url=["https://github.com/mianfeifq/share#%E6%9C%80%E6%96%B0%E8%8A%82%E7%82%B9",\
        "https://github.com/freefq/free","https://github.com/iwxf/free-v2ray"]
    configs=""
    for j in url:
        try:
            response = requests.get(j).text
            soup = BeautifulSoup(response, 'html.parser')
            link =soup.select_one('div[class*="snippet-clipboard-content notranslate position-relative overflow-auto"]').get_text(strip=True)
            configs=configs+link
        except Exception as error:
            bot.send_message(328660186,"مشکل در لینک زیر ایجاد شده یا لینک جوابگو نیست:"+"\r\n"+j)
        configs=configs.replace('telegram', '')
        configs=configs.replace('@', '')
        configs=configs.replace('github.com', '')

    con=['vmess://','trojan://','vless://']
    listco=[]
    for i in con:
        guess = i
        pattern = re.compile(guess)
        r = pattern.search(configs)
#         if not r: #print("(-1, -1)",i)

        while r:
            listco.append(r.start())
            r = pattern.search(configs,r.start() + 1)
    listco.sort()

    parts = [configs[i:j] for i,j in zip(listco, listco[1:]+[None])]

    msgs=[]
    msg=''
    for i in parts:
        if len(msg)+len(i)>4096:
            msgs.append(msg)
            msg=''
        elif parts.index(i)-1==len(parts):
            msg=msg + i
            msgs.append(msg)
        msg=msg + i

if __name__ == '__main__':
    # nest_asyncio.apply()
    executor.start_polling(dp,allowed_updates=['message','edited_message','channel_post','edited_channel_post','inline_query','chosen_inline_result','callback_query','shipping_query','pre_checkout_query','poll','poll_answer','my_chat_member','chat_member','chat_join_request'])