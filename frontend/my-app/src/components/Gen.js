import { useState } from 'react';
function Gen() {

    const [lyricsbool, updatelyricsbool] = useState(false)
    const [lyrics, updatelyrics] = useState([])
    const [selectedArtists, setSelectedArtists] = useState([]);
    const [showPopup, setShowPopup] = useState(false);

    const generatePoem = async () => {
        updatelyricsbool(true)
        updatelyrics(["Generating lyrics"])
        try {
            const requestBody = { artists: selectedArtists };
            const response = await fetch("http://127.0.0.1:5000/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // Optional, helps with response parsing
                },
                body: JSON.stringify(requestBody)
            });
            // Check if the response is OK (status 200-299)
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            // Parse the JSON response
            const data = await response.json();
            setShowPopup(true);  // Show the popup after generating poem
            const lyrics = data.lyrics
            updatelyrics(lyrics.slice(0, 50))
            updatelyricsbool(true)
            // const lyrics = data.lyrics

        } catch (error) {
            console.error("Fetch error:", error); // Log any error
        } finally {
            updatelyricsbool(false)
        }
    };

    const artist_list = [
        "adele",
        "al-green",
        "alicia-keys",
        "amy-winehouse",
        "beatles",
        "bieber",
        "bjork",
        "blink-182",
        "bob-dylan",
        "bob-marley",
        "britney-spears",
        "bruce-springsteen",
        "bruno-mars",
        "cake",
        "dickinson",
        "disney",
        "dj-khaled",
        "dolly-parton",
        "dr-seuss",
        "drake",
        "eminem",
        "janisjoplin",
        "jimi-hendrix",
        "johnny-cash",
        "joni-mitchell",
        "kanye-west",
        "kanye",
        "Kanye_West",
        "lady-gaga",
        "leonard-cohen",
        "lil-wayne",
        "Lil_Wayne",
        "lin-manuel-miranda",
        "lorde",
        "ludacris",
        "michael-jackson",
        "missy-elliott",
        "nickelback",
        "nicki-minaj",
        "nirvana",
        "notorious-big",
        "notorious_big",
        "nursery_rhymes",
        "patti-smith",
        "paul-simon",
        "prince",
        "r-kelly",
        "radiohead",
        "rihanna",
    ]

    const handleCheckboxChange = (event) => {
        const { id, checked } = event.target;
        if (checked) {
            setSelectedArtists((prev) => [...prev, id]); // Add to the list if checked
        } else {
            setSelectedArtists((prev) => prev.filter((artist) => artist !== id)); // Remove if unchecked
        }

    }
    const closePopup = () => {
        setShowPopup(false);  // Close popup when clicked on close button
    };
    const saveLyricsToFile = () => {
        // Convert lyrics array to a single string with line breaks
        const lyricsText = lyrics.join("\n");

        // Create a Blob object with lyrics data
        const blob = new Blob([lyricsText], { type: "text/plain" });

        // Create a temporary download link
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "generated_lyrics.txt";

        // Trigger the download
        link.click();

        // Clean up the URL object
        URL.revokeObjectURL(link.href);
    };

    return (

        <div>
            <div>
                <div className={lyricsbool ? " opacity-50 pointer-events-none" : ""}>
                    <div className='text-5xl font-semibold text-center my-4 font-mono'>Pick up your Artists</div>
                    {
                        (<div className='mx-4 my-4'>
                            <ul class=" grid gap-5 w-full md:grid-cols-4">
                                {artist_list.map((line, index) => (
                                    <li key={index} onChange={handleCheckboxChange}>
                                        <input type="checkbox" id={line} value="" class="hidden peer" required="" />
                                        <label for={line} class="inline-flex items-center justify-between w-full p-5 text-gray-500 bg-white border-2 border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 peer-checked:border-blue-600 peer-checked:bg-sky-900 hover:text-gray-600 dark:peer-checked:text-gray-300 peer-checked:text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700">
                                            <div class="block">
                                                <div class="w-full text-lg font-semibold">{line}</div>
                                            </div>
                                        </label>
                                    </li>
                                ))}
                                <li className="col-span-3 flex justify-center items-center">
                                    <button type="button" className=" w-full h-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" onClick={generatePoem}>
                                        Generate
                                    </button>
                                </li>
                            </ul>
                        </div>
                        )
                    }
                </div>
            </div>
            <div class="flex flex-col">
                {showPopup && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">


                        <div className="bg-white p-8 rounded-lg shadow-lg w-1/2 max-w-md max-h-[80vh] overflow-y-auto scrollbar-hide">
                            <div className='flex flex-row justify-between items-center mb-4'>
                                <h2 className="text-3xl font-bold ">Generated Lyrics</h2>
                                <button
                                    onClick={saveLyricsToFile}
                                    className="mt-4 text-white bg-green-500 hover:bg-green-600 px-4 py-2 rounded-lg"
                                >
                                    Save
                                </button>
                            </div>
                            <div>
                                {lyrics.map((line, index) => (
                                    <p key={index} style={{ margin: "5px 0" }}>
                                        {line.trim()}
                                    </p>
                                ))}
                            </div>
                            <button
                                onClick={closePopup}
                                className="mt-4 text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg"
                            >
                                Close
                            </button>
                        </div>

                    </div>
                )}
                {lyricsbool && (
                    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
                        <div class="spinner">
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Gen;
