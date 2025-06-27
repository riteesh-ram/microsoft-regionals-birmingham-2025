import sounddevice as sd
from scipy.io.wavfile import write
import assemblyai as aai

def record_audio(filename="output.wav", duration=15, sample_rate=44100):
    """Records audio from microphone and saves it as a WAV file."""
    print("🎙️ Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write(filename, sample_rate, audio)
    print(f"✅ Audio recording saved as {filename}")


def transcribe_audio(filename="output.wav"):
    """Transcribes the given WAV file using AssemblyAI."""
    aai.settings.api_key = "df5ab52f47a34c97a968bd829bbf92de"
    transcriber = aai.Transcriber()

    print("🧠 Transcribing audio...")
    transcript = transcriber.transcribe(filename)
    print("📝 Transcription:")
    return transcript.text

if __name__ == "__main__":
    wav_file = "output.wav"
    record_audio(filename=wav_file, duration=5)
    transcribe_audio(filename=wav_file)
