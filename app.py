import json
import random
from flask import Flask, render_template, redirect, url_for
from forms import SignUpForm, RadioForm, StringForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Объявление глобальных переменных и загрузка словаря из файла
login = ''
score, mistakes = 0, 0
with open('static/vocabulary.json') as file:
    vocabulary = json.load(file)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    global login, score, mistakes
    score, mistakes = 0, 0
    login = ''
    form = SignUpForm()
    if form.validate_on_submit():
        login = form.name.data
        return redirect(url_for("test_1", dword=random.choice(list(vocabulary.keys()))))
    return render_template("index.html", login=login, form=form, score=score, mistakes=mistakes)


@app.route('/test_1/<dword>', methods=['GET', 'POST'])
def test_1(dword):
    global login, score, mistakes
    global vocabulary
    translation = vocabulary[dword]
    values = list(vocabulary.values())
    random.shuffle(values)
    options = [translation]
    # Здесь добираются случайные неверные варианты ответов (0 - верный; 1,2,3 - ложный)
    for option in values:
        if option not in options:
            options.append(option)
        if len(options) >= 4:
            break
    random.shuffle(options)
    form = RadioForm()
    form.choice.label.text = dword
    form.choice.choices = options
    if form.is_submitted():
        if form.choice.data == translation:
            score += 1
            del vocabulary[dword]
            if score >= 5:  # переход на уровень 2
                return redirect(url_for('test_2', dword=random.choice(list(vocabulary.keys()))))
        else:
            mistakes += 1
            if mistakes >= 3:
                return redirect(url_for('game_over'))
        return redirect(url_for('test_1', dword=random.choice(list(vocabulary.keys()))))
    return render_template("test_1.html", login=login, score=score, form=form, mistakes=mistakes)


@app.route('/test_2/<dword>', methods=['GET', 'POST'])
def test_2(dword):
    global login, score, mistakes
    global vocabulary
    form = StringForm()
    form.answer.label.text = dword
    if form.validate_on_submit():
        if form.answer.data == vocabulary[dword]:
            score += 1
            del vocabulary[dword]
            if score >= 10:  # Победа
                return redirect(url_for('game_over'))
        else:
            mistakes += 1
            if mistakes >= 3:
                return redirect(url_for('game_over'))
        return redirect(url_for('test_2', dword=random.choice(list(vocabulary.keys()))))
    return render_template("test_2.html", login=login, score=score, form=form, mistakes=mistakes)


@app.route('/message')
def game_over():
    if score >= 10:
        message = "Вы прошли тест успешно. Молодец!"
    else:
        message = "К сожалению вы не прошли тест. Учите английский."
    return render_template("message.html", message=message, score=score, mistakes=mistakes)


if __name__ == '__main__':
    app.run()
