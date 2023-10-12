"""
Phidelity
GitHub: [JeffAllen714](https://github.com/JeffAllen714)

* * * * * * * * * * * * * * * * * * * * * * * * * * * *
README: Phidelity is still in development! Ive had a lot of fun with this one and...
hope to do a lot more audio related scripts in the future for creative production!

## Description ##
Phidelity is a granular synthesis tool that transforms audio files based on the Fibonacci sequence.
Its suggested that you run this with a rather long file as it will get truncated significantly.

## Features ##
- Granular synthesis processing using the Fibonacci sequence!
- GUI interface with easy to import files.
- Outputs a WAV file with a link to open it in Finder*

## How to Use ##
1. Run the script. A GUI will appear.
2. Enter the location of a WAV file and a name for the output file.
3. Click "Run" to process the audio.
5. Once finished, the message will change to "FINISHED," and a link to the generated WAV file will appear.
6. Click the link to open the newly generated WAV file in Finder*
* * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

import os
import time
import librosa
import numpy as np
import tkinter as tk
import soundfile as sf
from tkinter import filedialog


class Phidelity:
    """
    ## Description ##
    Phidelity is an audio manipulation tool that works with WAV format audio files.
    This class uses the Fibonacci sequence as the foundation for its granular syntheses process.
    In theory this should sound different everytime you run it.
    It's probably suggested you use a longer WAV file as it will be shortened significantly!

    ## Methods ##

    - fibonacciPseudoRandom(seed=None): Generates a pseudo-random number using the Fibonacci sequence.
      If `seed` is not provided, the current time in milliseconds is used as the seed.

    - granularSynthesis(inputFilePath, outputFilePath, seed=None, progressCallback=None): Performs
      granular synthesis on an input WAV file and writes the result to an output file
    """

    @staticmethod
    def fibonacciPseudoRandom(seed=None):
        # Generates a Pseudo Random sequence for the granularSynthesis Process
        if seed is None:
            seed = int(time.time() * 1000)

        fib = [0, 1]
        for _ in range(100):
            fib.append(fib[-1] + fib[-2])

        index = seed % len(fib)

        return fib[index]

    @staticmethod
    def granularSynthesis(inputFilePath, outputFilePath, seed=None, progressCallback=None):
        # Fragments the audio and rejoins for the output

        audio, sr = librosa.load(inputFilePath)
        numGrains = 100
        grainSize = 1024
        overlap = 0.5

        grains = []

        for grain in range(numGrains):
            start = np.random.randint(0, len(audio) - grainSize)
            grain = audio[start:start + grainSize]

            grains.append(grain)

            if progressCallback:
                progressCallback(grain / numGrains * 100)

        # Overlap and sum grains
        hopSize = int(grainSize * (1 - overlap))
        newAudio = np.zeros_like(audio)

        for grain in range(len(grains)):
            start = grain * hopSize
            end = start + grainSize
            newAudio[start:end] += grains[grain]

        # Output audio cannot be longer than the original audio
        if len(newAudio) > len(audio):
            newAudio = newAudio[:len(audio)]

        outputFilePath = f"{outputFilePath}.wav"

        sf.write(outputFilePath, newAudio, int(sr))


class PhidelityApp:
    """
    ## Description ##
    GUI application that is supplementary to the Phidelity granular synthesis tool (using tkinter)

    Methods:
    - __init__(self, master): Initialize
    - browseFile(): Select input WAV file.
    - runProcess(): Initiate granular synthesis
    - openFileInFinder(): generate the WAV file
    """

    def __init__(self, master):
        # Initialize tkinter GUI
        self.master = master
        master.title("Phidelity - Granular Synthesis Tool")

        # Create GUI elements
        self.filePathEntry = tk.Entry(master, width=50)
        self.browseButton = tk.Button(master, text="Browse", command=self.browseFile)
        self.runButton = tk.Button(master, text="Run", command=self.runProcess)
        self.statusLabel = tk.Label(master, text="")
        self.outputLabel = tk.Label(master, text="Output Filename:")
        self.outputEntry = tk.Entry(master, width=20)

        # Center the "Output Filename:" label and entry widget
        self.outputLabel.grid(row=4, column=0, pady=5, sticky=tk.E)
        self.outputEntry.grid(row=4, column=1, pady=5, sticky=tk.W)

        # TODO: The actual wav file is being made but the open in finder feature is bugged...
        self.openButton = tk.Button(master, text="Open in Finder", command=self.openFileInFinder)

        # Place GUI elements
        self.filePathEntry.grid(row=0, column=0, columnspan=2, pady=5)
        self.browseButton.grid(row=0, column=2, pady=5)
        self.runButton.grid(row=1, column=0, columnspan=3, pady=10)
        self.statusLabel.grid(row=2, column=0, columnspan=4, pady=5)
        self.openButton.grid(row=5, column=0, columnspan=4, pady=10)

    def browseFile(self):
        # Opens a file dialog to select an input WAV file.
        filePath = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        self.filePathEntry.delete(0, tk.END)
        self.filePathEntry.insert(0, filePath)

    def runProcess(self):
        # Initiates the granular synthesis process.
        inputFilePath = self.filePathEntry.get()

        try:
            if not inputFilePath:
                raise ValueError("Please enter a valid WAV file.")

            if not inputFilePath.lower().endswith('.wav'):
                raise ValueError("Invalid file format. Please select a WAV file.")

            outputFilename = self.outputEntry.get() or "output"

            seed = int(time.time() * 1000)
            self.statusLabel.config(text="Please Stand By...")

            def updateProgress(progress):
                self.master.update_idletasks()

            Phidelity.granularSynthesis(inputFilePath, outputFilename, seed, progressCallback=updateProgress)

            self.statusLabel.config(text="FINISHED")
            self.openButton.config(state=tk.NORMAL)

        except Exception as e:
            self.statusLabel.config(text=str(e))

    def openFileInFinder(self):
        # Opens the generated WAV file in Finder.
        outputFilename = self.outputEntry.get() or "output"
        outputFilePath = os.path.join(os.path.dirname(self.filePathEntry.get()), f"{outputFilename}.wav")
        import subprocess
        subprocess.run(["open", "-R", outputFilePath])


if __name__ == "__main__":
    root = tk.Tk()
    app = PhidelityApp(root)
    root.mainloop()

