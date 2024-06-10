from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import spacy
from collections import Counter
import random
import PyPDF2
from PyPDF2 import PdfReader
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

app = Flask(__name__)
Bootstrap(app)

# Load spaCy English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Load pre-trained BERT model and tokenizer from local directory
local_model_path = './models/bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(local_model_path)
bert_model = BertModel.from_pretrained(local_model_path, ignore_mismatched_sizes=True)

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def find_similar_words_bert(bert_embeddings, word, top_n=5):
    word_embedding = get_bert_embeddings(word)
    similarities = {other_word: np.dot(word_embedding, bert_embeddings[other_word].T) for other_word in bert_embeddings if other_word != word}
    return sorted(similarities, key=similarities.get, reverse=True)[:top_n]

def generate_mcqs(text, num_questions=5):
    if text is None:
        return []

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    num_questions = min(num_questions, len(sentences))
    selected_sentences = random.sample(sentences, num_questions)
    mcqs = []

    bert_embeddings = {token.text: get_bert_embeddings(token.text) for token in doc if token.pos_ == "NOUN"}

    for sentence in selected_sentences:
        sent_doc = nlp(sentence)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]
        if len(nouns) < 2:
            continue
        noun_counts = Counter(nouns)
        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]
            question_stem = sentence.replace(subject, "______")
            answer_choices = [subject]
            distractors = find_similar_words_bert(bert_embeddings, subject, top_n=3)
            while len(distractors) < 3:
                distractors.append("[Distractor]")
            random.shuffle(distractors)
            for distractor in distractors[:3]:
                answer_choices.append(distractor)
            random.shuffle(answer_choices)
            correct_answer = chr(64 + answer_choices.index(subject) + 1)
            mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = ""
        if 'files[]' in request.files:
            files = request.files.getlist('files[]')
            for file in files:
                if file.filename.endswith('.pdf'):
                    text += process_pdf(file)
                elif file.filename.endswith('.txt'):
                    text += file.read().decode('utf-8')
        else:
            text = request.form['text']

        num_questions = int(request.form['num_questions'])
        mcqs = generate_mcqs(text, num_questions=num_questions)
        mcqs_with_index = [(i + 1, mcq) for i, mcq in enumerate(mcqs)]
        return render_template('mcqs.html', mcqs=mcqs_with_index)

    return render_template('index.html')

def process_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        text += page_text
    return text

if __name__ == '__main__':
    app.run(debug=True)
