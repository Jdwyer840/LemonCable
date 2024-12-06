import random


class NameGenerator:

    def __init__(self):
        pass

    adjectives = ["Thunderous", "Electric", "Wild", "Dark", "Loud", "Majestic",
        "Furious",  "Broken", "Eternal", "Lonely",
        "Endless", "Frozen", "Rebellious", "Shadowy", "Glorious",
        "Radiant", "Wicked", "Silent", "Hidden",
        "Fiery", "Vicious", "Crimson", "Mystic", "Golden",
        "Twisted",  "Silver", "Fierce", "Ghostly", "Sacred",
        "Savage", "Divine", "Fallen",  "Distant", "Forgotten",
         "Grim", "Restless", "Chained", "Bright",
        "Starry", "Hollow", "Luminous", "Sweaty", "Moist", "Salty", "Hairy", "Fluffy", "Greasy", "Sticky",
        "Wobbly", "Sassy", "Cranky", "Tipsy", "Cheeky", "Shady", "Stinky",
        "Chunky", "Spicy", "Awkward", "Goofy", "Clumsy", "Snarky",
        "Juicy", "Grumpy", "Quirky", "Randy", "Sketchy", "Funky",
        "Saucy", "Zesty", "Floppy", "Rough", "Smelly", "Thirsty",
        "Dirty", "Lazy", "Rowdy", "Sloppy", "Petty", "Frisky", "Gassy",
        "Loopy", "Snuggly", "Wacky", "Droopy", "Kinky", "Spunky",
        "Raunchy", "Slippery", "Shifty", "Grimy", "Soggy", "Chubby",
        "Trashy", "Whiny", "Freakish", "Bitchish", "Sluts", "Psychotic", "Busted"]
    nouns = ["Storm", "Heart", "Soul", "Fire", "Dream", "Night", "Shadow",
        "Rebel", "Phoenix", "Chaos", "Flame", "Light", "Rain", "Thunder",
        "Horizon", "Ashes", "Infinity", "Sky", "Wind", "Silence", "Waves",
        "Tide", "Destiny", "Moon", "Raven", "Eclipse", "Chasm", "Edge", "Sawtooth Tiger",
        "Glory", "Fate", "Spirit", "Wilderness", "Forest", "Ember",
        "Mystery", "Serpent", "Wraith", "Vision", "Beacon", "Canyon",
        "Bliss", "Desire", "Ruin", "Vortex", "Pulse", "Legend", "Vow",
        "Revenge", "Echo", "Trail", "Valley", "Courage", "Crown",
        "Crystal", "Light", "Noodle", "Beefcake", "Dumpster", "Pickle", "Sausage", "Meatball",
        "Unicorn", "Taco", "Pancake", "Burrito", "Bologna", "Banana",
        "Wiener", "Crab", "Muffin", "Monkey", "Goose", "Eggplant",
        "Troublemaker", "Sneeze", "Potato", "Llama", "Pimple", "Booty",
        "Donkey", "Cabbage", "Melon", "Wiggle", "Giraffe", "Banana",
        "Kumquat", "Squid", "Sloth", "Meatloaf", "Hamster", "Armpit",
        "Butt", "Fart", "Toaster", "Belly", "Warthog", "Puppy",
        "Weasel", "Badger", "Cheeseball", "Biscuit", "Piglet", "Nugget",
        "Pancake", "Blubber", "Blobfish", "Squishy", "Jellybean", "Cactus", "Cream", "Beefcake", "Dumpster", "Pickle", "Sausage", "Meatball",
        "Unicorn", "Taco", "Pancake", "Burrito", "Bologna",
        "Banana", "Wiener", "Crab", "Muffin", "Monkey",
        "Goose", "Eggplant", "Troublemaker", "Sneeze", "Potato",
        "Llama", "Pimple", "Booty", "Donkey", "Cabbage",
        "Melon", "Wiggle", "Giraffe", "Kumquat", "Squid",
        "Sloth", "Meatloaf", "Hamster", "Armpit", "Butt",
        "Fart", "Toaster", "Belly", "Warthog", "Puppy",
        "Weasel", "Badger", "Cheeseball", "Biscuit", "Piglet",
        "Nugget", "Blubber", "Blobfish", "Squishy", "Jellybean",
        "Cactus", "Cream", "Noodle", "Booger", "Gnome",
        "Spatula", "Cheesecake", "Fluffball", "Clown", "Dingus",
        "Wombat", "Dodo", "Plankton", "Shrub", "Cupcake",
        "Gobbler", "Sandwich", "Mug", "Bucket", "Splat",
        "Bunny", "Wigglebutt", "Doorknob", "Gargoyle", "Moth",
        "Pogo Stick", "Spork", "Peanut", "Cucumber", "Fuzzball",
        "Dingleberry", "Zebra", "Snail", "Slime", "Bacon",
        "Dumpling", "Lobster", "Bubbles", "Puddle", "Marshmallow",
        "Turd", "Popsicle", "Flapjack", "Hedgehog", "Squirrel",
        "Squirt", "Toothpick", "Sardine", "Sock", "Mittens",
        "Walrus", "Penguin", "Peacock", "Wigwam", "Cork",
        "Bug", "Whisker", "Snout", "Ostrich", "Puffin"]
    verbs = [
        "Burning", "Rising", "Falling", "Crashing", "Breaking", "Soaring",
        "Fading", "Running", "Screaming", "Dancing", "Dreaming", "Hunting",
        "Chasing", "Wandering", "Drifting", "Flying", "Dying", "Living",
        "Howling", "Shouting", "Crying", "Hiding", "Exploding", "Collapsing",
        "Searching", "Roaring", "Shattering", "Breathing", "Yearning",
        "Raging", "Melting", "Shining", "Blazing", "Echoing", "Trembling",
        "Flowing", "Fighting", "Piercing", "Binding", "Forging", "Surrendering",
        "Lurking", "Marching", "Drowning", "Chanting", "Ascending", "Diving",
        "Grieving", "Stirring", "Hovering", "Unfolding", "Gliding", "Surging", "Farting", "Sniffing", "Drooling", "Burping", "Squishing",
        "Wiggling", "Flopping", "Snorting", "Slapping", "Humping", "Fucking", "Shitting",
        "Nibbling", "Tickling", "Whining", "Grunting", "Lurking",
        "Peeing", "Moaning", "Spitting", "Chomping", "Scooting",
        "Licking", "Scratching", "Squeaking", "Smacking", "Gargling",
        "Pranking", "Pouting", "Flailing", "Scooping", "Slurping",
        "Twerking", "Hiding", "Shaking", "Stumbling", "Coughing",
        "Yawning", "Poking", "Stinking", "Barking", "Bark", "Drooping",
        "Quacking", "Biting", "Scrunching", "Plopping", "Snuggling",
        "Hopping", "Rolling", "Fumbling", "Stretching", "Dancing",
        "Squirming", "Tumbling", "Cough", "Laughs", "Burn", "Rise", "Fall", "Crash", "Break", "Soar", "Fade", "Run",
        "Scream", "Dance", "Dream", "Hunt", "Chase", "Wander", "Drift",
        "Fly", "Die", "Live", "Howl", "Shout", "Cry", "Explode", "Collapse",
        "Search", "Roar", "Shatter", "Breathe", "Yearn", "Rage", "Melt",
        "Shine", "Blaze", "Echo", "Tremble", "Flow", "Fight", "Pierce",
        "Bind", "Forge", "Surrender", "Lurk", "March", "Drown", "Chant",
        "Ascend", "Dive", "Grieve", "Stir", "Hover", "Unfold", "Glide",
        "Surge", "Fart", "Sniff", "Drool", "Burp", "Squish", "Wiggle",
        "Flop", "Snort", "Slap", "Hump", "Fuck", "Shit", "Nibble", "Tickle",
        "Whine", "Grunt", "Pee", "Moan", "Spit", "Chomp", "Scoot", "Lick",
        "Scratch", "Squeak", "Smack", "Gargle", "Prank", "Pout", "Flail",
        "Scoop", "Slurp", "Twerk", "Hide", "Shake", "Stumble", "Cough",
        "Laugh", "Bark", "Droop", "Quack", "Bite", "Scrunch", "Plop",
        "Snuggle", "Hop", "Roll", "Fumble", "Stretch", "Squirm", "Tumble",
        "Poke", "Quack", "Bite", "Smash", "Strike", "Grip", "Jump", "Lash",
        "Swing", "Slide", "Kick", "Leap", "Rush", "Bolt", "Sprint", "Charge","Fart", "Sniff", "Drool", "Burp", "Squish", "Wiggle", "Flop", "Snort",
        "Slap", "Hump", "Fuck", "Shit", "Pee", "Moan", "Spit", "Chomp", "Scoot",
        "Lick", "Scratch", "Squeak", "Smack", "Gargle", "Prank", "Twerk",
        "Droop", "Quack", "Plop", "Snuggle", "Hump", "Waddle", "Sneeze",
        "Pout", "Flail", "Slurp", "Poke", "Squeeze", "Shake", "Tickle",
        "Chug", "Wobble", "Jiggle", "Fumble", "Bark", "Tumble", "Wank",
        "Scoot", "Boink", "Smash", "Plunge", "Twiddle", "Grope", "Pinch",
        "Squeeze", "Grind", "Scratch", "Drool", "Paddle", "Snuggle", "Chafe",
        "Slobber", "Scoff", "Dribble", "Fondle"
        "Grab", "Twist", "Pull", "Push", "Step", "Climb", "Dive", "Plunge"
        ]

    random_short_phrases = [
        "Hold my beer", "Bless this mess", "Eat my shorts", "Call me maybe",
        "Send it!", "Not today", "Do it live", "Stay salty", "Full send",
        "Get wrecked", "Chill your beans", "Send noods", "Spicy vibes",
        "Why tho?", "Big yikes", "Oh snap", "Bite me", "Deal with it",
        "Hard pass", "Mind the gap", "Break a leg", "Top notch",
        "Zero chill", "What's up?", "For science!", "Just wing it",
        "In your dreams", "Hit the road", "Well, crap", "Game on",
        "Oh, fudge", "All the feels", "Slow your roll", "Say what?",
        "Shut up!", "No biggie", "Get bent", "Holy smokes", "Cool beans",
        "Yolo swag", "Don’t @ me", "Bruh moment", "Mic drop",
        "Plot twist", "Big mood", "Send it bruv", "Check yourself",
        "Keep it classy", "Flip the script", "Hold the line", "Get lost",
        "Stay frosty", "Eat dirt", "Own the night", "Hot mess", "What a vibe",
        "Be right back", "No way!", "Dope AF", "Hell yeah", "Chug life",
        "Cry me a river", "Too legit", "Can’t even", "Flex on them",
        "Mood booster", "Get good", "Meh vibes", "Mood swing", "Sassy queen",
        "Boss move", "Lame sauce", "Slick moves", "Epic fail", "Send it, bro",  "Roll with it", "Drop the mic", "High key", "Low key",
        "Kick rocks", "Make it rain", "What’s the tea?", "Sip it slow",
        "Take the L", "Big brain time", "Fake it, bro", "Bet on it",
        "Push the button", "Full tilt", "Dance it out", "Loud and proud",
        "Chase the vibe", "Risk it all", "Nice try", "Level up",
        "No cap", "Get outta here", "Over the top", "Straight fire",
        "Let it rip", "Make it weird", "Run for it", "Zip it up",
        "Shake it off", "Glow up", "Panic mode", "Too spicy",
        "Broke the mold", "Catch these hands", "Vibe check",
        "Major cringe", "I’m dead", "Off the rails", "Crash and burn",
        "What a flex", "Own it", "Pay the piper", "One for the books",
        "Big oof", "Ride or die", "Talk to the hand", "Yikes forever",
        "It’s a trap", "What a legend", "Full throttle", "Let’s boogie",
        "That’s sus", "Call the shots", "Punch it, Chewie", "Go ham",
        "All in", "Watch your back", "Clap back", "Skrrt skrrt",
        "Buckle up", "Ride the wave", "All gas, no brakes",
        "Drop the act", "Run it back", "On thin ice", "Shoot your shot",
        "Send it hard", "Eyes on me", "Don’t choke", "Brace yourself",
        "Cash me outside", "Can’t stop, won’t stop", "Pipe down",
        "Get hyped", "Don’t mess up", "Lights out", "Game face on",
        "Let’s bounce", "Run and gun", "Feel the burn", "Nailed it!"
    ]

    def generate_unique_set_of_titles(self, number_of_titles: int = 30):
        title_set = set()
        while len(title_set) != number_of_titles:
            title_set.add(self.generate_title())
        return title_set

    def generate_title(self, category: str = "album") -> str:
        # Choose a random generation strategy
        strategy = random.choice([
            "single_noun", "single_verb", "single_adjective", "short_phrase",
            "adj_noun", "noun_verb", "verb_adj_noun", "random_combo"
        ])

        # Generate based on the strategy
        if strategy == "single_noun":
            return random.choice(self.nouns)
        elif strategy == "single_verb":
            return random.choice(self.verbs)
        elif strategy == "single_adjective":
            return random.choice(self.adjectives)
        elif strategy == "short_phrase":
            return random.choice(self.random_short_phrases)
        elif strategy == "adj_noun":
            return f"{random.choice(self.adjectives)} {random.choice(self.nouns)}"
        elif strategy == "noun_verb":
            return f"{random.choice(self.nouns)} {random.choice(self.verbs)}"
        elif strategy == "verb_adj_noun":
            return f"{random.choice(self.verbs)} {random.choice(self.adjectives)} {random.choice(self.nouns)}"
        elif strategy == "random_combo":
            # Combine two or three random elements in no particular order
            elements = random.sample(
                [random.choice(self.adjectives), random.choice(self.nouns), random.choice(self.verbs)],
                k=random.randint(2, 3)
            )
            return " ".join(elements)

        # Fallback: Random short phrase
        return random.choice(self.random_short_phrases)
