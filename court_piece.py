import random
import datetime

players={}  #{namegame:{player1(user id):{name_playe:,result_games;{win:[],lose:[], half_over:[], score: win+half_over}}},namegame:{player2(user id):{team:nameteam,score:}},...}
games={}   #{ Court_Piece:{team1:{level_game:[tashkil_team,entekhab_hokm,start_game] ,pairs:[[player1,player3],[player4,player2], cpl:cpl ,[hakem,raghib,yarhakem,yarraghib],hakem],player1:{status_player: ,rankhakem: ,created_date:,cart:[]},player2:{} , ...} }
Court_Piece_pool_player=[]
rank_Court_Piece=[14,13,12,11,10,9,8,7,6,5,4,3,2]
Court_Piece={'khest':[(14,'تک خشت') , (13,'پادشاه خشت'),(12,'بی بی خشت'),(11,'سرباز خشت'),(10,'ده خشت'),(9,'نه خشت'),(8,'هشت خشت'),(7,'هفت خشت'),(6,'شش خشت'),(5,'پنج خشت'),(4,'چهار خشت'),(3,'سه خشت'),(2,'دو خشت')]\
    ,'geshniz':[(14,'تک گشنیز') , (13,'پادشاه گشنیز'),(12,'بی بی گشنیز'),(11,'سرباز گشنیز'),(10,'ده گشنیز'),(9,'نه گشنیز'),(8,'هشت گشنیز'),(7,'هفت گشنیز'),(6,'شش گشنیز'),(5,'پنج گشنیز'),(4,'چهار گشنیز'),\
                (3,'سه گشنیز'),(2,'دو گشنیز')]\
    ,'del':[(14,'تک دل') , (13,'پادشاه دل'),(12,'بی بی دل'),(11,'سرباز دل'),(10,'ده دل'),(9,'نه دل'),(8,'هشت دل'),(7,'هفت دل'),(6,'شش دل'),(5,'پنج دل'),(4,'چهار دل'),(3,'سه دل'),(2,'دو دل')]\
    ,'pik':[(14,'تک پیک') , (13,'پادشاه پیک'),(12,'بی بی پیک'),(11,'سرباز پیک'),(10,'ده پیک'),(9,'نه پیک'),(8,'هشت پیک'),(7,'هفت پیک'),(6,'شش پیک'),(5,'پنج پیک'),(4,'چهار پیک'),(3,'سه پیک'),(2,'دو پیک')]}
a=[]
Court_Piece_list=[a.extend(v) for k , v in Court_Piece.items()]
Court_Piece_list=a
direction_Court_Piece={} #{team:[id1,id2,..],..}
name_game = 'Court_Piece'



if str(message.from_id) not in all_players:
    Court_Piece_pool_player.append(str(message.from_id))


    if len(Court_Piece_pool_player)==4:
        number_players=Court_Piece_pool_player.copy()
        Court_Piece_pool_player=[]
        # team_game = [k for k, v in games[name_game].items() if str(message.from_id) in games[name_game][k]]
        last_teams = [*games[name_game]]
        nem=len(number_players)//4 # creat number teams for players
        if len(last_teams)==0:
            c=1
        else:
            c = int(last_teams[-1].split(':')[1])
        empty_teams=[]
        for i in range(c,c+nem):
            games[name_game]['team:%s' % (i)] = {}
            games[name_game]['team:%s' % (i)]['created_date']  =str(datetime.datetime.utcnow())
            empty_teams.append('team:%s' % (i))


        for q in range(2):
            random.shuffle(number_players)
        pair=[]
        team_player=[0,2,1,3]
        b = 0
        findex=0
        for i in number_players:
            pair.append(i)
            team_player[team_player.index(findex)]=i # arrange player
            findex=findex+1
            games[name_game][empty_teams[0]][i] = {}
            if len(pair)==2:
                games[name_game][empty_teams[b]]['pairs'].append(pair)
                pair=[]
            if len(team_player)==4:
                games[name_game][empty_teams[b]]['pairs'].append(team_player)
                team_player=[0,2,1,3]
                b=b+1
                findex=0
        all_game_player()
        entekhab_hakem_and_direction(empty_teams)
        pakhsh_barye_hakem(empty_teams)
        pakhsh_cart_players(empty_teams)
        games[name_game][all_players[str(message.from_id)]]['level_game'] = 'start_game'

