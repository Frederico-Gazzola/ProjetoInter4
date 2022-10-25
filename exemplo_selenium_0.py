# Vamos utilizar o pacote Selenium Python para manipular browsers via código:
# https://selenium-python.readthedocs.io/
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install selenium
#
# Depois de instalar o Selenium Python, é necessário instalar o driver referente
# ao browser que será utilizado:
#
# Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
# Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Firefox: https://github.com/mozilla/geckodriver/releases
# Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/
#
# Depois de baixar o driver, garantir que ele seja instalado/descompactado em uma
# pasta que pertença ao PATH global do sistema (de preferência com o VS Code fechado).
#
# No Linux, podem ser as pastas /usr/bin, /usr/local/bin ou outra que esteja no PATH.
# Para adicionar outra pasta ao PATH, basta editar o arquivo ~/.bashrc, e adicionar
# uma linha parecida com essa:
# export PATH=/nova/pasta/para/adicionar:${PATH}
#
# No Windows, o PATH pode ser editado clicando com o botão direito sobre o ícone do
# Computador (no Windows Explorer), depois no menu "Propriedades", em seguida "Configurações
# avançadas do sistema" e, por fim, em "Variáveis de Ambiente".
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine('mysql+mysqlconnector://root:root@localhost/games')

driver = webdriver.Chrome()

jogos = [
	{
		'id': 1,
		'nome': 'Disco Elysium',
		'link': 'https://steamcharts.com/app/632470'
	},
	{
		'id': 2,
		'nome': 'Apex Legends',
		'link': 'https://steamcharts.com/app/1172470'
	},
	{
		'id': 3,
		'nome': 'Hollow Knight',
		'link': 'https://steamcharts.com/app/367520'
	},
	{
		'id': 4,
		'nome': 'Destiny 2',
		'link': 'https://steamcharts.com/app/1085660'
	},
	{
		'id': 5,
		'nome': 'The Witcher 3',
		'link': 'https://steamcharts.com/app/292030'
	},
	{
		'id': 6,
		'nome': 'Cyberpunk 2077',
		'link': 'https://steamcharts.com/app/1091500'
	},
	{
		'id': 7,
		'nome': 'FIFA 22',
		'link': 'https://steamcharts.com/app/1506830'
	},
	{
		'id': 8,
		'nome': 'Sea of Thieves',
		'link': 'https://steamcharts.com/app/1172620'
	},
	{
		'id': 9,
		'nome': 'VRChat',
		'link': 'https://steamcharts.com/app/438100'
	},
	{
		'id': 10,
		'nome': 'Hades',
		'link': 'https://steamcharts.com/app/1145360'
	},
	{
		'id': 11,
		'nome': 'Elden Ring',
		'link': 'https://steamcharts.com/app/1245620'
	},
	{
		'id': 12,
		'nome': 'GTA 5',
		'link': 'https://steamcharts.com/app/271590'
	},

]

for jogo in jogos:
	driver.get(jogo['link'])

	span = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, '#app-heading > .app-stat + .app-stat > .num'))
	)

	pico = int(span.text.replace(',', ''))

	print(pico)

	with Session(engine) as sessao, sessao.begin():
		sessao.execute(text("INSERT INTO raspagem (id_jogo, acessos, data) VALUES (:id_jogo, :acessos, date_add(now(), INTERVAL -1 DAY))"), {
			'id_jogo': jogo['id'],
			'acessos': pico
		})

driver.close()
