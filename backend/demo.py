selected_artists = ["kanye", "adele"]
selected_artists = sorted(selected_artists)

unique_name = f"combined_{'_'.join(selected_artists)}"

filenames = []
for artist in selected_artists:
    filenames.append(f"./song_lyrics/{artist}.txt")

# Use UTF-8 encoding when reading and writing files
with open(f"./song_lyrics/{unique_name}.txt", "w", encoding="utf-8") as outfile:
    for fname in filenames:
        try:
            with open(fname, encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)
        except FileNotFoundError:
            print(f"File not found: {fname}")
        except UnicodeDecodeError as e:
            print(f"Error decoding {fname}: {e}")

final_filename = f"./song_lyrics/{unique_name}.txt"
