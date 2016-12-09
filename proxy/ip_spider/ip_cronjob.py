from crontab import CronTab
import os


cron = CronTab()

IP_CRAWL_HOME = os.getcwd()
CMD = 'cd ' + IP_CRAWL_HOME + ' && scrapy crawl xici'
print (CMD)

ip_job = cron.new(command=CMD)
ip_job.hour.every(4)
ip_job.run()
