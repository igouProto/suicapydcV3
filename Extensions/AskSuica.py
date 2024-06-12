from ast import alias
import logging
from discord.ext import commands
from Replies.Strings import Messages

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


# logging
log = logging.getLogger(__name__)

"""
So I'm trying out Google Gemini to see if I can add some AI to the bot.
"""
# TODO: Chat session based on guild or user ID? We need 

class AskSuica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = bot.gemini_key

        # read system prompt from file
        with open("Assets/genaiSysPrompt.txt", "r") as file:
            self.system_prompt = file.read()

        # gemini configuration
        genai.configure(api_key=self.api_key)
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config = self.generation_config,
            safety_settings = self.safety_settings,
            # See https://ai.google.dev/gemini-api/docs/safety-settings
            system_instruction = self.system_prompt,
        )
        self.chat_session = self.model.start_chat()

    @commands.command(name="ask", aliases = ['a'])
    async def _ask(self, ctx, *, query):
        async with ctx.typing():
            resp = self.chat_session.send_message(query) # this blocks all other command requests, try async version?
            await ctx.send(resp.text)
            meta = resp.usage_metadata
            await ctx.send(f"`Prompt tokens: {meta.prompt_token_count}, Cand. tokens: {meta.candidates_token_count}, Total tokens: {meta.total_token_count}`")


async def setup(bot):
    await bot.add_cog(AskSuica(bot))
    log.info("Google Gemini Module loaded, key: {}".format(bot.gemini_key))
