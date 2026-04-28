from faster_whisper import WhisperModel
import speech_recognition as sr
import logging
import os 
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


logging.basicConfig(level=logging.WARNING, format='%(message)s') # print karega, and useful when we ill get andy wrror

print("whishper model load ho raha hai...")

WHISPER_MODEL = WhisperModel("base", device="cpu", compute_type="int8")
