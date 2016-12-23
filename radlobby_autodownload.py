import shutil
import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser(factory=mechanize.RobustFactory())

br.open('https://www.radlobby.at/user')

br.select_form(nr=1)

name = br.form.find_control('name')
login = br.form.find_control('pass')
name.value = 'Christoph Bayer'
login.value = 'A!guef77'

br.submit()

br.open('https://www.radlobby.at/node/74/webform-results/download')
br.select_form(nr=1)

#export format
control = br.form.find_control('format')
control.value = ['delimited']
#delimiter
control = br.form.find_control('delimiter')
control.value = [';']
#header keys
control = br.form.find_control('header_keys')
control.value = ['1']
#
## funktioniert nicht, ladet html herunter
#with open('test-download', 'wb') as f:
#        shutil.copyfileobj(br.submit(), f)

download = br.submit()
