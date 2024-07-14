## CDRM-Project
 ![forthebadge](https://forthebadge.com/images/badges/uses-html.svg) ![forthebadge](https://forthebadge.com/images/badges/uses-css.svg) ![forthebadge](https://forthebadge.com/images/badges/uses-javascript.svg) ![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
 ## O que é isso?

Uma aplicação web open source escrita em Python para descriptografar conteúdos protegidos por Widevine.

## Pré-requisitos

- [Python](https://www.python.org/downloads/) com PIP instalado

  > Python 3.12 foi usado no momento da escrita
- Módulo de Descriptografia de Conteúdo L1/L3 provisionado no formato .WVD usando [pyWidevine](https://github.com/devine-dl/pywidevine)
 
## Instalação
 
- Abra seu terminal e navegue até onde você gostaria de armazenar a aplicação
- Crie um novo ambiente virtual Python usando `python -m venv .venv`
- Mude de diretório para a nova pasta `.venv`
- Ative o ambiente virtual

  > Windows - mude de diretório para a pasta `Scripts` e então execute `activate.bat`
  >
  > Linux - execute `source bin/activate`

- Instale as dependências Python `pip install -r requirements.txt`
- Coloque seu arquivo .WVD em `/databases/WVDs`
- Execute a aplicação `python main.py`