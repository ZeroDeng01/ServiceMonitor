from flask import Flask
from flask import request
from db import DB

app = Flask(__name__)



service_name = ''#服务器别称
service_ip = ''#服务器ip
cpu_rate = ''#cpu使用率
memory_rate = ''#内存使用率
cpu_num = ''#cpu使用量
memory_num = ''#内存使用量

datetime = ''#时间

@app.route("/", methods=['POST','GET'])
def getServiceStatus():
    if request.method == 'POST':
        try:
            service_name = request.form['service_name']
            service_ip = request.form['service_ip']
            cpu_rate = request.form['cpu_rate']
            memory_rate = request.form['memory_rate']
            cpu_num = request.form['cpu_num']
            memory_num = request.form['memory_num']

            datetime = request.form['datetime']
            print( u'数据已接收')
            dbobj = DB()
            dbobj.insDATA(service_name, service_ip, cpu_rate, memory_rate,cpu_num,memory_num,datetime)
            return 'ok'
        except Exception as e:
            print(e)
            return 'error'

    else:
        return 'Fuck You！Get is not allowed!'



if __name__ == '__main__':
    app.run()
