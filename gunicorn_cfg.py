# 我就改成gunicorn.py
# 绑定的ip与端口
# bind = "0.0.0.0:8000"
bind="unix:/home/ubuntu/Pi_Media_Server/flaskapp.sock"
# 进程数  
workers = 1
# 指定每个进程开启的线程数
# threads = 2
# 工作模式
worker_class = 'gthread'
# 处理请求的工作线程数，使用指定数量的线程运行每个worker。为正整数，默认为1。
# worker_connections = 2000
# 设置pid文件的文件名，如果不设置将不会创建pid文件
pidfile = './gunicorn.pid'
# 要写入错误日志的文件目录。
errorlog = './log/gunicorn.error.log' 
# 要写入的访问日志目录
accesslog = './log/gunicorn.access.log' 