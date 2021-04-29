from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import datetime
from ConfigParser import SafeConfigParser

''' application modules '''
from database_utils.mongo_utils import mongo_db_util as db

''' email config details '''
parser = SafeConfigParser()
parser.read('email.ini')

me = parser.get('email_congfiguration_details', 'me')
password = parser.get('email_congfiguration_details', 'password')
to = parser.get('email_congfiguration_details', 'to')

''' Basic email template '''
html_string = '''<html><body><div>Hi team </div><div>Please refer below mentioned chat dialogflow history  </div> <br/> {} <br/><div>Thanks & Regards </div><div>AMS chatbot Support </div></body></html>'''


def email_sending(session_id: int, company_id: int, domain_id: int) -> bool:
	try:
        chat_history = (db.get_value_with_session_id(session_id))['chat_flow']
        chat_questions = db.get_question_chat(company_id, domain_id)['questions']

        questions = []
        answers = []

        for value in chat_history:
            question_id = int(value["question_id"])
            answer = value["answer"]
            for chat_question in chat_questions:
                if chat_question["question_id"] == question_id:
                    questions.append(chat_question["question"])
                    answers.append(answer)
                    break

        #html = "<div> Question : {} </div>  <div> Answer : {} </div>"
        final_html = ""
        for index, value in enumerate(questions):
            string = html.format(value.replace("\n", ""), answers[index])
            final_html = final_html + string + "  "
        mail_html_content = html_string.format(final_html)
        msg = MIMEMultipart()
        msg['Subject'], msg['From'], msg['To'] = "REG : Chat dialogflow history...", me, ",".join(to)
        ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)
        text = MIMEText(mail_html_content, 'html')
        msg.attach(text)
        s = smtplib.SMTP('smtp.zoho.com', 587)
        context = ssl.create_default_context()
        s.starttls(context=context)
        s.login(me, password)

        s.sendmail(me, to, msg.as_string())
        s.quit()
        return True
	except Exception as ex:
		logf = open("Email_error.log", "w")
		logf.write("Error == {0} : {1}\n".format(
			now.strftime("%Y-%m-%d %H:%M:%S"), str(ex.strerror)))
		logf.close()
		return False
