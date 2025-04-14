
from flask import Flask, render_template_string, request, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure random key!
csrf = CSRFProtect(app)

# --- Database (in-memory) ---
marriages = []
capybaras = []
swim_classes = []
mandarins = []

# --- Forms ---
class MarriageForm(FlaskForm):
    partner1 = StringField('Партнер 1 (Имя)', validators=[DataRequired()])
    partner2 = StringField('Партнер 2 (Имя)', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать Брак')

class CapybaraForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст (в днях)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Добавить Капибару')

class SwimForm(FlaskForm):
    capybara_name = StringField('Имя Капибары', validators=[DataRequired()])
    date = StringField('Дата (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Записаться')

class MandarinForm(FlaskForm):
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    address = StringField('Адрес Доставки', validators=[DataRequired()])
    submit = SubmitField('Купить')


# --- Templates (all in Python strings) ---
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #B0E2FF; /* Light Blue */
            text-align: center;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 80%;
            margin: 20px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
        }}
        .capybara-image {{
            max-width: 300px;
            height: auto;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .menu {{
            list-style: none;
            padding: 0;
            margin-top: 20px;
        }}
        .menu li {{
            margin: 10px 0;
        }}
        .menu a {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        .menu a:hover {{
            background-color: #0056b3;
        }}
        .form-container {{
            width: 50%;
            margin: 20px auto;
            padding: 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            text-align: left;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        input[type="text"],
        input[type="number"] {{
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        input[type="submit"] {{
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        input[type="submit"]:hover {{
            background-color: #45a049;
        }}
        .error {{
            color: red;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Капибаро-ГосУслуги</h1>
        <img class="capybara-image" src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Capybara_%28Hydrochoerus_hydrochaeris%29.JPG" alt="Капибара">
        {content}
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<ul class="menu">
    <li><a href="{marriage_url}">Регистрация Брака</a></li>
    <li><a href="{capybara_url}">Добавить Капибару</a></li>
    <li><a href="{swim_url}">Записаться на Плаванье</a></li>
    <li><a href="{mandarin_url}">Купить Мандарины</a></li>
</ul>
"""

FORM_TEMPLATE = """
    <div class="form-container">
        <h2>{form_title}</h2>
        <form method="POST">
            {form.csrf_token}
            {form_fields}
            <input type="submit" value="{submit_label}">
        </form>
    </div>
"""

LIST_TEMPLATE = """
    <h2>{list_title}</h2>
    <ul>
        {list_items}
    </ul>
    <a href="/">Вернуться на Главную</a>
"""

# --- Routes ---

@app.route("/")
def index():
    """Main page."""
    content = INDEX_TEMPLATE.format(
        marriage_url=url_for('marriage'),
        capybara_url=url_for('add_capybara'),
        swim_url=url_for('swim'),
        mandarin_url=url_for('buy_mandarin')
    )
    return render_template_string(BASE_TEMPLATE.format(title="Капибаро-ГосУслуги", content=content))


@app.route("/marriage", methods=['GET', 'POST'])
def marriage():
    """Marriage Registration."""
    form = MarriageForm()
    if form.validate_on_submit():
        marriages.append({
            'partner1': form.partner1.data,
            'partner2': form.partner2.data
        })
        return redirect(url_for('list_marriages'))

    form_fields = ""
    for field in form:
        if field.widget.input_type != 'hidden':
            form_fields += f"<label>{field.label.text}</label>{field()}<br>"

    content = FORM_TEMPLATE.format(
        form_title="Регистрация Брака",
        form=form,
        form_fields=form_fields,
        submit_label="Зарегистрировать"
    )
    return render_template_string(BASE_TEMPLATE.format(title="Регистрация Брака", content=content))


@app.route("/list_marriages")
def list_marriages():
    """List of Marriages."""
    list_items = ""
    for marriage in marriages:
        list_items += f"<li>{marriage['partner1']} & {marriage['partner2']}</li>"
    content = LIST_TEMPLATE.format(list_title="Список Браков", list_items=list_items)
    return render_template_string(BASE_TEMPLATE.format(title="Список Браков", content=content))


@app.route("/add_capybara", methods=['GET', 'POST'])
def add_capybara():
    """Add Capybara."""
    form = CapybaraForm()
    if form.validate_on_submit():
        capybaras.append({
            'name': form.name.data,
            'age': form.age.data
        })
        return redirect(url_for('list_capybaras'))

    form_fields = ""
    for field in form:
        if field.widget.input_type != 'hidden':
            form_fields += f"<label>{field.label.text}</label>{field()}<br>"

    content = FORM_TEMPLATE.format(
        form_title="Добавить Капибару",
        form=form,
        form_fields=form_fields,
        submit_label="Добавить"
    )
    return render_template_string(BASE_TEMPLATE.format(title="Добавить Капибару", content=content))


@app.route("/list_capybaras")
def list_capybaras():
    """List of Capybaras."""
    list_items = ""
    for capybara in capybaras:
        list_items += f"<li>{capybara['name']} ({capybara['age']} дней)</li>"
    content = LIST_TEMPLATE.format(list_title="Список Капибар", list_items=list_items)
    return render_template_string(BASE_TEMPLATE.format(title="Список Капибар", content=content))


@app.route("/swim", methods=['GET', 'POST'])
def swim():
    """Swim Class Registration."""
    form = SwimForm()
    if form.validate_on_submit():
        swim_classes.append({
            'capybara_name': form.capybara_name.data,
            'date': form.date.data
        })
        return redirect(url_for('list_swims'))

    form_fields = ""
    for field in form:
        if field.widget.input_type != 'hidden':
            form_fields += f"<label>{field.label.text}</label>{field()}<br>"

    content = FORM_TEMPLATE.format(
        form_title="Запись на Плаванье",
        form=form,
        form_fields=form_fields,
        submit_label="Записаться"
    )
    return render_template_string(BASE_TEMPLATE.format(title="Запись на Плаванье", content=content))


@app.route("/list_swims")
def list_swims():
    """List of Swim Classes."""
    list_items = ""
    for swim in swim_classes:
        list_items += f"<li>{swim['capybara_name']} - {swim['date']}</li>"
    content = LIST_TEMPLATE.format(list_title="Список записанных на плаванье", list_items=list_items)
    return render_template_string(BASE_TEMPLATE.format(title="Список записанных на плаванье", content=content))


@app.route("/mandarins", methods=['GET', 'POST'])
def buy_mandarin():
    """Buy Mandarins."""
    form = MandarinForm()
    if form.validate_on_submit():
        mandarins.append({
            'quantity': form.quantity.data,
            'address': form.address.data
        })
        return redirect(url_for('list_mandarins'))

    form_fields = ""
    for field in form:
        if field.widget.input_type != 'hidden':
            form_fields += f"<label>{field.label.text}</label>{field()}<br>"

    content = FORM_TEMPLATE.format(
        form_title="Купить Мандарины",
        form=form,
        form_fields=form_fields,
        submit_label="Купить"
    )
    return render_template_string(BASE_TEMPLATE.format(title="Купить Мандарины", content=content))


@app.route("/list_mandarins")
def list_mandarins():
    """List of Mandarin Orders."""
    list_items = ""
    for mandarin in mandarins:
        list_items += f"<li>{mandarin['quantity']} мандаринов - {mandarin['address']}</li>"
    content = LIST_TEMPLATE.format(list_title="Список Заказов Мандаринов", list_items=list_items)
    return render_template_string(BASE_TEMPLATE.format(title="Список Заказов Мандаринов", content=content))



if __name__ == "__main__":
    app.run(debug=True)
