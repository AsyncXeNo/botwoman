import discord
import json
import random
import string
import pickle
import copy

from discord.ext import commands
from utils.logger import Logger
from utils.math import Vector2


class RPG(commands.Cog):
	def __init__(self, client):
		self.logger = Logger("cog/rpg")
		self.client = client

		self.logger.log_neutral("Loaded rpg.")


def setup(client):
	client.add_cog(RPG(client))
