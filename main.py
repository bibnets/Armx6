#!/usr/bin/python

import smtplib
import string
import subprocess as sub
import time
from collections import Counter

def notice_mail(m_text):
	HOST = 'mail.ABC.com'
	SUBJECT = "This is From 10.10.1.1 OB_2 ARM_Core Notice"
	TO = "bibnets@abc.com"
	FROM = "bibnets@abc.com"
	text = m_text
	BODY = string.join((
		"From:  %s" % FROM,
		"To:	%s"	% TO,
		"Subject: %s" % SUBJECT,
		"",
		text
	), "\r\n")
	server = smtplib.SMTP()
	server.connect(HOST,"25")
	server.login("bibnets@abc.com","abc")
	server.sendmail(FROM, [TO], BODY)
	server.quit()
	
def get_yellowcard_list(baseline):
	list_tcpdump_set = []
	list_machine_set = []
	dict_tcpdump_statistics = {}

	p = sub.Popen(('tcpdump','-i','eth1','ip','-c','1000','-nNtqfnn'), stdout=sub.PIPE)

	for row in iter(p.stdout.readline, b''):
		tcpdump = row.rstrip().split()[3].split('.')
		if len(tcpdump) == 4:
			tcpdump[3] = tcpdump[3].strip(':')
			tcpdump_format = '.'.join(tcpdump)
			list_tcpdump_set.append(tcpdump_format)
		else:
			del tcpdump[4]
			tcpdump_format = '.'.join(tcpdump)
			list_tcpdump_set.append(tcpdump_format)

	dict_tcpdump_statistics = Counter(list_tcpdump_set)

	for machine in dict_tcpdump_statistics.keys():
		if dict_tcpdump_statistics.get(machine) > baseline:
			list_machine_set.append(machine)
	return list_machine_set

def main():
	baseline = 400
	b = []
	dict_yellowcard_statistics = {}
	i = 1
	while i <= 6:
		a = get_yellowcard_list(baseline)
		b.extend(a)
		i += 1
		time.sleep(9)
	dict_yellowcard_statistics = Counter(b)
		
	for yellowcard_machine in dict_yellowcard_statistics.keys():
		if dict_yellowcard_statistics.get(yellowcard_machine) > 4 :
			m_ip = yellowcard_machine
			m_account = dict_yellowcard_statistics.get(yellowcard_machine)
			m_text = "Warning, {top_ip} > {top_baseline}/1000 packets in 10s: {top_account} times per minute."
			notice_mail(m_text.format(top_baseline=baseline,top_ip=m_ip,top_account=m_account))
			
		elif dict_yellowcard_statistics.get(yellowcard_machine) > 1 :
			m_ip = yellowcard_machine
			m_account = dict_yellowcard_statistics.get(yellowcard_machine)
			m_text = "Warning, {top_ip} > {top_baseline}/1000 packets in 10s: {top_account} times per minute."
			#notice_mail(m_text.format(top_baseline=baseline,top_ip=m_ip,top_account=m_account))
				
		else:
			m_ip = yellowcard_machine
			m_account = dict_yellowcard_statistics.get(yellowcard_machine)
			m_text = "Warning, {top_ip} > {top_baseline}/1000 packets in 10s: {top_account} times per minute."
			#notice_mail(m_text.format(top_baseline=baseline,top_ip=m_ip,top_account=m_account))

if __name__ == "__main__":
	main()

