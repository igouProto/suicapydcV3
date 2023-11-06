import datetime
import json
import logging
import random
from discord.ext import commands

log = logging.getLogger(__name__)

class FortuneResult:
    def __init__(self, lucky_number, lucky_color, gacha_index, charge_index, determination, direction, fortune, serial_number):
        self.lucky_number = lucky_number
        self.lucky_color = lucky_color
        self.gacha_index = gacha_index
        self.charge_index = charge_index
        self.determination = determination
        self.direction = direction
        self.fortune = fortune
        self.serial_number = serial_number

class Generator:
    def __init__(self):
        # load configuration from Assets/omikuji.json
        try:
            with open("Assets/omikuji.json", "r") as source:
                self.config = json.load(source)
                log.info("Omikuji configuration loaded from Assets/omikuji.json")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # if omikuji.json is not found, treat it as a fresh setup
            log.error(
                "Failed to load omikuji.json: {}".format(e)
            )

        self.weights = self.config["weights"]
        self.fortunes = self.config["fortunes"]
        self.colors = self.config["colors"]
        self.determinations = self.config["determinations"]
        self.directions = self.config["directions"]

    def choose_luck(self):
        """
        Chooses a random luck value based on the weights in the configuration.
        """
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        luck = random.choices(numbers, weights=self.weights, k=1)[0]
        return luck
    
    def generate(self, id, force=False):
        """
        Generates a fortune for the given user. Using the current date plus the user's ID as the seed.
        """
        time = datetime.datetime.now()
        seed = time.year * 10000 + time.month * 100 + time.day + id

        if force:
            seed += (time.second + time.microsecond)

        random.seed(seed)
        
        # draw the results
        luck = self.choose_luck()

        lucky_number = random.randint(1, 500)
        lucky_color = random.choice(self.colors)
        gacha_index = random.randint(0, 10)
        charge_index = random.randint(0, 10)
        determination = random.choice(self.determinations)
        direction = random.choice(self.directions)
        fortune = self.fortunes[luck]

        # show the seed just for fun
        serial_number = f"{seed}"

        # wrap it up
        result = FortuneResult(lucky_number, lucky_color, gacha_index, charge_index, determination, direction, fortune, serial_number)

        return result
