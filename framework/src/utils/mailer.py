"""
This module provides convenience methods to send mail to recipiants from the framework.

Usage:

>>> from mailer import Mailer
2013-02-20 10:39:56,996 -  WARNING - The log file [log/ionunittest.log] is not created as the directory [log] is not existing!
>>> m = Mailer()
>>> m.addTo('ranjan.muthumalai@lifetech.com')
>>> m.addFrom('ranjan.muthumalai@lifetech.com')
>>> m.addSubject('Anoy Mail')
>>> m.addTextContent("Hi!\\n I am sending this mail to anoy you.\\nThanks,\\nRanjan")
>>> m.sendMail()
"""
import sys, smtplib, traceback

from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from logbase              import LogBase

class Mailer(object):
    """
    This class has methods to add basic information to send mail such as from, to, subject and body of the mail.
    """
    logBase = LogBase('Mailer')
    logBase.createRotatingFileLogger('log/ionunittest.log')
    logger = logBase.logger
    
    def __init__(self):
        self.msg = MIMEMultipart('alternative')

    def addFrom(self, fromAddress):
        """
        This method provides the interface to add a from address.
        @type fromAddress: string
        @param fromAddress: The email address of the email originator. This is the from field of the email.
        @rtype: void
        @return: None.
        """
        self.fromAddress = fromAddress
        self.msg['From'] = fromAddress
        self.logger.debug('From Address: %s'%fromAddress)
        
    def addTo(self, toAddress):
        """
        This method provides the interface to add a to address. 
        @type toAddress: string
        @param toAddress: The email address of the email recipient. This is the to field of the email.
        @rtype: void
        @return: None.
        """
        self.toAddress = toAddress
        self.msg['To'] = toAddress
        self.logger.debug('To Address: %s'%toAddress)
        
    def addSubject(self, subject):
        """
        This method provides the interface to add subject of the email.
        @type subject: string
        @param subject: The suject of the email to be sent.
        @rtype: void
        @return: None.
        """
        self.msg['Subject'] = subject
        self.logger.debug('Subject: %s'%subject)

    def addTextContent(self, textContent):
        """
        This method provides the interface to add text content of the email.
        @type textContent: string
        @param textContent: The body of the email to be sent.
        @rtype: void
        @return: None.
        """
        mimeTextContent = MIMEText(textContent, 'plain')
        self.msg.attach(mimeTextContent)
        self.logger.debug('Plain Text Content: %s'%textContent)
        
    def addHtmlContent(self, htmlContent):
        """
        This method provides the interface to add html content of the email.
        @type htmlContent: string
        @param htmlContent: The body of the email to be sent.
        @rtype: void
        @return: None.
        """
        mimeHtmlContent = MIMEText(htmlContent, 'html')
        self.msg.attach(mimeHtmlContent)
        self.logger.debug('HTML Content: %s'%htmlContent)
        
    def sendMail(self):
        """
        This method sends the content of the email out.
        @raise Exceptions: SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError
        @rtype: void
        @return: None.
        """
        try:
            s = smtplib.SMTP('smtp.itw')
            s.sendmail(self.fromAddress, self.toAddress, self.msg.as_string())
            s.quit()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logger.error('Exception [%s]: %s'%(exc_type.__name__, exc_value))
            self.logger.error('Traceback:')
            for line in traceback.format_tb(exc_traceback):
                self.logger.error(line.strip())
    