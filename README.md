# CECTI-SPRINT1_Grup4

# Selenium Tests per a CyberHotSecurity

Aquest codi conté tests automatitzats amb Selenium per al formulari de contacte de la web **CyberHotSecurity**.

## Instal·lació de dependències

pip install -r requirements.txt

## Requisits previs

1. **Navegador Firefox**: El codi està configurat per utilitzar Firefox.
2. **GeckoDriver**: Descarregar des de https://github.com/mozilla/geckodriver/releases
3. **Python 3.7+**

## Configuració del GeckoDriver

### Windows:
1. Descarregar geckodriver.exe
2. Afegir la ruta al PATH del sistema
3. O col·locar geckodriver.exe dins la carpeta del projecte

### Linux/Mac:

# Ubuntu/Debian
sudo apt-get install firefox-geckodriver

# O descarregar manualment i afegir al PATH
export PATH=$PATH:/ruta/al/geckodriver

## Execució dels tests

### Executar tots els tests:
pytest test_simple_firefox.py

### Executar un test específic:
pytest -k "test_02_check_elements_Andrei"

> Nota: Els noms dels tests inclouen els teus noms personalitzats al final (Andrei, Ximo, Lucas) segons la funció de cada test.

## Tests inclosos

1. test_01_page_loads: Comprova que la pàgina de contacte es carrega correctament, mesura el temps de càrrega i guarda una captura.
2. test_02_check_elements_Andrei: Verifica que tots els camps del formulari existeixen i si són obligatoris.
3. test_03_submit_and_required_validation_Ximo: Prova l'enviament correcte del formulari i la validació dels camps obligatoris.
4. test_04_xss_injection_check_Lucas: Comprova un intent bàsic d'injecció XSS (sense executar scripts) i registra evidència si falla.

## Estructura del formulari detectada

- Camp Nom: wpforms-2234-field_1
- Camp Cognoms: wpforms-2234-field_1-last
- Camp Email: wpforms-2234-field_2
- Camp Missatge: wpforms-2234-field_3
- Botó Enviar: wpforms-submit-2234

## Notes importants

- Els tests utilitzen esperes explícites (WebDriverWait) per a més estabilitat.
- El codi gestiona excepcions per evitar fallades inesperades.
- Cada test és independent i pot executar-se de manera separada.
- Es generen captures de pantalla automàticament per documentar els resultats.

## Resultats esperats

- test_01_page_loads: La pàgina es carrega en menys de 30 segons, el títol existeix i es guarda captura.
- test_02_check_elements_Andrei: Tots els camps i botó d'enviament estan presents i es detecten correctament els obligatoris.
- test_03_submit_and_required_validation_Ximo: El formulari s'envia correctament quan tots els camps obligatoris estan plens; fallida si algun està buit.
- test_04_xss_injection_check_Lucas: El payload XSS no s'executa ni es reflecteix al HTML.

## Personalització

Per adaptar a altres navegadors, canviar a setup_class():

# Per Chrome
cls.driver = webdriver.Chrome()

# Per Edge
cls.driver = webdriver.Edge()

> Recorda que el teu script actual està configurat per Firefox amb geckodriver i execució headless.
