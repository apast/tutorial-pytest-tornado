---
layout: post
title:  "Sobre Testes, TDD, pytest, web e Tornado Web!"
date:   2018-04-03 18:52:40 -0300
categories: test tdd pytest tornado python
---

Olá!


### Pré-requisitos:
. Firefox instalado e atualizado
. python
. pip
. Google Chrome (opcional)


### Pré-instalação:
{% highlight sh %}
. sudo pip install pyenv
{% endhighlight %}


### Perguntas para conhecer participantes:
+ Quem desenvolve em python?
+ Quem desenvolve com testes?
+ Quem conhece testes?
+ Quem trabalha com web?
+ Quem conhece Selenium?
+ Quem conhece Tornado?
+ Quem trabalha com Tornado?


### Por que testes?
+ Apresentar cenário caótico de desenvolvimento de uma app web simples
+ Em seguida sugere uma mudança no cenário


### Testes

Vamos construir um exemplo de teste simples sobre uma página web:

{% highlight python %}
# src/test_functional.py

from selenium import webdriver

browser = webdriver.Firefox()
response = browser.get("http://localhost:8000")

assert "dimdim converter" in browser.title
{% endhighlight %}


Neste código, temos três fases:

+ abrimos um navegador web (setup)
+ visitamos uma página (execução)
+ esperamos uma página contendo 'dimdim converter' (verificação)


Vamos executar nosso script de testes:

{% highlight sh %}
python test_functional.py
{% endhighlight %}

Um erro ocorre, pois as condições esperadas não estão satisfeitas.

Então, precisamos construir algo que responda o resultado corretamente.

Em python, possuimos um servidor web pronto para ser utilizado, através do módulo 'http.server'

Neste ponto, montaremos uma página simples para atender a esta requisição.

Crie um arquivo chamado src/index.html com o seguinte conteúdo:

{% highlight html %}
<!-- src/index.html -->
<html><head><title>dimdim converter</title></head></html>
{% endhighlight %}

Para iniciar nosso servidor web, execute:

{% highlight sh %}
python -m http.server 8000
{% endhighlight %}


Reexecute o teste novamente:

{% highlight sh %}
python test_functional.py
{% endhighlight %}

Sucesso!! Nosso teste funcionou, nenhum erro foi reportado ou outra mensagem foi impressa.

Percebe-se que sempre uma nova instância do navegador é aberta a cada chamada e este mantêm-se aberto.

Para fechá-lo sempre que o teste funcionar com sucesso, podemos chamar o método browser.quit() do Selenium.

{% highlight python %}
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
{% endhighlight %}


Mas, se ocorrer algum erro, ele ficará aberto. Podemos colocar nossa assertion dentro de um bloco try...finally, gantindo que sempre fechará.


{% highlight python %}
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
{% endhighlight %}

Adotada esta estratégia, percebe-se que esta manutenção de setup e finalização podem ser redundantes, não-escalável ou irregular.


### Módulo unittest

Podemos reorganizar um pouco nosso teste, utilizando o módulo unittest, existente nativamente no python.

Neste caso, a estrutura básica de teste segue uma estrutura orientada a objetos. Portanto, vamos declarar uma Classe de Teste e alguns métodos auxiliares.

{% highlight python %}
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
{% endhighlight %}


Para executar o código acima, digite em seu console:


{% highlight sh %}
python -m unittest test_functional.py
{% endhighlight %}


Note que algumas mensagens serão apresentadas na tela, como o total de testes executados, sucessos e falhas.


Um error ocorrerá no teste `test_content_should_not_be_empty`, onde é verificado se há algo dentro da tag <body>. Para este teste funcionar, devemos modificar nosso arquivo HTML original.

{% highlight html %}
<html>
<head>
    <title>dimdim converter</title>
</head>
<body>abc</body>
</html>
{% endhighlight %}


Reexecutando nosso script:


{% highlight sh %}
python -m unittest test_functional.py
{% endhighlight %}

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

{% highlight python %}
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
{% endhighlight %}

Para executar este código, será necessário instalar a biblioteca pytest. Para isso, digite em seu terminal:

{% highlight sh %}
pip install pytest
{% endhighlight %}

Em seguida, execute o comando:

{% highlight sh %}
pytest
{% endhighlight %}

Note a diferença entre os resultados do unittest e a execução do pytest.

Nesta nova versão do código, temos alguns pontos a notar:

Desta forma, o código está mais simples, sem dependência do unittest. Alguns detalhes podemos identificar:
+ Pro: Retiramos import unittest
+ Pro: Retiramos os métodos setUp e tearDown gerais da classe;
+ Con: Introduzimos a inicialização e fechamento do navegador dentro dos testes. Será que podemos fazer melhor? Sim, normalmente sim.
+ Con: Se ocorrer um erro, navegador permanecerá aberto


Para contornar o problema do navegador aberto, mesmo durante após erro, podemos contornar ingenuamente da seguinte maneira:

{% highlight python %}
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
{% endhighlight %}


Retornamos ao boilerplate code inicial, com redundância de código e controles irregulares de recursos.


### @pytest.fixture

Para contornar estes pontos Cons, podemos adotar uma nova técnica de injeção de dependência, denominada "fixture" no contexto do pytest. Pela definição da documentação oficial, o conjunto de fixtures é um modo a prover uma base fixa onde os testes podem ser executados com confiança e repetidamente. Algumas características destas fixtures são:

. Nomes explícitos, disponíveis facilmente aos testes
. Modularidade: São funções simples, que podem ser construídas utilizando outras fixtures ou recursos
. Escalabilidade


No código anterior, identificamos o objeto 'browser' como um recurso comum e repetido a ambos os testes, além de precisarmos fechá-lo sempre, independente do resultado do teste.

Este será o primeiro recurso extraído a uma nova fixture.


{% highlight python %}
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
{% endhighlight %}


Para cada teste utilizando o navegador, uma nova janela é aberta no ambiente do usuário, a navegação é simulada e o navegador é encerrado.

Podemos evitar esta abertura executando o navegador em background, sem interface, utilizando o modo "headless". Isto simplifica o fluxo de execução.


Fixtures podem ser compostas por outras fixtures. Por exemplo, se quisermos executar os testes em outro navegador, como o Chrome, por exemplo. Podemos adicionar outras fixtures para cada navegador.

A seguir, um exemplo completo com fixtures compostas:

{% highlight python %}
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
{% endhighlight %}

Então, vamos começar a construir nosso conversor mais próximo do objetivo sério.


Algumas das features que nossa aplicação deve atender ao usuário, são:

. Na primeira visita do usuário, a tela estará vazia, com os campos vazios.

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
