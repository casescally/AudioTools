import os
import time
import librosa
import numpy as np
import soundfile as sf

class Phidelity:
    @staticmethod
    def fibonacciPseudoRandom(seed=None):
        if seed is None:
            seed = int(time.time() * 1000)

        fib = [0, 1]
        for _ in range(100):
            fib.append(fib[-1] + fib[-2])

        index = seed % len(fib)

        return fib[index]

    @staticmethod
    def granularSynthesis(inputFilePath, outputFilePath, seed=None):
        audio, sr = librosa.load(inputFilePath)
        numGrains = 100
        grainSize = 10
        overlap = 0.25

        grains = []

        for _ in range(numGrains):
            start = np.random.randint(0, len(audio) - grainSize)
            grain = audio[start:start + grainSize]
            grains.append(grain)

        hopSize = int(grainSize * (1 - overlap))
        newAudio = np.zeros_like(audio)

        for grain in range(len(grains)):
            start = grain * hopSize
            end = start + grainSize
            newAudio[start:end] += grains[grain][:end - start]

        if len(newAudio) > len(audio):
            newAudio = newAudio[:len(audio)]

        outputFilePath = f"{outputFilePath}.wav"  # Change the file format to WAV
        sf.write(outputFilePath, newAudio, sr)  # Use the original sample rate 'sr'

if __name__ == "__main__":
    inputFilePath = "/Users/Desktop/SoundFile.wav"
    outputFilePath = "testphidelity2"  # Change the file name (without extension)
    seed = int(time.time() * 1000)

    try:
        Phidelity.granularSynthesis(inputFilePath, outputFilePath, seed)
        print("Granular synthesis completed. Output file:", outputFilePath + ".wav")
    except Exception as e:
        print("An error occurred:", str(e))
