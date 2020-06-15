from discord.ext import commands
import discord
import json
import urllib
import random


class IMBDCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bob_characters = {}
        with open("static/bob.txt", "r") as f:
            for line in f:
                self.bob_characters[line.split(":")[0]] = line.split(":")[1]
        self.bob_episodes = {}
        with open("static/bob2.txt", "r", encoding="utf-8") as f:
            for line in f:
                self.bob_episodes[line.split(":")[0]] = [line.split(":")[1],
                                                         line.split(":")[2],
                                                         line.split(":")[3].replace("\n", "")]

    @commands.command(pass_context=True, aliases=["IMDB", "ImDb", "Imdb"])
    async def imdb(self, context, type, *IMDBQuery):  # The type is 'imdb', the media query is everything after

        IMDBqueryplus = "+".join(IMDBQuery)
        response_raw = urllib.request.urlopen('http://www.omdbapi.com/?apikey='+ os.environ["OMDB"] +'&t=' + IMDBqueryplus + '&plot=full')
        response = json.loads(response_raw.read())
        if not type.lower() in ["poster", "plot", "synopsis", "actors", "cast", "ratings", "rating", "release", "released"]:
            await context.send("Please use one of the approved queries. Try this one-\n!imdb release moana")
            type = "release"
            response_raw = urllib.request.urlopen('http://www.omdbapi.com/?apikey='+ os.environ["OMDB"] +'&t=moana&plot=full')
            response = json.loads(response_raw.read())
        elif response["Response"] == 'False':
            await context.send("Sorry, that movie or show ain't a thing. Or maybe you cant spell")
            return

        if type.lower() == "poster":
            embed = discord.Embed(title=response["Title"] + " poster")
            embed.set_image(url=response["Poster"])
            await context.send("", embed=embed)
        elif type.lower() == "plot" or type.lower() == "synopsis":
            await context.send(f"Here is the plot for {response['Title']}-\n{response['Plot']}")
        elif type.lower() == "actors" or type.lower() == "cast":
            await context.send(f"Some actors from {response['Title']} included:\n{response['Actors']}")
        elif type.lower() == "rating" or type.lower() == "ratings":
            RawRatings = response["Ratings"]
            msg = ""
            for rating in RawRatings:
                msg = msg + rating["Source"] + ": " + rating["Value"] + "\n"
            await context.send(f"The ratings for {response['Title']} were: \n{msg}")
        elif type.lower() == "release" or type.lower() == "released":
            IMDBdate = response["Released"].split(" ")
            if IMDBdate[0][0] == "0":
                IMDBdate[0] = IMDBdate[0][1:]
            await context.send(f"{response['Title']} was released on the {IMDBdate[0]}th of {IMDBdate[1]}, {response['Year']}\nNow that is {response['Title']}tastic")

    @commands.group("bob", aliases=["BOB", "BoB", "Bob"])
    async def bob(self, context):
        pass

    @bob.command("random", aliases=["Random"])
    async def bob_random(self, context):
        choice = random.choice(list(self.bob_characters.items()))
        name = choice[0]
        episodes = choice[1].replace("\n", "")
        if episodes != "null":
            await context.send(f"Your random Band of Brothers character is {name}. He was the principal character in episode {episodes}")
        else:
            await context.send(f"Your random Band of Brothers character is {name}.")

    @bob.command("ep", aliases=["EP", "eP", "Ep", "Episode", "episode"])
    async def bob_episode(self, context, EpQuery):
        try:
            EpQuery = int(EpQuery)
        except ValueError:
            await context.send(f"Please represent your BoB episode request as a number")
            return
        if 11 > EpQuery > 0:
            await context.send(f"Band of Brothers episode {EpQuery} is titled '{self.bob_episodes.get(str(EpQuery))[0]}' and is directed by {self.bob_episodes.get(str(EpQuery))[1]}\nSynopsis --- {self.bob_episodes.get(str(EpQuery))[2]}")
        else:
            await context.send(f"BoB has ten episodes you uncultured swine")


def setup(client):
    client.add_cog(IMBDCog(client))
