import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from googletrans import Translator
duration = 5  # секунды записи
sample_rate = 44100
words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}
level = input("Выберите уровень: ").lower()
if level not in words_by_level:
    print("❌ Неверный уровень!")
    exit()
lang = input("Введите код языка для перевода")
score = 0
mistakes = 0
while mistakes < 3:
    word = random.choice(words_by_level[level])
    translator = Translator()
    translated_word = translator.translate(word,dest=lang).text.lower()
    print("\n" + "=" * 30)
    print("🔤 Переведите слово:")
    print(word)
    print("🎤 Говорите...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate,  channels=1 , dtype='int16' , device=2)
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language=lang).lower()
        print("🗣 Вы сказали:", text)
        print("✅ Правильный ответ:", translated_word)
        if text  == translated_word:
            score += 1
            print('Верно!!')
        else:
            mistakes += 1
            print("❌ Ошибка!")
            print(f"Ошибок: {mistakes}/3")
    except sr.UnknownValueError:             
        mistakes += 1
        print("❌ Речь не распознана!")
        print(f"Ошибок: {mistakes}/3")
    except sr.RequestError as e:             
        print(f"Ошибка сервиса: {e}")
    print(f"🏆 Счёт: {score}")
print("\n💀 GAME OVER")
print(f"Ваш итоговый счёт: {score}")

