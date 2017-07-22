import pymysql


class DB(object):
    def insDATA(self,service_name, service_ip, cpu_rate, memory_rate, cpu_num, memory_num,datetime):
            self.service_name = service_name
            self.service_ip = service_ip
            self.cpu_rate = cpu_rate
            self.memory_rate = memory_rate
            self.cpu_num = cpu_num
            self.memory_num = memory_num
            self.datetime = datetime

            db = pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           db='serviceDB',
                           port=33066,
                           charset='utf8')
            try:
                with db.cursor() as cur:
                    print(u'数据库已连接完毕。。。')
                    # 执行sql语句
                    sql = 'INSERT INTO serviceinfo (service_name, service_ip, cpu_rate, memory_rate,cpu_num,memory_num,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                    cur.execute(sql,(self.service_name, self.service_ip, self.cpu_rate, self.memory_rate, self.cpu_num,self.memory_num,self.datetime))
                    # 提交到数据库执行
                    db.commit()
                    print (u'监控数据写入完毕\n')
            except Exception as e:
                print(e)
                db.rollback()
                print (u'监控数据写入失败')
            # 关闭数据库连接
            finally:
                db.close()
                print(u'数据库连接已经关闭。。。')