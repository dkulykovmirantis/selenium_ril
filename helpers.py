from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from utils import Utils

conf = Utils.get_configuration()


def get_client_driver():
    driver = webdriver.Firefox(
        capabilities={"marionette": False},
        executable_path='/usr/bin/firefox')
    driver.implicitly_wait(conf.get('timeout'))
    if conf.get("minimize_window"):
        driver.set_window_position(2000, 0)
    return driver


def safe_horizon_login(self, user, password):
    try:
        horizon_login(
            self.driver,
            user,
            password)
    except Exception as e:
        self.tearDown()
        raise Exception(e.message)


def horizon_login(driver, user, password):
    driver.get("{}{}".format(conf.get('BASE_URI'), conf.get('login_page')))

    if not driver.find_element_by_id("id_username").is_displayed():
        driver.find_element_by_xpath('//*[@value="credentials"]').click()

    driver.find_element_by_id("id_username").send_keys(user)
    driver.find_element_by_id("id_password").send_keys(password)
    driver.find_element_by_id("loginBtn").submit()

    if conf.get('login_page') in driver.current_url:
        raise Exception("Unauthorized")


def saml_login(driver):
    driver.get("{}{}".format(conf.get('BASE_URI'), conf.get('login_page')))
    driver.find_element_by_xpath('//*[@value="saml2"]').click()

    driver.find_element_by_id("loginBtn").submit()

    driver.find_element_by_name('username').send_keys(conf.get('saml_user'))
    driver.find_element_by_name('password').send_keys(
        conf.get('saml_user_pass'))
    driver.find_element_by_xpath('//*[@value="Login"]').click()

    # ToDo(den) add check for success


def oli_login(driver, ip):
    url = "{}{}".format(conf.get('ilo_url'), ip)
    driver.get(url)

    driver.switch_to.frame(driver.find_element_by_id("modalFrame"))

    driver.find_element_by_id('usernameInput').send_keys(
        conf.get('ilo_user'))
    driver.find_element_by_id('passwordInput').send_keys(
        conf.get('ilo_user_pass'))

    driver.find_element_by_id('ID_LOGON').click()


def ilo_next_page(driver):
    # ActionChains(driver).send_keys(Keys.CONTROL + 't').perform()

    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("appFrame"))
    driver.find_element_by_id('appBody').send_keys(Keys.CONTROL + 't')


def check_element_exists(driver, by, value):
    """We can use Class By or the simple sting

    By.ID = "id"
    By.XPATH = "xpath"
    By.LINK_TEXT = "link text"
    By.PARTIAL_LINK_TEXT = "partial link text"
    By.NAME = "name"
    By.TAG_NAME = "tag name"
    By.CLASS_NAME = "class name"
    By.CSS_SELECTOR = "css selector"
    """
    try:
        driver.implicitly_wait(3)
        driver.find_element(by, value)
    except NoSuchElementException:
        return False
    finally:
        driver.implicitly_wait(conf.get("timeout"))
    return True


def create_screenshot(driver, name_of_test):
    path = conf.get("folder_screenshot")
    if path == '<path of folder for screenshot>':
        path = './'

    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    driver.save_screenshot("{}{}-{}.png".format(
        path, name_of_test, now))
