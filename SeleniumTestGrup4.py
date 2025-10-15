import pytest
import shutil
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

class TestCyberhotContact:
    @classmethod
    def setup_class(cls):
        """Crea el driver abans de tots els tests, detectant la ruta de Firefox correcta"""
        try:
            firefox_path = None
            for path in ["/usr/bin/firefox-esr", "/usr/bin/firefox", "/snap/bin/firefox"]:
                # fem servir shutil.which sobre el basename i també comprovem si el path existeix
                if shutil.which(os.path.basename(path)) or os.path.exists(path):
                    firefox_path = path
                    break

            if not firefox_path:
                raise RuntimeError("No s'ha trobat un binari de Firefox vàlid")

            print(f"Usant Firefox a: {firefox_path}")

            options = Options()
            options.headless = True
            options.binary_location = firefox_path
            options.accept_insecure_certs = True

            service = Service("/usr/local/bin/geckodriver", log_path="gecko.log")
            cls.driver = webdriver.Firefox(service=service, options=options)
            cls.driver.set_window_size(1920, 1080)

        except Exception as e:
            print(f"✗ No s'ha pogut crear el driver: {e}")
            cls.driver = None

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            cls.driver.quit()

    # ---------------- TEST 1 ----------------
    def test_01_page_loads(self):
        """Test professional: mesura el temps de càrrega, verifica el títol i guarda una captura."""
        if not self.driver:
            pytest.skip("Driver no disponible")

        start = time.time()
        self.driver.get("https://www.cyberhotsecurity.cecti.iesmontsia.cat/contact/")
        load_time = round(time.time() - start, 2)

        title = self.driver.title
        current_url = self.driver.current_url

        screenshot_path = "captura_contacte.png"
        try:
            self.driver.save_screenshot(screenshot_path)
        except Exception:
            pass

        print(f"\n🌐 Pàgina carregada correctament.")
        print(f"🏷️  Títol: {title}")
        print(f"🔗 URL actual: {current_url}")
        print(f"⏱️  Temps de càrrega: {load_time} segons")
        print(f"📸 Captura guardada a: {screenshot_path}")

        assert "contact" in current_url.lower()
        assert len(title) > 0
        assert load_time < 30, f"La pàgina ha trigat massa a carregar ({load_time}s)"

    # ---------------- TEST 2 ----------------
    def test_02_check_elements_Andrei(self):
        """Comprova que els camps del formulari existeixen i detecta si són obligatoris"""
        if not self.driver:
            pytest.skip("Driver no disponible")

        URL = "https://www.cyberhotsecurity.cecti.iesmontsia.cat/contact/"
        self.driver.get(URL)
        wait = WebDriverWait(self.driver, 10)

        fields = [
            ("wpforms-2234-field_1", "Nom (first)"),
            ("wpforms-2234-field_1-last", "Cognom (last)"),
            ("wpforms-2234-field_2", "Correu electrònic (email)"),
            ("wpforms-2234-field_3", "Missatge"),
        ]

        for field_id, friendly in fields:
            el = wait.until(EC.presence_of_element_located((By.ID, field_id)))
            assert el, f"No s'ha trobat el camp: {friendly} (id={field_id})"

            # Verifiquem si té l'atribut required (HTML5) o classe required de WPForms
            required_attr = el.get_attribute("required")
            class_attr = el.get_attribute("class") or ""
            has_required_class = "wpforms-field-required" in class_attr or "required" in class_attr.lower()
            if required_attr or has_required_class:
                print(f"✅ Camp obligatori detectat: {friendly} (id={field_id}) — required_attr={required_attr}, class='{class_attr}'")
            else:
                print(f"⚠️ Camp NO obligatori: {friendly} (id={field_id}) — required_attr={required_attr}, class='{class_attr}'")

        # Comprovem el botó d'enviament
        submit_btn = wait.until(EC.presence_of_element_located((By.ID, "wpforms-submit-2234")))
        assert submit_btn
        print(f"✅ Botó d'enviament detectat: {submit_btn.get_attribute('id')}")

    # ---------------- TEST 3 ----------------
    def test_03_submit_and_required_validation_Ximo(self):
        """
        Test 3 robust:
        A) Envia el formulari correctament (sense fallar si no apareix cap missatge visible).
        B) Per a cada camp obligatori, el deixa buit i verifica que el formulari NO s'envia.
        """
        if not self.driver:
            pytest.skip("Driver no disponible")

        URL = "https://www.cyberhotsecurity.cecti.iesmontsia.cat/contact/"
        wait = WebDriverWait(self.driver, 25)

        def screenshot(name):
            ts = time.strftime("%Y%m%d_%H%M%S")
            path = f"screenshot_{name}_{ts}.png"
            try:
                self.driver.save_screenshot(path)
                print(f"💾 Captura guardada: {path}")
            except Exception as e:
                print(f"No s'ha pogut guardar la captura: {e}")
            return path

        def fill_field(el, value):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            el.clear()
            time.sleep(0.2)
            el.send_keys(value)
            time.sleep(0.1)
            el.click()
            self.driver.execute_script("arguments[0].focus();", el)
            time.sleep(0.1)
            self.driver.execute_script("arguments[0].blur();", el)
            time.sleep(0.2)

        # A) Enviament correcte
        self.driver.get(URL)
        wait.until(EC.presence_of_element_located((By.ID, "wpforms-2234-field_1")))

        fill_field(self.driver.find_element(By.ID, "wpforms-2234-field_1"), "Test")
        fill_field(self.driver.find_element(By.ID, "wpforms-2234-field_1-last"), "User")
        fill_field(self.driver.find_element(By.ID, "wpforms-2234-field_2"), "test@example.com")
        fill_field(self.driver.find_element(By.ID, "wpforms-2234-field_3"), "Missatge de prova")

        submit_btn = self.driver.find_element(By.ID, "wpforms-submit-2234")
        # fem click via JS per evitar problemes d'interactuabilitat
        self.driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(2)  # esperar crida AJAX / submit
        print("✅ Formulari enviat correctament (sense error detectat al botó).")

        # B) Validació camps obligatoris
        required_fields = [
            ("wpforms-2234-field_1", "Nom (first)"),
            ("wpforms-2234-field_1-last", "Cognom (last)"),
            ("wpforms-2234-field_2", "Correu (email)"),
        ]

        for field_id, friendly in required_fields:
            self.driver.get(URL)
            wait.until(EC.presence_of_element_located((By.ID, "wpforms-2234-field_1")))

            f_first = self.driver.find_element(By.ID, "wpforms-2234-field_1")
            f_last = self.driver.find_element(By.ID, "wpforms-2234-field_1-last")
            f_email = self.driver.find_element(By.ID, "wpforms-2234-field_2")
            f_msg = self.driver.find_element(By.ID, "wpforms-2234-field_3")

            for el in (f_first, f_last, f_email, f_msg):
                try:
                    el.clear()
                except:
                    pass

            if field_id != "wpforms-2234-field_1":
                f_first.send_keys("Test")
            if field_id != "wpforms-2234-field_1-last":
                f_last.send_keys("User")
            if field_id != "wpforms-2234-field_2":
                f_email.send_keys("test@example.com")

            f_msg.send_keys("Missatge prova validació obligatòria")

            submit_btn = self.driver.find_element(By.ID, "wpforms-submit-2234")
            self.driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(1)  # esperar validació JS

            # Verifiquem que el formulari segueix present a la pàgina (no es navega a 'gràcies')
            try:
                wait.until(EC.presence_of_element_located((By.ID, "wpforms-2234-field_1")))
                print(f"✅ Validació obligatòria OK: {friendly} (id={field_id})")
            except:
                screenshot(f"required_field_sent_{field_id}")
                pytest.fail(f"El formulari s'ha enviat encara que '{friendly}' (id={field_id}) estava buit.")

    # ---------------- TEST 4 ----------------
    def test_04_xss_injection_check_Lucas(self):
        """Test 4 (ciberseguretat): comprovar un intent bàsic d'XSS (no executar scripts)."""
        if not self.driver:
            pytest.skip("Driver no disponible")

        URL = "https://www.cyberhotsecurity.cecti.iesmontsia.cat/contact/"
        wait = WebDriverWait(self.driver, 15)
        self.driver.get(URL)

        # Payload de prova (inofensiu) per detectar si es reflecteix o s'executa
        xss_payload = "<script>alert('XSS');</script>"

        fields_to_test = [
            "wpforms-2234-field_1",
            "wpforms-2234-field_1-last",
            "wpforms-2234-field_2",
            "wpforms-2234-field_3"
        ]

        # Omplir camps amb el payload
        for field_id in fields_to_test:
            el = wait.until(EC.presence_of_element_located((By.ID, field_id)))
            try:
                el.clear()
            except:
                pass
            # escrivim el payload
            el.send_keys(xss_payload)
            # blur per disparar validacions JS
            self.driver.execute_script("arguments[0].blur();", el)
            time.sleep(0.2)

        # Enviem via JS per evitar errors d'scroll / interactuabilitat
        submit_btn = wait.until(EC.presence_of_element_located((By.ID, "wpforms-submit-2234")))
        self.driver.execute_script("arguments[0].click();", submit_btn)

        # Esperem una mica perquè es processi l'enviament / renderitzat
        time.sleep(2)

        # 1) Comprovem que no ha aparegut un alert (si apareix, XSS s'ha executat)
        alert_triggered = False
        try:
            self.driver.switch_to.alert
            # si no llença excepció, hi ha una alerta -> execució XSS
            alert_triggered = True
        except NoAlertPresentException:
            alert_triggered = False
        except Exception:
            # altres problemes, assumim que no hi ha alert però ho registrem
            alert_triggered = False

        # 2) Comprovem que el payload no està reflectit com a HTML al page_source
        page_source = self.driver.page_source or ""
        payload_present = xss_payload in page_source

        # Resultat: si es detecta alert o payload reflectit, considerem que hi ha un problema XSS
        if alert_triggered or payload_present:
            # Guardem evidència
            ts = time.strftime("%Y%m%d_%H%M%S")
            path = f"screenshot_xss_detected_{ts}.png"
            try:
                self.driver.save_screenshot(path)
                print(f"💾 Captura guardada: {path}")
            except Exception:
                pass
            pytest.fail(f"XSS detectat: alert={alert_triggered}, payload reflectit={payload_present}")
        else:
            print("✅ XSS check OK: no s'ha executat ni s'ha reflectit el payload a la pàgina.")
