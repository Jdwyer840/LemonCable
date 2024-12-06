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
        "Trashy", "Whiny", "Freakish", "Bitchish", "Sluts", "Psychotic", "Busted", "gritty", "dusty", "rustic", "spurred", "brawny", "lonesome", "outlawed", "sunset",
    "shadowy", "wild", "grizzled", "rugged", "bronzed", "saddle worn", "stubbled",
    "gravelly", "weathered", "barbed", "ironclad", "whiskey slicked", "gold dust",
    "galactic", "stellar", "cosmic", "neon", "hyperdrive", "quantum", "celestial",
    "interstellar", "spacial", "voided", "alien", "martian", "futuristic",
    "chromatic", "dystopian", "mechanoid", "laser focused", "techno", "cybernetic",
    "plasma filled", "dimensionless", "gravitational", "parallel", "light speed",
    "horrific", "ghastly", "macabre", "eerie", "bloodied", "grisly", "phantasmal",
    "bone chilling", "haunted", "shadowed", "spine crawling", "fanged", "cursed",
    "witchy", "occult", "undead", "mummified", "spectral", "howling", "graven",
    "nightmarish", "darkened", "sinister", "foreboding", "guttural", "cryptic",
    "metallic", "ferocious", "blazing", "screaming", "devilish", "thunderous",
    "powerful", "hellish", "infernal", "fiery", "scorched", "chaotic", "headbanging",
    "iron fisted", "steelbound", "vicious", "vengeful", "berserk", "unholy",
    "war torn", "savage", "apocalyptic", "doomladen", "forged", "gory", "blackened",
    "skeletal", "necrotic", "flaming", "barbaric", "ashen", "vile", "cataclysmic",
    "reaperlike", "razor sharp", "brutal", "howling", "obsidian", "bloodthirsty",
    "darkened", "voidborn", "shattered", "stormridden", "apex", "razorclad"]

    nouns = ["Storm", "Heart", "Soul", "Fire", "Dream", "Night", "Shadow",
        "Rebel", "Phoenix", "Chaos", "Flame", "Light", "Rain", "Thunder",
        "Horizon", "Ashes", "Infinity", "Sky", "Wind", "Silence", "Waves",
        "Tide", "Destiny", "Moon", "Raven", "Eclipse", "Chasm", "Edge", "Sawtooth Tiger",
        "Glory", "Fate", "Spirit", "Wilderness", "Forest", "Ember",
        "Mystery", "Serpent", "Wraith","politics", "religion", "deserts", "oceans", "mountains", "forests", "rivers", "countries",
    "cities", "villages", "towns", "governments", "laws", "justice", "freedom", "equality",
    "traditions", "culture", "philosophy", "history", "science", "technology", "art",
    "music", "literature", "education", "knowledge", "truth", "beliefs", "faith",
    "morality", "ethics", "war", "peace", "conflict", "revolution", "democracy",
    "dictatorship", "capitalism", "socialism", "communism", "anarchy", "civilization",
    "empire", "kingdom", "republic", "dynasty", "empire", "pharaoh", "gladiator", "crusade", "chariot", "artifact",
    "hieroglyph", "archaeology", "renaissance", "dark ages", "siege", "trebuchet",
    "catapult", "medieval", "vikings", "knights", "plague", "samurai", "coliseum",
    "tomb", "mummy", "explorer", "conquistador", "inquisition", "revolution",
    "alchemy", "guild", "crown", "scepter", "papyrus", "scroll", "manuscript",
    "armory", "battlefield", "fortress", "galleon", "keel", "cannonball",
    "monarch", "serf", "peasant", "alchemy", "monastery", "cathedral", "oracle",
    "graveyard", "haunted house", "zombie", "werewolf", "vampire", "slasher",
    "chainsaw", "demon", "possession", "seance", "witch", "coven", "poltergeist",
    "phantom", "creepy doll", "crypt", "basement", "attic", "curse", "ritual",
    "blood moon", "full moon", "fog", "scream", "shadow", "nightmare",
    "ghost", "specter", "skull", "skeleton", "ritual dagger", "cult", "evil twin",
    "abandoned asylum", "serial killer", "mask", "shadows", "creepy forest",
    "grave marker", "pumpkin patch", "witchcraft", "book of spells", "black cat",
    "tarot cards", "sinister", "omen", "coffin", "hearse", "cemetery",
    "goober", "dingleberry", "flibbertigibbet", "snickerdoodle", "bamboozle",
    "lollygag", "hullabaloo", "fiddlesticks", "skedaddle", "shenanigans",
    "hootenanny", "kerfuffle", "boondoggle", "wackadoodle", "flummox",
    "thingamajig", "whatchamacallit", "doohickey", "gobbledygook", "hogwash",
    "nincompoop", "ragamuffin", "bumfuzzle", "cattywampus", "jabberwocky",
    "snollygoster", "lickspittle", "poppycock", "malarkey", "fopdoodle",
    "whippersnapper", "klutz", "brouhaha", "guffaw", "hodgepodge",
    "booger", "turdnugget", "fartknocker", "wigglebottom", "pickleweasel",
    "crumpet", "sassyfrass", "flapdoodle", "gigglesnort", "zamboni",
    "toots", "twaddle", "blubberbutt", "sockdologer", "bumbling buffoon",
    "piddlywink", "mugwump", "snickerdoodle", "beelzebub", "quibbler" "monarchy", "feudalism", "theocracy",
    "economy", "trade", "industry", "agriculture", "resources", "wealth",
    "poverty", "hunger", "famine", "health", "medicine", "disease", "epidemic",
    "pandemic", "climate", "weather", "seasons", "sunlight", "rain", "snow",
    "wind", "hurricanes", "tornadoes", "earthquakes", "volcanoes", "wildlife",
    "habitat", "extinction", "evolution", "genes", "biology", "chemistry",
    "physics", "astronomy", "galaxies", "stars", "planets", "moons", "blackholes",
    "cosmos", "universe", "space", "time", "gravity", "energy", "matter",
    "atoms", "particles", "waves", "light", "darkness", "shadows", "dreams",
    "imagination", "creativity", "invention", "innovation", "exploration",
    "discovery", "adventure", "journey", "voyage", "expedition", "migration",
    "settlement", "colonization", "slavery", "liberation", "oppression", "resistance",
    "justice", "inequality", "discrimination", "rights", "privileges",
    "obligations", "duties", "relationships", "family", "friendship",
    "love", "marriage", "divorce", "parenting", "childhood", "adulthood",
    "aging", "death", "mourning", "grief", "happiness", "sadness", "anger",
    "fear", "courage", "patience", "compassion", "kindness", "charity",
    "violence", "crime", "punishment", "rehabilitation", "education", "learning",
    "wisdom", "ignorance", "knowledge", "mystery", "curiosity", "questions",
    "answers", "secrets", "lies", "truth", "reality", "fantasy", "fiction",
    "stories", "narratives", "legends", "myths", "folklore", "rituals",
    "symbols", "languages", "dialects", "scripts", "writing", "communication",
    "media", "news", "propaganda", "advertising", "marketing", "consumption",
    "consumerism", "capital", "labor", "markets", "profits", "losses", "investments",
    "savings", "loans", "debt", "wealth", "poverty", "hunger", "abundance",
    "scarcity", "plenty", "surplus", "deficit", "balance", "imbalance",
    "harmony", "discord", "unity", "division", "integration", "segregation",
    "fusion", "separation", "connection", "isolation", "community", "society",
    "individual", "identity", "self", "ego", "consciousness", "awareness",
    "thoughts", "ideas", "beliefs", "faith", "doubt", "hope", "despair",
    "optimism", "pessimism", "ambition", "contentment", "freedom", "slavery",
    "tyranny", "liberty", "justice", "peace", "war", "conflict", "agreement",
    "treaties", "alliances", "enemies", "friends", "rivals", "competitors",
    "partners", "collaborators", "teamwork", "cooperation", "leadership",
    "followership", "hierarchies", "networks", "systems", "organizations",
    "institutions", "companies", "corporations", "businesses", "entrepreneurs",
    "workers", "employers", "employees", "managers", "executives", "leaders",
    "followers", "innovators", "creators", "artists", "scientists", "engineers",
    "teachers", "students", "learners", "mentors", "guides", "explorers",
    "adventurers", "pioneers", "trailblazers", "heroes", "villains", "protagonists",
    "antagonists", "characters", "actors", "roles", "scripts", "dialogues",
    "monologues", "soliloquies", "performances", "audiences", "spectators",
    "viewers", "readers", "listeners", "observers", "participants", "players",
    "competitors", "contestants", "champions", "winners", "losers", "survivors" "Vision", "Beacon", "Canyon",
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
        "Bug", "Whisker", "Snout", "Ostrich", "Puffin", "astronaut", "galaxy", "black hole", "meteor", "nebula", "cosmos", "satellite", "orbit", "spaceship",
    "starlight", "planet", "rocket", "asteroid", "milky way", "comet", "space station", "alien", "telescope",
    "constellation", "quasar", "dancing star", "lunar eclipse", "solar system",
    "waltz", "tango", "salsa", "bachata", "cha cha", "swing", "foxtrot", "breakdance", "hip hop",
    "ballet", "jazz", "tap dance", "flamenco", "polka", "jitterbug", "rumba", "quickstep",
    "spork", "snail mail", "pickle", "banana phone", "rubber duck", "rainbow", "trampoline", "toothbrush",
    "cactus", "unicorn", "disco ball", "bubble wrap", "sock puppet", "pirate", "robot", "sloth",
    "penguin", "platypus", "yeti", "marshmallow", "fizzy drink", "spaghetti", "potato salad",
    "avocado toast", "toaster", "meatball", "ice cream", "cupcake", "rainboot", "glowstick",
    "plunger", "squeegee", "yo yo", "hotdog", "hamburger", "ketchup", "pogo stick", "balloon animal",
    "cheeseburger", "nacho", "pajamas", "roller skates", "pogo stick", "zebra", "raincloud", "pizza",
    "noodle", "corn dog", "space pirate", "moonwalker", "starfish", "bubble bath", "rubber band",
    "doodle", "hamster", "hedgehog", "sandcastle", "beach ball", "trombone", "kazoo", "jukebox",
    "hula hoop", "cowboy hat", "astronaut ice cream", "marble", "lava lamp", "snuggie", "giraffe",
    "popcorn", "fairy dust", "jack in the box", "monkey wrench", "party hat", "bouncy castle",
    "snowman", "moose", "glitter", "gummy bear", "jellybean", "whoopee cushion", "accordion",
    "milkshake", "watermelon", "flamingo", "spacesuit", "space bar", "warp drive", "beam me up",
    "starship", "hoverboard", "mars rover", "venus flytrap", "pulsar", "astral projection",
    "dancing queen", "disco pants", "rocket boots", "space cadet", "asteroid belt", "neutron star",
    "cosmic ray", "space junk", "gravity well", "warp speed", "galactic emperor", "solar flare",
    "lunar lander", "space cookie", "comet tail", "zero gravity", "moonbase", "alien abduction",
    "space crystal", "tang", "spaghetti monster", "cupcake king", "nacho supreme", "rainbow unicorn",
    "socks in space", "flying pig", "skipping stone", "sneeze machine", "sandwich art",
    "dancing doughnut", "boogie monster", "snack baron", "bubble snail", "spaceman sneeze"]
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
        "Yawning", "Poking", "Capture", "Conquer", "Seize", "March", "Beseech", "Revolt", "Dominate", "Raid",
    "Pillage", "Plunder", "Execute", "Subdue", "Flee", "Pursue", "Negotiate",
    "Ambush", "Defend", "Unravel", "Reign", "Usurp", "Duel", "Cower", "Proclaim",
    "Surrender", "Halt", "Emerge", "Erect", "Summon", "Imprison", "Crown",
    "Fortify", "Embody", "Dismantle", "Falsify", "Worship", "Denounce",
    "Oust", "Establish", "Reclaim", "Embrace", "Torment", "Shiver", "Weep",
    "Lament", "Haunt", "Dread", "Terrorize", "Menace", "Devour", "Howl",
    "Scratch", "Chase", "Snarl", "Whisper", "Crush", "Entice", "Sway",
    "Conspire", "Hiss", "Eviscerate", "Stalk", "Unleash", "Mutilate",
    "Pierce", "Swarm", "Twist", "Disguise", "Emerge", "Descend", "Eclipse",
    "Gleam", "Shatter", "Desecrate", "Entomb", "Poison", "Incite", "Manipulate",
    "Flinch", "Bicker", "Jape", "Sneer", "Mock", "Guffaw", "Wail", "Sniffle",
    "Jeer", "Scoff", "Feign", "Plead", "Scheme", "Swagger", "Swindle",
    "Whimper", "Clamber", "Cringe", "Peep", "Shriek", "Leap", "Wrangle",
    "Stumble", "Crawl", "Grovel", "Stomp", "Shove", "Tug", "Twirl", "Clutch",
    "Hurl", "Vault", "Flip", "Grip", "Cling", "Barter", "Beg", "Gnaw",
    "Chew", "Squeal", "Yelp", "Tinker", "Jostle", "Prod", "Flop", "Waddle",
    "Trot", "Whack", "Dash", "Pummel", "Flick", "Swat", "Snatch", "Flinch",
    "Toss", "Bash", "Crash", "Fiddle", "Snore", "Giggle", "Snort", "Chirp",
    "Burrow", "Thump", "Grunt", "Flail", "Rattle", "Creak", "Clang", "Dodge",
    "Scurry", "Bolt", "Sprint", "Lurk", "Duck", "Plummet", "Erupt", "Gasp",
    "Chuckle", "Blurt", "Sputter", "Sigh", "Exhale", "Wince", "Yawn", "Slither",
    "Stab", "Poke", "Jab", "Whack", "Swipe", "Shred", "Skid", "Scoot", "Paddle",
    "Slink", "Quiver", "Nuzzle", "Sprawl", "Wrestle", "Quake", "Quaff", "Bumble",
    "Ramble", "Slouch", "Brood", "Vanish", "Appear", "Soak", "Frolic", "Twiddle",
    "Hasten", "Waver", "Confront", "Wander", "Expand", "Evoke", "Ignite",
    "Enrage", "Bewilder", "Conceal", "Transform", "Summon", "Implore", "Vex",
    "Awaken", "Invoke", "Perish", "Resurrect", "Gnash", "Thrash", "Writhe",
    "Dismember", "Transcend", "Incinerate", "Engulf", "Obliterate" "Stinking", "Barking", "Bark", "Drooping",
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
        "Grab", "Twist", "Pull", "Push", "Step", "Climb", "Dive", "Plunge", "Penetrate"
        ]

    random_short_phrases = [
        "Hold my beer", "Bless this mess", "Eat my shorts", "Call me maybe",
        "Send it!", "Not today", "Do it live", "Stay salty", "Full send",
        "Get wrecked", "Chill your beans", "Send noods", "Spicy vibes",
        "Why tho", "Big yikes", "Oh snap", "Bite me", "Deal with it",
        "Hard pass", "Mind the gap", "Break a leg", "Top notch",
        "Zero chill", "What is up", "For science!", "Just wing it",
        "In your dreams", "Hit the road", "Well, crap", "Game on", "Fucked and Out of Luck",
        "Uptown Gals", "Gay Man Kickboxing", "Flight of the Hot Holes", "ABCs", "Five Four Two", "Six Three Not Me",
        "Oh, fudge", "All the feels", "Slow your roll", "Say what",
        "Shut up!", "No biggie", "Get bent", "Holy smokes", "Cool beans",
        "Yolo swag", "Dont @ me", "Bruh moment", "Mic drop",
        "Plot twist", "Big mood", "Send it bruv", "Check yourself",
        "Keep it classy", "Flip the script", "Hold the line", "Get lost",
        "Stay frosty", "Eat dirt", "Own the night", "Hot mess", "What a vibe",
        "Be right back", "No way!", "Dope AF", "Hell yeah", "Chug life",
        "Cry me a river", "Too legit", "Cant even", "Flex on them",
        "Mood booster", "Get good", "Meh vibes", "Mood swing", "Sassy queen",
        "Boss move", "Lame sauce", "Slick moves", "Epic fail", "Send it, bro",  "Roll with it", "Drop the mic", "High key", "Low key",
        "Kick rocks", "Make it rain", "Whats the tea", "Sip it slow",
        "Take the L", "Big brain time", "Fake it, bro", "Bet on it",
        "Push the button", "Full tilt", "Dance it out", "Loud and proud",
        "Chase the vibe", "Risk it all", "Nice try", "Level up",
        "No cap", "Get outta here", "Over the top", "Straight fire",
        "Let it rip", "Make it weird", "Run for it", "Zip it up",
        "Shake it off", "Glow up", "Panic mode", "Too spicy",
        "Broke the mold", "Catch these hands", "Vibe check",
        "Major cringe", "Im dead", "Off the rails", "Crash and burn",
        "What a flex", "Own it", "Pay the piper", "One for the books",
        "Big oof", "Ride or die", "Talk to the hand", "Yikes forever",
        "Its a trap", "What a legend", "Full throttle", "Lets boogie",
        "Thats sus", "Call the shots", "Punch it, Chewie", "Go ham",
        "All in", "Watch your back", "Clap back", "Skrrt skrrt",
        "Buckle up", "Ride the wave", "All gas, no brakes",
        "Drop the act", "Run it back", "On thin ice", "Shoot your shot",
        "Send it hard", "Eyes on me", "Dont choke", "Brace yourself",
        "Cash me outside", "Cant stop, wont stop", "Pipe down",
        "Get hyped", "Dont mess up", "Lights out", "Game face on",
        "Lets bounce", "Run and gun", "Feel the burn", "Nailed it!", "Hold the line", "Feel the vibe", "Make it happen", "Ride the storm",
    "Flip the switch", "Catch the wave", "Take the shot", "Hit the gas",
    "Full power", "Level the field", "Break the mold", "Keep it real",
    "Turn the tide", "Own the moment", "Set the tone", "Chase the dream",
    "Bring the heat", "Raise the bar", "Stay the course", "Kick the tires",
    "Light the fire", "Hit the ground", "Take a chance", "Move the needle",
    "Run the show", "Take the wheel", "Play the game", "Clear the air",
    "Run the race", "Shake it up", "Stay on track", "Own the night",
    "Face the music", "Find the spark", "Hit the lights", "Keep the peace",
    "Ride the wave", "Start the engine", "Fuel the fire", "Watch the clock",
    "Chase the sun", "Keep the faith", "Feel the rush", "Make your move",
    "Stand your ground", "Call the shots", "Roll the dice", "Go the distance",
    "Make it count", "Push the limits", "Change the game", "Feel the power",
    "Know the score", "Trust the process", "Climb the ladder", "Seize the day",
    "Follow the plan", "Start the journey", "Lead the charge", "Show the way",
    "Take the lead", "Run the play", "Play it cool", "Make it shine",
    "Hit the mark", "Find your groove", "Take the plunge", "Find your fire",
    "Seal the deal", "Find the rhythm", "Run the table", "Stand the test",
    "Keep your cool", "Feel the flow", "Ride the lightning", "Catch the wind",
    "Push the button", "Hit the brakes", "Turn the page", "Make it stick",
    "Hold your ground", "Find your footing", "Press the issue", "Take a stand",
    "Take a bow", "Keep your head", "Find the balance", "Play it straight",
    "Hold the line", "Face the storm", "Rise to glory", "Aim for greatness",
    "Reach the summit", "Crush the goal", "Stay the path", "Set the standard",
    "Claim the prize", "Fight the fight", "Win the day", "Beat the odds",
    "Finish strong", "Live the moment", "Embrace the chaos", "Harness the energy",  "Keep moving", "Stay bold", "Lead the way", "Feel alive",
    "Step up", "Stand tall", "Make waves", "Keep pushing",
    "Stay sharp", "Play big", "Think fast", "Find strength",
    "Take charge", "Keep steady", "Stay wild", "Keep going",
    "Stay ready", "Find courage", "Be fierce", "Move forward",
    "Stay strong", "Chase victory", "Keep rising", "Face forward",
    "Move mountains", "Stay steady", "Keep climbing", "Be unstoppable",
    "Stay fearless", "Push harder", "Stay grounded", "Stay determined",
    "Rise above", "Go higher", "Keep hustling", "Stay focused",
    "Keep dreaming", "Find balance", "Be daring", "Move faster",
    "Push through", "Stay inspired", "Think bigger", "Move closer",
    "Keep thriving", "Rise strong", "Stay humble", "Stay bold",
    "Dream bigger", "Feel unstoppable", "Keep soaring", "Push forward",
    "Think clearly", "Stay ambitious", "Stay creative", "Be relentless",
    "Keep striving", "Take the leap", "Find your edge", "Stay powerful",
    "Hold the vision", "Make your mark", "Reach for more", "Go beyond",
    "Rise together", "Stay focused", "Keep innovating", "Lead boldly",
    "Find your spark", "Stay true", "Keep shining", "Face your fears",
    "Stay limitless", "Stay unique", "Push your limits", "Go all in",
    "Keep believing", "Stay motivated", "Stay authentic", "Own your space",
    "Live fully", "Reach higher", "Stay committed", "Think outside",
    "Own your moment", "Drive forward", "Fuel your fire", "Find your drive",
    "Chase greatness", "Embrace challenge", "Go the extra", "Stand strong",
    "Stay persistent", "Find your flow", "Create your path", "Run your race",
    "Forge ahead", "Build momentum", "Embrace ambition", "Shatter limits",
    "Unlock potential", "Keep creating", "Find your rhythm", "Stay centered",
        "Hold my drink", "What the hell", "Hot mess express", "Send help",
        "Zero fucks given", "Spill the tea", "Big oof energy", "Oh crap",
        "Well shit", "Full shitstorm ahead", "Party like a legend",
        "Keep your pants on", "Hotter than hell", "Out of fucks",
        "Whiskey tango foxtrot", "Call the cops", "Shits and giggles",
        "Damn it all", "Balls to the wall", "Take a damn seat",
        "Kiss my ass", "No filter needed", "Burn it all down",
        "Drop some truth", "Go to hell", "Straight savage",
        "Shut your piehole", "Piss off", "Damn straight",
        "Where is my drink", "Too hot to handle", "Send wine",
        "Get off my lawn", "This is my circus", "It is all bullshit",
        "Pour another round", "Who invited this guy", "Talk shit get hit",
        "Big dick energy", "Screw this noise", "Hold my purse",
        "This is chaos", "Pity party for one", "Burn it to ashes",
        "Where is the tequila", "Go full send", "Crap hit the fan",
        "This sucks hard", "Hell no", "Deal with this shit",
        "Drunk and thriving", "Send the bail money", "Beer me now",
        "Vodka cures everything", "Oh hell yeah", "Flip the damn table",
        "Save your bullshit", "Slap some sense", "Take a damn chill pill",
        "Too sober for this", "Champagne problems", "Drink about it",
        "Get your shit together", "Go raise some hell", "All aboard the hot mess",
        "Shut it down", "Drink it like you mean it", "Where is my sanity",
        "Party like a rockstar", "Zero chill zone", "Who pissed in your cereal",
        "Shit just got real", "What a shitshow", "Handle your shit",
        "Stop talking crap", "Raise some hell", "Bend the damn rules",
        "Throw me a drink", "Give no shits", "Laugh your ass off",
        "Too much sauce", "Pour it up", "No brakes allowed",
        "Here for the drama", "Drinks on me", "Sassy and smashing",
        "Go hard or go home", "Bring the damn heat", "Screw it, I am in",
        "Full meltdown mode", "Hotter than my ex", "Make it spicy",
        "Shut up and drink", "Burn bridges boldly", "Too much damn coffee",
        "Karma is drunk", "Cry like a badass", "Screw the rules",
        "Raise the damn stakes", "Do not tempt me", "Zero regrets",
    "Shut the fuck up", "Well fuck me sideways", "Jesus tap-dancing Christ",
    "This is a shitshow", "What fresh hell is this", "Get your shit together",
    "Ass over teakettle", "Who the fuck cares", "Eat shit and die",
    "Holy mother of fuck", "Balls deep in chaos", "Kiss my hairy ass",
    "Get wrecked, loser", "Fuck this noise", "Drunk as a skunk",
    "Shit just hit the fan", "Zero shits given", "Hot as Satan s balls",
    "Straight to hell", "Raise some fucking hell", "Stop being a dick",
    "You absolute jackass", "Piss up a rope", "What the actual fuck",
    "Tighter than a nun s knickers", "Go fuck yourself",
    "Shit the bed on that one", "Hell in a handbasket",
    "Who lit this dumpster fire", "Slap your ass into gear",
    "Run like hell", "Fuck around and find out",
    "Drunk as a motherfucker", "Balls to the fucking wall",
    "Not my circus, not my monkeys", "Get your shit together, Karen",
    "Shove it where the sun don t shine", "You colossal fuckup",
    "Dumber than a box of rocks", "Holy shitballs",
    "I am done with this bullshit", "Fuck it, I am out",
    "Crap on a cracker", "Do not be an asshole",
    "What a steaming pile of shit", "Shit your pants funny",
    "Stop your damn whining", "Get bent, asshole",
    "Who invited this shithead", "Fucking amateur hour",
    "Go pound sand", "Lose your shit properly",
    "Well butter my ass and call me a biscuit",
    "Shit-eating grin", "Raise hell and drink whiskey",
    "Get the fuck over it", "Drop the fucking ball",
    "Full-on shitstorm", "Shut your damn mouth",
    "Take a flying fuck", "Blow it out your ass",
    "Colder than a witch s tit", "The shit has sailed",
    "Asshat extraordinaire", "Shit happens, bro",
    "Shut the front door", "Fucking nailed it",
    "Go screw yourself", "Hotter than Satan s sauna",
    "Up shit creek without a paddle", "Dumbass alert",
    "Stop being a shitbag", "Holy fucking shit",
    "Drunk and disorderly", "Eat my shorts, asshole",
    "Get your head out of your ass", "Hell of a clusterfuck",
    "Messy as fuck", "What a goddamn disaster",
    "Fuck you and the horse you rode in on",
    "Chug a beer and calm the fuck down",
    "Hot as Satans left nut", "Fucked and fabulous",
    "Suck it up, buttercup", "Do not be a shithead",
    "Crazy as batshit", "Burn this shit to the ground",
    "Cool your damn jets", "Sassy and savage",
    "No one gives a flying fuck", "Drunk as hell and twice as ugly",
    "Raise your middle finger", "Absolutely fucked",
    "Trashier than a landfill", "Choke on it, buddy",
    "Holy motherfucking shit", "Shut it and drink up"
    ]

    def generate_unique_set_of_titles(self, number_of_titles: int = 30, used_titles: set = None):
        title_set = set()
        while len(title_set) != number_of_titles:
            current_title = self.generate_title()
            if used_titles is not None and current_title in used_titles:
                print("Title already used.")
                continue
            title_set.add(current_title)
        return title_set

    def generate_title(self, category: str = "album") -> str:
        # Choose a random generation strategy
        strategy_pool = [
            "single_noun", "single_verb", "single_adjective", "short_phrase",
            "adj_noun", "noun_verb", "verb_adj_noun", "random_combo", "double_noun",
            "short_phrase_and_a_noun", "short_phrase_with_a_noun", "noun_and_noun",
            "random_combo", "noun_on_a_noun", "like_a_noun", "passing_by_a_noun",
            "verb_by_a_noun", "in_the_adj_noun", "noun_of_a_noun", "verb_the_noun",
            "noun_in_the_noun", "the_noun_and_the_noun", "adjective_and_adjective",
            "verb_a_verb", "random_combo_funny", "the_adj_of_the_noun",
            "verb_with_a_noun", "adjective_verb_noun", "gerund_and_the_noun",
            "from_the_adj_noun", "noun_at_a_time", "adj_noun_in_space", "noun_vs_noun", "the_adj_and_the_noun", "gerund_of_a_noun", "dude_where_is_my_noun"
        ]

        # Add weights for more randomness (some strategies appear more frequently)
        weighted_strategies = strategy_pool * 2 + ["short_phrase", "random_combo", "adj_noun"] * 3

        # Select one or more strategies for layering
        primary_strategy = random.choice(weighted_strategies)
        secondary_strategy = random.choice(strategy_pool)

        # 50% chance to use the secondary strategy for added randomness
        strategy = random.choice([primary_strategy, secondary_strategy])

        # Generate based on the strategy
        if strategy == "single_noun":
            return random.choice(self.nouns)
        elif strategy == "single_verb":
            return random.choice(self.verbs)
        elif strategy == "single_adjective":
            return random.choice(self.adjectives)
        elif strategy == "short_phrase":
            return random.choice(self.random_short_phrases)
        elif strategy == "short_phrase_and_a_noun":
            noun = random.choice(self.nouns)
            article = self.get_article(noun)
            return f"{random.choice(self.random_short_phrases)} and {article} {noun}"
        elif strategy == "short_phrase_with_a_noun":
            noun = random.choice(self.nouns)
            article = self.get_article(noun)
            return f"{random.choice(self.random_short_phrases)} with {article} {noun}"
        elif strategy == "adj_noun":
            return f"{random.choice(self.adjectives)} {random.choice(self.nouns)}"
        elif strategy == "noun_verb":
            return f"{random.choice(self.nouns)} {random.choice(self.verbs)}"
        elif strategy == "noun_on_a_noun":
            noun = random.choice(self.nouns)
            return f"{random.choice(self.nouns)} on {self.get_article(noun)} {noun}"
        elif strategy == "double_noun":
            return f"{random.choice(self.nouns)} {random.choice(self.nouns)}"
        elif strategy == "noun_and_noun":
            return f"{random.choice(self.nouns)} and {random.choice(self.nouns)}"
        elif strategy == "verb_adj_noun":
            return f"{random.choice(self.verbs)} {random.choice(self.adjectives)} {random.choice(self.nouns)}"
        elif strategy == "random_combo":
            elements = random.sample(
                [random.choice(self.adjectives), random.choice(self.nouns), random.choice(self.verbs)],
                k=random.randint(2, 3)
            )
            return " ".join(elements)
        elif strategy == "like_a_noun":
            noun = random.choice(self.nouns)
            article = self.get_article(noun)
            return f"Like {article} {noun}"
        elif strategy == "passing_by_a_noun":
            noun = random.choice(self.nouns)
            article = self.get_article(noun)
            return f"Passing by {article} {noun}"
        elif strategy == "dude_where_is_my_noun":
            noun: str = random.choice(self.nouns)
            return f"Where {'are' if noun.endswith('s') else 'is'} my {noun}"
        elif strategy == "gerund_of_a_noun":
            noun = random.choice(self.nouns)
            verb = random.choice(self.verbs)
            return f"{verb} of {self.get_article(noun)} {noun}"
        elif strategy == "the_adj_and_the_noun":
            adj = random.choice(self.adjectives)
            noun = random.choice(self.nouns)
            return f"The {adj} and the {noun}"
        elif strategy == "noun_vs_noun":
            return f"{random.choice(self.nouns)} vs {random.choice(self.nouns)}"
        elif strategy == "adj_noun_in_space":
            return f"{random.choice(self.adjectives)} {random.choice(self.nouns)} in Space"
        elif strategy == "verb_by_a_noun":
            noun = random.choice(self.nouns)
            article = self.get_article(noun)
            verb = random.choice(self.verbs)
            return f"{verb.capitalize()} by {article} {noun}"
        elif strategy == "in_the_adj_noun":
            adj = random.choice(self.adjectives)
            noun = random.choice(self.nouns)
            return f"In the {adj} {noun}"

        # Fallback: Random short phrase
        return random.choice(self.random_short_phrases)

    def get_article(self, word):
        """Determine whether to use 'a' or 'an' based on the word."""
        vowels = "aeiou"
        return "an" if word[0].lower() in vowels else "a"

    def pluralize_if_needed(self, word):
        """Return a pluralized form if the word is a plural noun."""
        if word.endswith("s"):
            return word
        # Pluralization logic (basic heuristic)
        return f"{word}s" if not word.endswith("y") else f"{word[:-1]}ies"