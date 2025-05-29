import re
import zipfile
from collections import defaultdict


def analyze_text(input_file, output_file, zip_name):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    target_length = int(input("Введите длину слов для замены: "))
    modified_text = re.sub(
        rf'\b\w{{{target_length}}}\b',
        lambda m: m.group()[:-3] + '$' * 3,
        text
    )

    # Поиск времени
    times = re.findall(r'\b(?:[01]\d|2[0-3]):[0-5]\d\b', text)

    # Статистика
    words = re.findall(r'\b\w+\b', text)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Сбор результатов
    result = [
        "=== Результаты анализа ===",
        f"1. Найдено временных меток: {len(times)} ({', '.join(times)})",
        f"2. Слов максимальной длины: {max_length_words(words)}",
        f"3. Слова перед запятой/точкой: {', '.join(words_before_punctuation(text))}",
        f"4. Самое длинное слово на 'e': {longest_word_ending_e(words)}",
        "\nОбщая статистика:",
        f"• Предложений: {len(sentences)}",
        f"• По типам: {sentence_types(sentences)}",
        f"• Средняя длина предложения: {avg_sentence_length(sentences):.1f}",
        f"• Средняя длина слова: {avg_word_length(words):.1f}",
        f"• Смайликов: {count_smileys(text)}"
    ]

    # Сохранение и архивация
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join([modified_text, '\n'] + result))

    with zipfile.ZipFile(zip_name, 'w') as zf:
        zf.write(output_file)
        info = zf.getinfo(output_file)
        print(f"Файл '{info.filename}' ({info.file_size} байт) добавлен в архив")


def max_length_words(words):
    lengths = [len(w) for w in words]
    return len([l for l in lengths if l == max(lengths)])


def words_before_punctuation(text):
    return re.findall(r'\b\w+\b(?=\s*[,\.])', text)


def longest_word_ending_e(words):
    e_words = [w for w in words if w.lower().endswith('e')]
    return max(e_words, key=len) if e_words else 'Нет'


def sentence_types(sentences):
    types = defaultdict(int)
    for s in sentences:
        types['повествовательные'] += s.endswith('.')
        types['вопросительные'] += s.endswith('?')
        types['побудительные'] += s.endswith('!')
    return ', '.join([f'{k}: {v}' for k, v in types.items()])


def avg_sentence_length(sentences):
    words = [len(re.findall(r'\w+', s)) for s in sentences]
    return sum(words) / len(sentences) if sentences else 0


def avg_word_length(words):
    return sum(len(w) for w in words) / len(words) if words else 0


def count_smileys(text):
    return len(re.findall(r'[:;]-*([()\[\]])\1*', text))


analyze_text('input.txt', 'output.txt', 'results.zip')
