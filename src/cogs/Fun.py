import getpass
import os
import platform
import pwd
import re
import socket
import textwrap
import uuid
from datetime import datetime
from PIL import ImageGrab
from functools import partial
import discord
import psutil
import requests
import pyautogui
import cv2
import asyncio
import time
import random
import string
import webbrowser
from discord.ext import commands


class Fun(commands.Cog, description="System Information"):

    def __init__(self, client: commands.Bot):
        self.client = client


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
