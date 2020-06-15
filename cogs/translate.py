import discord
from discord.ext import commands
from google.cloud import translate_v2 as translate
from google.api_core.exceptions import BadRequest
import os

translate_client = translate.Client()


class TranslateCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group("translate")
    async def translate(self, context):
        pass

    @translate.command("text", pass_context=True)
    async def text(self, context, *string):
        language = string[-1]
        string = " ".join(string[:-1])
        try:
            result = translate_client.translate(string, target_language=language)
        except BadRequest:
            await context.send(f"Could not find language: {language}")
            return
        translated = result['translatedText'].replace("&#39;", "'")
        output = f"Translating from {result['detectedSourceLanguage']} to {language}:\n*{translated}*"
        await context.send(output)

    @translate.command("detect", pass_context=True)
    async def detect(self, context, *text):
        string = " ".join(text)
        result = translate_client.detect_language(string)
        await context.send(f"I'm {round(result['confidence'] * 100)}% sure this is {result['language']}")

    @translate.command("languages", pass_context=True)
    async def languages(self, context):
        msg = ""
        result = translate_client.get_languages()
        for language in result["languages"]:
            print(language)
            msg += language["displayName"] + "(" + language["languageCode"] + ")"

def setup(client):
    client.add_cog(TranslateCog(client))
