import json
import random
import os
from typing import List

class WordService:
    def __init__(self, words_file: str):
        self.words_file = words_file
        self.words: List[str] = []
        self.load_words()

    def load_words(self):
        if not os.path.exists(self.words_file):
            self.words = []
            return
        
        with open(self.words_file, 'r', encoding='utf-8') as f:
            self.words = json.load(f)

    def get_random_words(self, count: int = 1) -> List[str]:
        if not self.words:
            return ["Нет слов в базе"]
        
        # Если слов меньше, чем запрашивается, возвращаем все, что есть, перемешав
        if len(self.words) <= count:
            random.shuffle(self.words)
            return self.words
            
        return random.sample(self.words, count)
