#!/usr/bin/python3
import logging

adminLog = logging.getLogger('admin_log')
devLog = logging.getLogger('dev_log')


dev_defect = logging.FileHandler('../logs/dev.log')
dev_defect.setLevel(logging.DEBUG)

admin_defect = logging.FileHandler('../logs/admin.log')
admin_defect.setLevel(logging.DEBUG)


dev_defect_format = logging.Formatter('[%(asctime)s] %(levelname)s In %(filename)s on line %(lineno)d - %(message)s',
							datefmt='%d-%b-%y %H:%M:%S')

admin_defect_format = logging.Formatter('[%(asctime)s] %(levelname)s In %(filename)s - %(message)s',
							datefmt='%d-%b-%y %H:%M:%S')

dev_defect.setFormatter(dev_defect_format)
admin_defect.setFormatter(admin_defect_format)

adminLog.addHandler(admin_defect)
devLog.addHandler(dev_defect)