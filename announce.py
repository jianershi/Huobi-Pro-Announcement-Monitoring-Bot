# -*- coding: utf-8 -*-
import requests
import time
from credentials import telegram_bot_token
from config import channel_name
# import html2text

#setup
announce_base_url = 'https://www.huobi.com/p/api/contents/pro/list_notice?&limit=10&language=zh-cn'
announcement_content_base_url = 'https://www.huobi.com/p/api/contents/pro/notice/'
webpage_link_base_url = 'https://www.huobi.pro/zh-cn/notice_detail/?id='
announcement_list = []


def pull_announcement():
	try:
		response = requests.get(announce_base_url).json()
		if response['status'] is not 0:
			print "empty response"
			return
		for item in response['data']['items']:
			if item['id'] not in announcement_list:
				try:
					content_response = requests.get(announcement_content_base_url+str(item['id'])).json()
				except:
					print "read content message error"
				if content_response['success'] is not True:
					print "empty response from content"
					return
				announcement_list.append(item['id'])
				send_announcement(item['title'],item['content'],content_response['data']['content'], webpage_link_base_url+str(item['id']))

	except:
		print "respnose error"
		raise

def telegram_send(msg):
	telegram_api_base='https://api.telegram.org/bot'
	telegram_bot_token
	method_name = 'sendMessage'
	chat_id = channel_name
	payload = {'chat_id':chat_id, 'text':msg, 'parse_mode':'Markdown', 'disable_notification':True}
	response = requests.post(telegram_api_base+telegram_bot_token+'/'+method_name, json=payload)
	# print response.text


def send_announcement(title,abstract,msg, link):
	msgbody= '*'+title+'*\n'+\
	'['+link+']'+'('+link+')'+'\n\n'+\
	abstract
		
	telegram_send(msgbody)
	# print '*'+title+'*'+'\n'+msg

def main():
	while(1):
		pull_announcement()
		time.sleep(30)

main()