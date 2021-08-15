#ODMyODY1ODk5MjY1NjU0Nzg0.YHqA0A.6aA4_yvYp9RBx5B2tN2iAb8kakg
#https://discord.com/api/oauth2/authorize?client_id=832865899265654784&permissions=8&scope=bot

from discord.ext import commands
from discord.ext import tasks
import discord

import json, os, asyncio, sys
import math, random
from datetime import datetime
from DiscordBot_Module import cari_image
from DiscordBot_Module import cari_barang

client = commands.Bot(command_prefix='!')

Operator_MTK = ["*", "+", "-"]

Soal_BahasaInggris = json.load(open("Json_Discordbot/bahasa_inggris.json"))
Soal_Fisika = json.load(open("Json_Discordbot/soal_fisika.json"))

Duel_Pelajaran = ["mtk", "bahasa_inggris", "fisika"]
Lomba_Duel_Pelajaran = ["mtk"]

Duel = {}
Lomba_Duel_Dict = {}

def Soal_MTK_Generator():
    x, y = random.randint(-10, 15), random.randint(-10, 15)
    operator = random.choice(Operator_MTK)

    hasil = eval(f'x {operator} y')

    return x, y, operator, hasil

def Soal_Fisika_Generator():
    Soal = random.choice(list(Soal_Fisika.keys()))

    yangDiformat = {}
    Nomor = {} #ini susah jelasinnya tapi, kayak gini kerjanya || Rumus program: b + (a * c), Nomor {a: 2, b: 7, c: 10} kita evalkan sesuai Rumus dan Nomor KITA GABUNG

    Jawaban_ = 0

    while Jawaban_ <= 0:
        for i in range(0, Soal.count('{}')):
            angka = random.randint(Soal_Fisika[Soal]["Minimal_Angka"], Soal_Fisika[Soal]["Maximum_Angka"])
            Nomor[chr(i+65).lower()] = angka #Dapatkan abjad dari nomor
            yangDiformat[i] = angka

        Jawaban_ = eval(Soal_Fisika[Soal]["Rumus_Program"], Nomor)

    if isinstance(Jawaban_, float):
        if Jawaban_.is_integer():
            Jawaban_ = int(Jawaban_)

    Soal_Formated = Soal.format(*yangDiformat.values())
    Soal_Fisika[Soal]["Jawaban"] = Jawaban_

    return Soal_Fisika, Soal, Soal_Formated

def Soal_BahasaInggris_Generator():
    Soal = random.choice(list(Soal_BahasaInggris.keys()))
    if Soal_BahasaInggris[Soal]["Sudah_Dipakai"] == True:
        while True:
            Soal = random.choice(list(Soal_BahasaInggris.keys()))
            if Soal_BahasaInggris[Soal]["Sudah_Dipakai"] == False:
                break

    Soal_BahasaInggris[Soal]["Sudah_Dipakai"] = True
    
    return Soal_BahasaInggris, Soal

