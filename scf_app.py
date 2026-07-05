# 腾讯云SCF部署配置
# Web函数监听端口必须为9000

import os
os.environ['PORT'] = '9000'

from app import app

# SCF入口
handler = app
