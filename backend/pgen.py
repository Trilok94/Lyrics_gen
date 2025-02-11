# importing libraries
import pronouncing
import markovify
import re
import random
import numpy as np
import os
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM


class RapGenerator:
    def __init__(self, artist, text_file, max_syllables, depth):
        self.artist = artist
        self.text_file = text_file
        # self.rap_file = rap_file
        self.max_syllables = max_syllables
        self.depth = depth
        self.model = None

    def create_network(self, train_mode):
        model = Sequential()
        model.add(LSTM(4, input_shape=(2, 2), return_sequences=True))
        for _ in range(self.depth):
            model.add(LSTM(8, return_sequences=True))
        model.add(LSTM(2, return_sequences=True))
        model.summary()
        model.compile(optimizer="rmsprop", loss="mse")

        if f"{self.artist}.rap.weights.h5" in os.listdir(".") and not train_mode:
            model.load_weights(f"{self.artist}.rap.weights.h5")
            print(f"Loaded saved network: {self.artist}.rap.weights.h5")

        self.model = model

    @staticmethod
    def markov_model(text_file):
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
        return markovify.NewlineText(text)

    def syllables(self, line):
        count = 0
        vowels = "aeiouy"
        for word in line.split(" "):
            word = word.lower().strip(".:;?!")
            if not word:  # Skip empty words
                continue
            if word[0] in vowels:
                count += 1
            for i in range(1, len(word)):
                if word[i] in vowels and word[i - 1] not in vowels:
                    count += 1
            if word.endswith("e"):
                count -= 1
            if word.endswith("le"):
                count += 1
            if count == 0:
                count += 1
        return count / self.max_syllables

    def rhymeindex(self, lyrics, train_mode):
        rhyme_file = f"{self.artist}.rhymes"
        if rhyme_file in os.listdir(".") and not train_mode:
            print(f"Loading saved rhymes from {rhyme_file}")
            with open(rhyme_file, "r", encoding="utf-8") as f:
                return f.read().split("\n")
        else:
            rhyme_master_list = []
            print("Building list of rhymes:")
            for line in lyrics:
                word = re.sub(r"\W+", "", line.split(" ")[-1]).lower()
                rhymes_list = pronouncing.rhymes(word)
                rhymes_list_ends = [r[-2:] for r in rhymes_list]
                rhymescheme = (
                    max(set(rhymes_list_ends), key=rhymes_list_ends.count)
                    if rhymes_list_ends
                    else word[-2:]
                )
                rhyme_master_list.append(rhymescheme)

            rhyme_master_list = sorted(set(rhyme_master_list))
            with open(rhyme_file, "w", encoding="utf-8") as f:
                f.write("\n".join(rhyme_master_list))
            return rhyme_master_list

    def rhyme(self, line, rhyme_list):
        word = re.sub(r"\W+", "", line.split(" ")[-1]).lower()
        rhymes_list = pronouncing.rhymes(word)
        rhymes_list_ends = [r[-2:] for r in rhymes_list]
        rhymescheme = rhymes_list_ends[0] if rhymes_list_ends else word[-2:]
        return (
            rhyme_list.index(rhymescheme) / float(len(rhyme_list))
            if rhymescheme in rhyme_list
            else 0
        )

    @staticmethod
    def split_lyrics_file(text_file):
        with open(text_file, encoding="utf-8") as f:
            text = f.read().split("\n")
        return [line for line in text if line]

    def generate_lyrics(self, text_model, text_file):
        bars = []
        last_words = []
        lyric_length = len(self.split_lyrics_file(text_file))
        count = 0
        markov_model = text_model

        while len(bars) < lyric_length / 9 and count < lyric_length * 2:
            bar = markov_model.make_sentence(max_overlap_ratio=0.49, tries=100)
            if bar and self.syllables(bar) < 1:
                last_word = bar.split(" ")[-1].strip("!.?,")
                if bar not in bars and last_words.count(last_word) < 3:
                    bars.append(bar)
                    last_words.append(last_word)
                    count += 1
        return bars

    def build_dataset(self, lines, rhyme_list):
        dataset = [
            [line, self.syllables(line), self.rhyme(line, rhyme_list)] for line in lines
        ]
        x_data, y_data = [], []

        for i in range(len(dataset) - 3):
            x = np.array([dataset[i][1:], dataset[i + 1][1:]]).flatten().reshape(2, 2)
            y = (
                np.array([dataset[i + 2][1:], dataset[i + 3][1:]])
                .flatten()
                .reshape(2, 2)
            )
            x_data.append(x)
            y_data.append(y)

        return np.array(x_data), np.array(y_data)

    def compose_rap(self, lines, rhyme_list, text_file):
        human_lyrics = self.split_lyrics_file(text_file)
        initial_index = random.choice(range(len(human_lyrics) - 1))
        initial_lines = human_lyrics[initial_index : initial_index + 2]
        starting_input = [
            [self.syllables(line), self.rhyme(line, rhyme_list)]
            for line in initial_lines
        ]

        rap_vectors = [self.model.predict(np.array([starting_input]))]
        for _ in range(100):
            rap_vectors.append(
                self.model.predict(np.array([rap_vectors[-1]]).reshape(1, 2, 2))
            )
        return rap_vectors

    def vectors_into_song(self, vectors, generated_lyrics, rhyme_list):
        def last_word_compare(rap, line2):
            penalty = 0
            for line1 in rap:
                word1 = line1.split(" ")[-1].strip("?!,. ")
                word2 = line2.split(" ")[-1].strip("?!,. ")
                if word1 == word2:
                    penalty += 0.2
            return penalty

        def calculate_score(vector_half, syllables, rhyme, penalty):
            desired_syllables = vector_half[0] * self.max_syllables
            desired_rhyme = vector_half[1] * len(rhyme_list)
            return (
                1.0
                - abs(desired_syllables - syllables)
                - abs(desired_rhyme - rhyme)
                - penalty
            )

        dataset = [
            [line, self.syllables(line), self.rhyme(line, rhyme_list)]
            for line in generated_lyrics
        ]
        rap = []
        vector_halves = [list(v[0][0]) for v in vectors] + [
            list(v[0][1]) for v in vectors
        ]

        for vector in vector_halves:
            scorelist = []
            for item in dataset:
                penalty = last_word_compare(rap, item[0]) if rap else 0
                score = calculate_score(vector, item[1], item[2], penalty)
                scorelist.append([item[0], score])

            best_line = max(scorelist, key=lambda x: x[1])[0]
            rap.append(best_line)
            dataset = [d for d in dataset if d[0] != best_line]
        return rap

    def train(self, x_data, y_data):
        self.model.fit(x_data, y_data, batch_size=2, epochs=5, verbose=1)
        self.model.save_weights(f"{self.artist}.rap.weights.h5")
        print(f"Saved artist rap to {self.artist}.rap.weights.h5")

    def main(self, train_mode):
        self.create_network(train_mode)
        text_model = self.markov_model(self.text_file)

        if train_mode:
            bars = self.split_lyrics_file(self.text_file)
        else:
            bars = self.generate_lyrics(text_model, self.text_file)

        rhyme_list = self.rhymeindex(bars, train_mode)

        if train_mode:
            x_data, y_data = self.build_dataset(bars, rhyme_list)
            self.train(x_data, y_data)
            return "model has been successfully trained"
        else:
            vectors = self.compose_rap(bars, rhyme_list, self.text_file)
            rap = self.vectors_into_song(vectors, bars, rhyme_list)
            return rap


# Parameters
# depth = 4
# max_syllables = 8
# deep_learning_model = "poem_model"
# # rap_file = "temporary_poem.txt"
# training_file = tfk.utils.get_file(
#     "hello.txt",
#     "https://storage.googleapis.com/kagglesdsdata/datasets/6776/19383/notorious_big.txt",
# )