def DapatkanSoalDuel(mata_pelajaran, member_id, ctx_id, LombaDuel=False):
    if mata_pelajaran == "mtk":
        x, y, operator, hasil = Soal_MTK_Generator()
        
        if not LombaDuel:
            for i in [member_id, ctx_id]:
                Duel[i]["hasil"] = hasil
        else:
            Lomba_Duel_Dict[member_id]["hasil"] = hasil

        return f"{x} {operator} {y} = ..."
    elif mata_pelajaran == "bahasa_inggris":
        soal_dict, soal_raw = Soal_BahasaInggris_Generator()
        soal_dict = soal_dict[soal_raw]
        
        if not LombaDuel:
            for i in [member_id, ctx_id]:
                Duel[i]["hasil"] = soal_dict['Jawaban']

        print("DUel " + Duel[i]["hasil"])
        print("soal_dict jawaban "+soal_dict["Jawaban"])
        return f"{soal_raw} \n A. {soal_dict['A']} \n B. {soal_dict['B']} \n C. {soal_dict['C']} \n D. {soal_dict['D']}"
    elif mata_pelajaran == "fisika":
        soal_dict, soal_raw, Soal = Soal_Fisika_Generator()
        soal_dict = soal_dict[soal_raw]

        if not LombaDuel:
            for i in [member_id, ctx_id]:
                Duel[i]["hasil"] = soal_dict["Jawaban"]

        return f"{Soal} \n | Rumus: {soal_dict['Rumus_Lengkap']} |"

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Group orang"))
    print(f"Bot sudah siap {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message=message)

    if message.author.id in Duel:
        jawaban_author = None

        if Duel[message.author.id]['mata_pelajaran'] == "mtk" or Duel[message.author.id]['mata_pelajaran'] == "fisika":
            if message.content.isdigit():
                jawaban_author = int(message.content)
            else:
                print(message.content)
        elif Duel[message.author.id]['mata_pelajaran'] == "bahasa_inggris":
            jawaban_author = str(message.content).upper()

        if Duel[message.author.id]["sudah_dijawab"] == False:
            print("hasil: " + str(Duel[message.author.id]["hasil"]))
            print("jawabanAuthor: "+str(jawaban_author))
            if Duel[message.author.id]["hasil"] == jawaban_author:
                for d in Duel:
                    Duel[d]['sudah_dijawab'] = True

                Duel[message.author.id]['point']+=1
                await message.channel.send(f"1 Point untuk {message.author.name}")
                
                asyncio.sleep(1)

                for i in Duel:
                    Duel[i]['Round'] += 1
                    Duel[i]['sudah_dijawab'] = True
                    await message.channel.send(f"{Duel[i]['nama']} Points: {Duel[i]['point']}")

                if Duel[message.author.id]['Round'] == 10:
                    pemenang = None
                    ind = None
                    mata_pelajaran = None

                    for i in Duel:
                        mata_pelajaran = Duel[i]['mata_pelajaran']
                        if ind is None:
                            ind = Duel[i]
                        else:
                            if ind['point'] > Duel[i]['point']: 
                                pemenang = ind['nama']
                            else:
                                pemenang = Duel[i]['nama']

                    if mata_pelajaran == "bahasa_inggris":
                        for i in Soal_BahasaInggris:
                            Soal_BahasaInggris[i]['Sudah_Dipakai'] = False
                    
                    await message.channel.send(f"Yang menang adalah {pemenang}")

                    for i in Duel:
                        del Duel[i]
                else:
                    mata_pelajaran = Duel[message.author.id]['mata_pelajaran']
                    Soal = DapatkanSoalDuel(mata_pelajaran, *Duel)

                    await message.channel.send(Soal)

                    for d in Duel:
                        Duel[d]['sudah_dijawab'] = False
        else:
            print(Duel[message.author.id]['hasil'])
    
    if message.author.id in Lomba_Duel_Dict:
        if Lomba_Duel_Dict[message.author.id]['boleh_main']:
            jawaban_author = None

            if Lomba_Duel_Dict[message.author.id]['mata_pelajaran'] == "mtk":
                jawaban_author = int(message.content)

            if jawaban_author == Lomba_Duel_Dict[message.author.id]["hasil"]:
                Lomba_Duel_Dict[message.author.id]['point'] += 1
                await message.channel.send("1+ point")

                Soal = DapatkanSoalDuel(Lomba_Duel_Dict[message.author.id]['mata_pelajaran'], member_id=message.author.id, ctx_id=None, LombaDuel=True)
                await message.channel.send(Soal)


@client.command()
async def duel(ctx, member: discord.Member, mata_pelajaran: str):
    mata_pelajaran = mata_pelajaran.lower()
    
    if ctx.author.id in Duel:
        await ctx.send("Kamu lagi duel")
        return

    if ctx.author.id == member.id:
        await ctx.send("Kamu gk bisa duel diri mu sendiri")
        return

    if member == client.user:
        await ctx.send("Kamu gk bisa duel sama bot")
        return
    
    if mata_pelajaran not in Duel_Pelajaran:
        await ctx.send(f"gk ada pelajarn {mata_pelajaran}")
        return

    await ctx.send(f"Menunggu {member.mention} untuk accept duelnya, Kalau mau accept duel type !accept_duel {ctx.author.mention}")

    for nama in [ctx.author, member]:
        Duel[nama.id] = {}
        Duel[nama.id]["yang_ngajak_duel"] = ctx.author
        Duel[nama.id]["mata_pelajaran"] = mata_pelajaran
        Duel[nama.id]["point"] = 0
        Duel[nama.id]["Round"] = 0
        Duel[nama.id]["nama"] = nama.name
        Duel[nama.id]["main"] = True
        Duel[nama.id]["sudah_dijawab"] = False

    Duel[member.id]["main"] = False

    await asyncio.sleep(30)

    if Duel[member.id]["main"] == False:
        for nama in [ctx.author.id, member.id]:
            del Duel[nama]

        await ctx.send(f"Time out {member.mention} tidak accept duelnya")

@client.command()
async def accept_duel(ctx, member: discord.Member):
    if member.id not in Duel:
        await ctx.send(f"{member.mention} tidak menantang kamu dari duel")
        return
    if member.id == ctx.author.id:
        await ctx.send(f"Tidak bisa accept duel dirisendiri")
        return
    if ctx.author.id == Duel[ctx.author.id]["yang_ngajak_duel"].id:
        await ctx.send(f"Yang accept duel itu harus yang kamu ajak")
        return

    Duel[ctx.author.id]["main"] = True
    mata_pelajaran = Duel[member.id]['mata_pelajaran']
    Soal = DapatkanSoalDuel(mata_pelajaran, member.id, ctx.author.id)

    print(Duel[ctx.author.id]["hasil"])

    await ctx.send(f"Duel antara {member.mention} dan {ctx.author.mention} dalam pelajaran {mata_pelajaran} siapa yang cepat mendapatkan 10 points dia yang menang, pertandingan akan dimulai dalam 3")
    await asyncio.sleep(2)
    await ctx.send("2")
    await asyncio.sleep(1)
    await ctx.send("1")
    await asyncio.sleep(1)
    await ctx.send(Soal)

@client.command()
async def cari_gambar(ctx, *, args):
    file_name = cari_image.run_image(args)
    
    if file_name is not None:
        msg = await ctx.send(file=discord.File(file_name))
        await msg.add_reaction("😏")

        if os.path.exists(file_name):
            os.remove(file_name)
    else:
        await ctx.send("Tidak ada gambar")
        return

@client.command()
async def CariHargaBarang(ctx, *, args):
    await ctx.send("Mohon ditunggu, ini lagi dicari lagian perlu beberapa detik")

    title, harga, link = cari_barang.run_caribarang(args)

    await ctx.send(f"Nama barang: {title} \n Harga: {harga} \n Link: {link}")

@client.command()
async def Lomba_duel(ctx, mata_pelajaran):
    if mata_pelajaran in Lomba_Duel_Pelajaran:
        data = json.load(open("Json_Discordbot/Lomba_Duel_Leaderboard.json"))

        Lomba_Duel_Dict[ctx.author.id] = {}
        Lomba_Duel_Dict[ctx.author.id]["point"] = 0
        Lomba_Duel_Dict[ctx.author.id]["mata_pelajaran"] = mata_pelajaran
        Lomba_Duel_Dict[ctx.author.id]["boleh_main"] = True

        await ctx.send("Dapatkan pointmu sebanyak mungkin dan dapatkan juara kesatu mu! Batas waktunya 2 Menit, Semoga beruntung!")        
        await asyncio.sleep(1)

        Soal = DapatkanSoalDuel(mata_pelajaran, member_id=ctx.author.id, ctx_id=None,LombaDuel=True)
        
        await ctx.send(Soal)

        await asyncio.sleep(60)
        await ctx.send("Waktu sisa 1 menit")

        await asyncio.sleep(60)
        Lomba_Duel_Dict[ctx.author.id]["boleh_main"] = False

        await ctx.send("Waktu habis!")

        #print(data.get(str(ctx.author.id)).get('point'))
        if data.get(str(ctx.author.id)) is not None:
            if data[str(ctx.author.id)]['point'] < Lomba_Duel_Dict[ctx.author.id]["point"]:
                await ctx.send(f"New HighSore! Kamu mempunyai {Lomba_Duel_Dict[ctx.author.id]['point']} poin, Selamat! Kalau mau lihat rankmu type !Leaderboard_LombaDuel")
                
                with open("Json_Discordbot/Lomba_Duel_Leaderboard.json", 'w') as filejson:
                    data[str(ctx.author.id)] = {}
                    data[str(ctx.author.id)]['name'] = ctx.author.mention
                    data[str(ctx.author.id)]['point'] = Lomba_Duel_Dict[ctx.author.id]["point"]
                    json.dump(data, filejson, indent=4)
            else:
                await ctx.send(f"Kamu mempunyai {Lomba_Duel_Dict[ctx.author.id]['point']} poin, Selamat!  Kalau mau lihat rankmu type !Leaderboard_LombaDuel")
        else:
            print("run 1")
            await ctx.send(f"New HighSore! Kamu mempunyai {Lomba_Duel_Dict[ctx.author.id]['point']} poin, Selamat! Kalau mau lihat rankmu type !Leaderboard_LombaDuel")
            with open("Json_Discordbot/Lomba_Duel_Leaderboard.json", 'w') as filejson:
                data[str(ctx.author.id)] = {}
                data[str(ctx.author.id)]['name'] = ctx.author.mention
                data[str(ctx.author.id)]['point'] = Lomba_Duel_Dict[ctx.author.id]["point"]
                json.dump(data, filejson, indent=4)

        del Lomba_Duel_Dict[ctx.author.id]
    else:
        await ctx.send(f"Tolong kasi mata pelajarannya... Yang ada {Lomba_Duel_Pelajaran}")
        return

@client.command()
async def Leaderboard_LombaDuel(ctx):
    toplist = []

    with open("Json_Discordbot/Lomba_Duel_Leaderboard.json",'r') as f:
        ind = 1
        data = json.load(f)
        for i in data:
            toplist.append(f"{data[i]['name']}: {data[i]['point']}")

    name = '\n'.join(toplist)
    embed = discord.Embed(title="Top global lomba duel", description=name)
    await ctx.send(embed=embed)

@Lomba_duel.error
async def lombaduel_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Tolong kasi mata pelajarannya... Yang ada {Lomba_Duel_Pelajaran}")

@duel.error
async def duel_error(ctx, error):
   if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Cara duel orang", description="!duel [nama orang] [mata pelajaran]")
        embed.add_field(name="Nama orang", value="Cari orang dengan mention", inline=False)
        embed.add_field(name="Mata pelajaran", value="yang ada: mtk", inline=False)
        await ctx.send(embed=embed)

client.run("ODMyODY1ODk5MjY1NjU0Nzg0.YHqA0A.6aA4_yvYp9RBx5B2tN2iAb8kakg")
