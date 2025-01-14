import pyautogui
import time
import pandas as pd

pyautogui.press('win')
pyautogui.write('chrome')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.write('https://dlp.hashtagtreinamentos.com/python/intensivao/login')
pyautogui.press('enter')

time.sleep(1)

pyautogui.click(x=984, y=-840) # posição do campo e-mail
pyautogui.write('gabitrevis@gmail.com')
pyautogui.press('tab') # campo de senha
pyautogui.write('senha')
pyautogui.press('tab') # botão de login
pyautogui.press('enter')    


df = pd.read_csv('./aula 1/produtos.csv') # path arquivo

print(df.head()) # visualizando head do dataframe
time.sleep(1)

for row in df.index:
    pyautogui.click(x=1156, y=-962)
# cadastrando produtos
    codigo = df.loc[row, 'codigo']
    pyautogui.write(str(codigo)) # codigo
    pyautogui.press('tab')

    marca = df.loc[row, 'marca']
    pyautogui.write(str(marca)) # marca
    pyautogui.press('tab')

    tipo = df.loc[row, 'tipo']
    pyautogui.write(str(tipo)) # tipo
    pyautogui.press('tab')

    categoria = df.loc[row, 'categoria']
    pyautogui.write(str(categoria)) # categoria
    pyautogui.press('tab')

    preco = df.loc[row, 'preco_unitario']
    pyautogui.write(str(preco)) # preço
    pyautogui.press('tab')

    custo = df.loc[row, 'custo']
    pyautogui.write(str(custo)) # custo
    pyautogui.press('tab')

    obs = str(df.loc[row, 'obs'])
    if obs !='nan':
        pyautogui.write(str(obs)) # obs
    pyautogui.press('tab')

    pyautogui.press('enter') # botão enviar
    pyautogui.scroll(-700)
    time.sleep(3)
    pyautogui.scroll(700)