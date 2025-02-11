import keras._tf_keras.keras as tfk
from pgen import RapGenerator

deep_learning_model = "poem_model"

depth = 4
max_syllables = 8
training_file = tfk.utils.get_file(
    "hello.txt",
    "https://storage.googleapis.com/kagglesdsdata/datasets/6776/19383/notorious_big.txt",
)
training_file = "./song_lyrics/adele.txt"
# [
#     "adele",
#     "al-green",
#     "alicia-keys",
#     "amy-winehouse",
#     "beatles",
#     "bieber",
#     "bjork",
#     "blink-182",
#     "bob-dylan",
#     "bob-marley",
#     "britney-spears",
#     "bruce-springsteen",
#     "bruno-mars",
#     "cake",
#     "dickinson",
#     "disney",
#     "dj-khaled",
#     "dolly-parton",
#     "dr-seuss",
#     "drake",
#     "eminem",
#     "janisjoplin",
#     "jimi-hendrix",
#     "johnny-cash",
#     "joni-mitchell",
#     "kanye-west",
#     "kanye",
#     "Kanye_West",
#     "lady-gaga",
#     "leonard-cohen",
#     "lil-wayne",
#     "Lil_Wayne",
#     "lin-manuel-miranda",
#     "lorde",
#     "ludacris",
#     "michael-jackson",
#     "missy-elliott",
#     "nickelback",
#     "nicki-minaj",
#     "nirvana",
#     "notorious-big",
#     "notorious_big",
#     "nursery_rhymes",
#     "patti-smith",
#     "paul-simon",
#     "prince",
#     "r-kelly",
#     "radiohead",
#     "rihanna",
# ]

# training_file = "./song_lyrics/notorious-big.txt"
# with open(training_file, "r") as f:
#     line = f.readlines()
#     print(line)
generator = RapGenerator(deep_learning_model, training_file, max_syllables, depth)
rap = generator.main(train_mode=True)
print(rap)