elif str(message.from_id) in all_players:

    if games[name_game][all_players[str(message.from_id)]]['level_game']=='start_game':

        # when game is finnishe must level_game is changed

    # hakem , direction
def entekhab_hakem_and_direction(empty_teams): # empty_teams(list) is one team or multi teams
    for i in empty_teams:
        partners = games[name_game][empty_teams[b]]['pairs'][2] # all players in a team
        r=0
        print(partners)
        while r[0]==14:
            for a in partners:
                r = random.choice(Court_Piece_list)
                print(a ,'------>',r)
                if r[0] == 14:
                    print('shoma hakem hastid',':',a)
                    games[name_game][empty_teams[b]]['pairs'].append(a) # choose hakem = ['pairs'][3]
                    team_pl=games[name_game][empty_teams[b]]['pairs'][2]
                    hakem_index = partners.index(a)
                    t=hakem_index-4
                    games[name_game][empty_teams[b]]['pairs'][2]=team_pl[t:] + team_pl[:t]
                    print(team_pl)

#پخش کارتها حاکم
def pakhsh_barye_hakem(empty_teams):  # empty_teams(list) is one team or multi teams
    f=0
    g=0
    p=5
    for i in empty_teams:
        partners = games[name_game][i]['pairs'][2]
        cpl = Court_Piece_list.copy()
        for i in range(2):
            random.shuffle(cpl)
        games[name_game][i]['cpl']=cpl
        for j in partners:
            games[name_game][i][j]['cart']=[]
        for k in cpl:
            print(partners[f],'----->',k)
            games[name_game][i][partners[f]]['cart'].append(k)
            g = g + 1
            cpl.remove(k)
            if g==4:  # give 5 cart for hakem
                print('entekhab hokm')
                games[name_game][i]['cpl'] = cpl



        # برای جهت اعداد 1 و 2 و 3 و 4 و انتخاب میکنیم و از 1 به سمت 4 حرکت میکنیم

        # انتخاب کارتها برای فرد
        # اول باید یار کشی کرد
        # دوم باید حاکم را مشخص کرد
        # سوم باید به حاکم اینلاین کیبورد بفرستم تا حکم انتخاب کنه
        # یه روشی باید پیدا کنم که بشه رده بندی کرد کارتها را
        # طرف وقتی از یه رنگ تموم میکنه باید بتونه از کارتهای دیگش استفاده کنه
        # جهت چرخش بازی باید مشخص بشه

        else:
        # start game


            # کلید بزارم اگه طرف نخواست از بازی انصراف بده و از بقیه عذخواهی کنه بابت رفتنش

def pakhsh_cart_players(empty_teams):  # empty_teams(list) is one team or multi teams
    f = 1
    g = 0
    p = 5
    cpl=games[name_game][i]['cpl']
    for k in cpl:
        if p == 4:
            print(partners[f], '----->', k)
            games[name_game][i][partners[f]]['cart'].append(k)
            g = g + 1
            if f == 3 and g == 3:  # give 4 cart for every player
                f = 0
            if g == 3:
                g = 0
                f = f + 1



        else:
            print(partners[f], '----->', k)
            games[name_game][i][partners[f]]['cart'].append(k)
            g = g + 1
            if f == 3 and g == 4:
                f = 0
                p = 4
            if g == 4:  # give 5 cart for every player
                print('entekhab hokm')
                g = 0
                f = f + 1

def all_game_player():
    # all_players = [[y for y,u in v.items()] for k , v in games[name_game].items()]
    # all_players=[j for i in all_players for j in i]
    all_players_teams = {l: k for k, v in games[name_game].items() for l in v}