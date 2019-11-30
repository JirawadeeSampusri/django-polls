import datetime 
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from polls.models import Question,Choice

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (days < 0 for questions published
    in the past, days > 0 for questions published in the future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question

def create_choice(choice_text, question: Question):
    return Choice.objects.create(choice_text=choice_text,question=question)

class functional_test(LiveServerTestCase):
    username="user"
    password="pass"

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=r"/Users/mac/Desktop/chromedriver")
        super(functional_test,self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(functional_test,self).tearDown()

    def test_currentpoll(self):
        self.browser.get(self.live_server_url + "/polls/")
        head = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(head.text,'Current polls')   

    def test_createpoll_question(self): 
        question = create_question("What is your favorite fruits?", days=-1)
        self.browser.get(self.live_server_url + '/polls/')
        question_element = self.browser.find_element_by_id(f"{question.id}")  
        self.assertEqual(question_element.text,'What is your favorite fruits?')   

    def test_createpoll_question_detail(self):
        question = create_question("What is your favorite fruits?", days=-1)
        self.browser.get(self.live_server_url + '/polls/')
        links = self.browser.find_elements_by_tag_name('a')
        links[0].click()
        self.assertEqual(self.browser.current_url,self.live_server_url + '/polls/' + f"{question.id}/")

    def test_question_result(self):
        question = create_question("What is your favorite fruits?", days=-1)
        choice = create_choice("Mango", question)  
        User.objects.create_user(self.username, password=self.password)
        self.browser.get(self.live_server_url + '/accounts/login')
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)
        self.browser.find_element_by_id("login").click()
        link = self.browser.find_element_by_tag_name('a')
        link.click()
        choice_1 = self.browser.find_element_by_id(f"choice{choice.id}")
        choice_1.click()
        self.browser.find_element_by_id(f"vote").click()
        self.assertEqual(self.browser.current_url,self.live_server_url + '/polls/' + f"{question.id}/results/")     
    
  