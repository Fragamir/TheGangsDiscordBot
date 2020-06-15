import discord
from discord.ext import commands
import re
import urllib.request
from bs4 import BeautifulSoup


class MusicCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lyrics(self, context, *rest):
        input = " ".join(rest)
        # we do not want the bot to reply to itself
        if context.message.author == self.client.user:
            return


        msg = 'Here are the lyrics {0.author.mention}'.format(context.message)
        await context.send(msg)

        statement = input.lower()
        statement = statement.replace('?', '')
        statement = statement.split('-', 1)
        # statement = statement.replace("?bjork", "")
        if len(statement) > 1:
            print("searching songs by", statement[0], "called", statement[1])
            song_lyrics = self.get_lyrics(statement[0], statement[1])
            lyric_split = song_lyrics.splitlines()
            line_count = 0
            count = 1
            linegroup = []
            big_linegroup = []

            for line in lyric_split:
                if not line:
                    count += 1
                    line = '**Verse ' + str(count) + '**'
                linegroup.append(line)
                if len(linegroup) == 32:
                    big_linegroup.append(linegroup)
                    linegroup = []
                line_count += 1

            if linegroup:
                big_linegroup.append(linegroup)

            for lines in big_linegroup:
                msg = '\n'.join(lines)
                await context.send(msg)
        else:
            await context.send("fuck you the syntax is: ?artist - song")

    def get_lyrics(self, artist, song_title):
        artist = artist.lower()
        song_title = song_title.lower()
        # remove all except alphanumeric characters from artist and song_title
        artist = re.sub('[^A-Za-z0-9]+', "", artist)
        song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
        if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
            artist = artist[3:]
        url = "http://azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"

        try:
            content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(content, 'html.parser')
            lyrics = str(soup)
            # lyrics lies between up_partition and down_partition
            up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
            down_partition = '<!-- MxM banner -->'
            lyrics = lyrics.split(up_partition)[1]
            lyrics = lyrics.split(down_partition)[0]
            lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('</div>', '').replace('<br/>', '').replace(
                '<i>', '').replace('</i>', '').replace('[', '').replace(']', '').strip()
            return lyrics
        except Exception as e:
            return "Exception occurred \n" + str(e)
