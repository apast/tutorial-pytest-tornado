---
layout: post
title:  "Sobre Testes, TDD, pytest, web e Tornado Web!"
date:   2018-04-03 18:52:40 -0300
categories: test tdd pytest tornado python
---

Olá!


### Pré-requisitos:
+ Firefox instalado e atualizado
+ python
+ pip
+ Google Chrome (opcional)
+ geckodriver (https://github.com/mozilla/geckodriver/releases)
+ chromedriver (https://chromedriver.storage.googleapis.com/index.html?path=2.37/)


### Pré-instalação:
```bash
sudo pip install pyenv
```


### Perguntas para conhecer participantes:
+ Quem desenvolve em python?
+ Quem desenvolve com testes?
+ Quem conhece testes?
+ Quem usa o pytest?
+ Quem trabalha com web?
+ Quem conhece Selenium?
+ Quem conhece Tornado?
+ Quem trabalha com Tornado?


### Por que testes?
+ Apresentar cenário caótico de desenvolvimento de uma app web simples
+ Em seguida sugere uma mudança no cenário


### Testes

Vamos construir um exemplo de teste simples sobre uma página web:

```python
# src/test_functional.py

from selenium import webdriver

browser = webdriver.Firefox()
response = browser.get("http://localhost:8000")

assert "dimdim converter" in browser.title
```


Neste código, temos três fases:

+ setup: abrimos um navegador web
+ execução: visitamos uma página
+ verificação: esperamos uma página contendo 'dimdim converter'


Vamos executar nosso script de testes:

```bash
python test_functional.py
```

Um erro ocorre, pois as condições esperadas não estão satisfeitas.

A mensagem de erro impressa no console informa que o endereço acessado não pode ser alcançado.

Então, vamos construir uma solução para eliminarmos esta mensagem e chegarmos a um programa funcionando.

Em python, possuimos um servidor web pronto para ser utilizado, através do módulo 'http.server'

Para iniciar nosso servidor web, execute o seguinte comando em um terminal auxiliar:

```bash
python -m http.server 8000
```

Agora, reexecute o teste:

```bash
python test_functional.py
```

Evolução! O erro anterior não ocorre mais

Neste ponto, montaremos uma página simples para atender a esta requisição.

Crie um arquivo chamado src/index.html com o seguinte conteúdo:

```html
<!-- src/index.html -->
<html>
  <head>
    <title>dimdim converter</title>
  </head>
</html>
```

Executando o teste novamente:

```bash
python test_functional.py
```

Sucesso!!

Nosso teste funcionou, nenhum erro foi reportado ou outra mensagem foi impressa.

Percebe-se que sempre uma nova instância do navegador é aberta a cada chamada e este mantêm-se aberto.

Para fechá-lo sempre que o teste funcionar com sucesso, podemos chamar o método browser.quit() do Selenium.

```python
# test_functional.py
from selenium import webdriver

# setup: inicializações
browser = webdriver.Firefox()

# execução: exercitando o código
response = browser.get("http://localhost:8000")

# verificações de expectativas
assert "dimdim converter" in browser.title

# encerramento: liberação de recursos (cleanup)
browser.quit()
```


Mas, se ocorrer algum erro, ele ficará aberto. Podemos colocar nossa assertion dentro de um bloco try...finally, garantindo que sempre fechará.


```python
# test_functional.py
from selenium import webdriver

# setup: inicializações
browser = webdriver.Firefox()

# execução: exercitando o código
response = browser.get("http://localhost:8000")

try:
    # verificações de expectativas
    assert "dimdim converter" in browser.title
finally:
    # encerramento: liberação de recursos (cleanup)
    browser.quit()

try:
    assert "abracadabra" not in browser.title
finally:
    browser.quit()
```

Adotada esta estratégia, percebe-se que esta manutenção de setup e finalização podem ser redundantes, não-escalável ou irregular.


### Módulo unittest

Podemos reorganizar um pouco nosso teste, utilizando o módulo unittest, nativa do python.

Neste caso, a estrutura básica de teste é Orientada a Objetos. Portanto, devemos declarar uma Classe de Teste, herdando unittest.TestCase, além de sobrescrever alguns métodos auxiliares.

```python
# pytest_functional.py

import unittest

from selenium import webdriver


class ConverterPageTestCase(unittest.TestCase):

    def setUp(self):
      self.browser = webdriver.Firefox()

    def tearDown(self):
      self.browser.quit()

    def test_title_should_be_for_converter(self):
      self.browser.get("http://localhost:8000")
      self.assertIn("dimdim converter", self.browser.title)

    def test_content_should_not_be_empty(self):
        response = self.browser.get("http://localhost:8000")
      self.assertGreater(len(self.browser.find_element_by_tag_name("body").text), 0)
```


Para executar o código acima, digite em seu console:


```bash
python -m unittest test_functional.py
```


Note que algumas mensagens serão apresentadas na tela, como o total de testes executados, sucessos e falhas.


Um error ocorrerá no teste `test_content_should_not_be_empty`, onde é verificado se há algo dentro da tag <body>. Para este teste funcionar, devemos modificar nosso arquivo HTML original.

```html
<html>
<head>
    <title>dimdim converter</title>
</head>
<body>abc</body>
</html>
```


Reexecutando nosso script:


```bash
python -m unittest test_functional.py
```

Sucesso novamente!

Nesta versão, organizamos nosso código utilizando unittest, separamos a fase de inicialização, a fase de limpeza de recursos e nossos testes.


### Test Driven Development
Sobre testes:

Perceba a evolução em nosso código seguindo um ciclo regular:

https://twitter.com/bitfield/status/980843303246602240

1. Write just enough of a failing test to specify the feature / reproduce the bug ("Red")
2. Write just enough production code to make the test pass ("Green")
3. Tidy and reorganize code and tests ("Refactor")
4. Stop


Porém, adicionamos bastante código ao redor. Isto pode ser chamado de 'boillerplate code'. Algo muito declarativo, além de algumas aberturas para dependências de recursos não tão comuns a todos os testes.


### pytest
Como alternativa, introduzimos o uso da biblioteca 'py.test', atualmente chamada simplesmente: 'pytest'. Muito sobre a biblioteca pode ser encontrado na página oficial do projeto, <a href="https://pytest.org">https://pytest.org</a>.


Vamos reescrever os testes anteriores seguindo práticas adotadas pela biblioteca pytest

```python
from selenium import webdriver


def test_title_should_be_for_converter():
    browser = webdriver.Firefox()
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title
    browser.quit()


def test_content_should_not_be_empty():
    browser = webdriver.Firefox()
    browser.get("http://localhost:8000")
    assert len(browser.find_element_by_tag_name("body").text) > 0
    browser.quit()
```

Para executar este código, será necessário instalar a biblioteca pytest. Para isso, digite em seu terminal:

```bash
pip install pytest
```

Em seguida, execute o comando:

```bash
pytest
```

Note a diferença entre os resultados do unittest e a execução do pytest.

Nesta nova versão do código, temos alguns pontos a notar:

Desta forma, o código está mais simples, sem dependência do unittest. Alguns detalhes podemos identificar:
+ Pro: Retiramos import unittest
+ Pro: Retiramos os métodos setUp e tearDown gerais da classe;
+ Con: Introduzimos a inicialização e fechamento do navegador dentro dos testes. Será que podemos fazer melhor? Sim, normalmente sim.
+ Con: Se ocorrer um erro, navegador permanecerá aberto


Para contornar o problema do navegador aberto, mesmo durante após erro, podemos contornar ingenuamente da seguinte maneira:

```python
from selenium import webdriver


def test_title_should_be_for_converter():
    browser = webdriver.Firefox()
    try:
        browser.get("http://localhost:8000")
        assert "dimdim converter" in browser.title
    finally:
        browser.quit()


def test_content_should_not_be_empty():
    browser = webdriver.Firefox()
    try:
        browser.get("http://localhost:8000")
        assert len(browser.find_element_by_tag_name("body").text) > 0
    finally:
        browser.quit()
```


Retornamos ao boilerplate code inicial, com redundância de código e controles irregulares de recursos.


### @pytest.fixture

Para contornar estes pontos Cons, podemos adotar uma nova técnica de injeção de dependência, denominada "fixture" no contexto do pytest. Pela definição da documentação oficial, o conjunto de fixtures é um modo a prover uma base fixa onde os testes podem ser executados com confiança e repetidamente. Algumas características destas fixtures são:

. Nomes explícitos, disponíveis facilmente aos testes
. Modularidade: São funções simples, que podem ser construídas utilizando outras fixtures ou recursos
. Escalabilidade


No código anterior, identificamos o objeto 'browser' como um recurso comum e repetido a ambos os testes, além de precisarmos fechá-lo sempre, independente do resultado do teste.

Este será o primeiro recurso extraído a uma nova fixture.


```python
import pytest

from selenium import webdriver


@pytest.fixture
def browser():
    browser = webdriver.Firefox()
    yield browser  # atenção no uso do yield
    browser.quit()


def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
    assert len(browser.find_element_by_tag_name("body").text) > 0
```


Para cada teste utilizando o navegador, uma nova janela é aberta no ambiente do usuário, a navegação é simulada e o navegador é encerrado.

Podemos evitar esta abertura executando o navegador em background, sem interface, utilizando o modo "headless". Isto simplifica o fluxo de execução.


Fixtures podem ser compostas por outras fixtures. Por exemplo, se quisermos executar os testes em outro navegador, como o Chrome, por exemplo. Podemos adicionar outras fixtures para cada navegador.

A seguir, um exemplo completo com fixtures compostas:

```python
import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture
def browser_firefox():
    options = FirefoxOptions()
    options.set_headless(headless=True)
    return webdriver.Firefox(firefox_options=options)


@pytest.fixture
def browser_chrome():
    options = ChromeOptions()
    options.set_headless(headless=True)
    return webdriver.Chrome(chrome_options=options)


@pytest.fixture
def browser(browser_firefox):
    b = browser_firefox
    yield b
    b.quit()


def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
    assert len(browser.find_element_by_tag_name("body").text) > 0
```

Então, vamos evoluir nosso conversor com algumas novas features.

Nossa aplicação deve atender ao usuário, são:

+ Na primeira visita do usuário, a tela estará com a moeda de origem Dolar (USD) selecionada, com o valor 1 e moeda destino Real (BRL);
+ Com a moeda de origem em USD, quantidade 1 e moeda destino BRL, ao enviar o formulario, devera retornar a cotacao da unidade;
+ O usuário escolhe uma moeda de origem, inserir o valor e uma moeda de destino. Clica em enviar e uma nova página será desenhada com o valor do campo preenchido e um resultado;
+ O usuario pode escolher entre Real e Dolar;

Abaixo, iniciamos a estender o código com estas novas funcionalidades.

```python
import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture
def browser_firefox():
    options = FirefoxOptions()
    options.set_headless(headless=True)
    return webdriver.Firefox(firefox_options=options)


@pytest.fixture
def browser_chrome():
    options = ChromeOptions()
    options.set_headless(headless=True)
    return webdriver.Chrome(chrome_options=options)


@pytest.fixture
def browser(browser_firefox):
    b = browser_firefox
    yield b
    b.quit()


def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
	assert len(browser.find_element_by_tag_name("body").text) > 0


def test_initial_fields_setup_should_be_one_usd_to_brl(browser):
    browser.get("http://localhost:8000")
    assert "USD" == browser.find_element_by_css_selector("select.from_currency").text
    assert "BRL" == browser.find_element_by_css_selector("select.to_currency").text
    assert "1" == browser.find_element_by_css_selector("input").text
```

### Arquivo conftest.py

Perceba que este código começa a ficar mais complexo, com elementos não inerentes ao teste funcional, mas como suporte. A biblioteca pytest utiliza um arquivo chamado `conftest.py` que pode ser colocar na raíz de cada módulo.

Em nosso caso, podemos mover as fixtures relacionadas ao `browser` Selenium para este arquivo.

Teremos um novo arquivo:

```python
# src/conftest.py

import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture
def browser_firefox():
    options = FirefoxOptions()
    options.set_headless(headless=True)
    return webdriver.Firefox(firefox_options=options)


@pytest.fixture
def browser_chrome():
    options = ChromeOptions()
    options.set_headless(headless=True)
    return webdriver.Chrome(chrome_options=options)


@pytest.fixture
def browser(browser_firefox):
    b = browser_firefox
    yield b
    b.quit()

```

```python
# src/test_functional.py

def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
	assert len(browser.find_element_by_tag_name("body").text) > 0


def test_initial_fields_setup_should_be_one_usd_to_brl(browser):
    browser.get("http://localhost:8000")
    assert "USD" == browser.find_element_by_css_selector("select.from_currency").text
    assert "BRL" == browser.find_element_by_css_selector("select.to_currency").text
    assert "1" == browser.find_element_by_name("from_amount").get_attribute("value")


def test_one_usd_to_brl_should_return_unitary_conversion(browser):
    browser.get("http://localhost:8000")
    browser.find_element_by_css_selector("select.from_currency").set_attribute("value", "USD")
    browser.find_element_by_css_selector("select.to_currency").set_attribute("value", "BRL")
    browser.find_element_by_name("from_amount").set_attribute("value", "1")

	browser.find_element_by_id("convert_form").submit()

	assert len(browser.find_element_by_css_selector("to_amount").text)
```

O arquivo resultante `test_functional.py` está simplificado, sem dependências ou complexidade não inerente aos testes funcionais. O novo arquivo `conftest.py` torna disponíveis recursos que outros módulos podem utilizar.

Desta forma, ao iniciar o teste, o `pytest` busca por por aquivos nomeados `conftest.py` na árvore de diretórios, e carrega seus conteúdos isolados pela hierarquia dos módulos e disponibiliza na sessão dos testes em execução.

Executando este teste, precisaremos atender às expectativas descritas no novo caso test_initial_fields_setup_should_be_one_usd_to_brl. Isto pode ser feito editando o arquivo HTML `index.html`.

```html
<html>
	<head><title>dimdim converter</title></head>
	<body>
		<select class="from_currency">
			<option value="USD">Dolar</option>
		</select>
		<input type="text" name="from_amount" caption="amount" value="1"/>
		<select class="to_currency">
			<option value="BRL">Real</option>
		</select>
	</body>
</html>
```

## Pattern [PageTest](https://martinfowler.com/bliki/PageObject.html)

Neste momento, nosso teste cresce, com comandos redundantes para extração de elementos. Martin Fowler apresenta o padrão PageObject. Este padrao encapsula a complexidade de páginas, expondo funcionalidades públicas, acessos a campos comuns. Isto é uma melhoria em nosso teste, remoção de duplicidades.

Modificando nosso código de testes funcionais, teremos:

```python
# file test_functional.py
import pytest


@pytest.fixture
def home_pageobject(browser):
    return HomePageObject(browser)


class HomePageObject():

    def __init__(self, browser):
        self.browser = browser
        self.browser.get("http://localhost:8000")

    def get_from_currency_value(self):
        return self.browser.find_element_by_css_selector("select.from_currency").get_attribute("value")

    def get_to_currency_value(self):
        return self.browser.find_element_by_css_selector("select.to_currency").get_attribute("value")

    def get_from_amount_value(self):
        return self.browser.find_element_by_name("from_amount").get_attribute("value")

    def get_to_amount_value(self):
        return self.browser.find_element_by_css_selector(".to_amount").text

    def set_to_currency_value(self, curr):
        self.browser.find_element_by_css_selector("select.to_currency").set_attribute("value", curr)

    def set_from_amount_value(self, value):
        self.browser.find_element_by_name("from_amount").set_attribute("value", value)

    def submit_form(self):
        self.browser.find_element_by_id("convert_form").submit()


def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
    assert len(browser.find_element_by_tag_name("body").text) > 0


def test_initial_fields_setup_should_be_one_usd_to_brl(home_pageobject):
    assert "USD" == home_pageobject.get_from_currency_value()
    assert "BRL" == home_pageobject.get_to_currency_value()
    assert "1" == home_pageobject.get_from_amount_value()


def test_one_usd_to_brl_should_return_unitary_conversion(home_pageobject):
    assert "1" == home_pageobject.get_to_amount_value()
```

E agora, um HTML que atende ao nosso teste.

```html
<html>
	<head><title>dimdim converter</title></head>
	<body>
		<select class="from_currency">
			<option value="USD">Dolar</option>
		</select>
		<input type="text" name="from_amount" caption="amount" value="1"/>
		<select class="to_currency">
			<option value="BRL">Real</option>
		</select>
		<div class="to_amount">1</div>
	</body>
</html>
```

Se modificarmos adicionarmos um novo teste, dobrando o valor de entrada, então a expectativa no valor retornado pela conversão deve dobrar também.

Então, escrevemos mais um teste.

```python
# file test_functional.py
...

def test_two_usd_should_return_double_value_in_brl(home_pageobject):
	home_pageobject.set_from_amount_value("2")
	home_pageobject.submit()

	assert "2" == home_pageobject.get_to_amount_value()

```
