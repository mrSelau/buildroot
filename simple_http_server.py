import time
import BaseHTTPServer
import os
import platform, re, subprocess
import time
import psutil

HOST_NAME = '192.168.1.10' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
    	processos = get_running_process()
    	lista_processo = processos.split("+")
    	datahora = os.popen('date').read()
    	my_sys = platform.platform()
    	versao = platform.release()
    	modelo_processador = platform.machine()
    	velocidade = get_processor_speed()
    	up = uptime()
    	memory = psutil.virtual_memory()
    	memory_total = memory.total
    	memory_used = memory_total - memory.available
    	capProcessador = psutil.cpu_percent()
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>Lab SISOP       Grupo: Bruno Selau e Luiz Mosmann.</p>")
        s.wfile.write("<p>Data e Hora: %s</p>" % datahora)
        s.wfile.write("<p>--------------------------------</p>")
        s.wfile.write("<p> Uptime: %s segundos.</p>" % up)
        s.wfile.write("<p>--------------------------------</p>")
        s.wfile.write("<p>Modelo Processador: %s</p>" % modelo_processador)
        s.wfile.write("<p>Velocidade do processador: %s .</p>" % velocidade)# falta
        s.wfile.write("<p>--------------------------------</p>")
	s.wfile.write("<p>Capacidade ocupada do processador: %s percent.</p>" % capProcessador)# falta
        s.wfile.write("<p>--------------------------------</p>")
        s.wfile.write("<p>Quantidade memoria ram usada: %s mb</p>" %memory_used)# falta
        s.wfile.write("<p>Quantidade memoria ram total: %s mb</p>" %memory_total)# falta
        s.wfile.write("<p>--------------------------------</p>")
        s.wfile.write("<p>Sistema: %s</p>" % my_sys)
        s.wfile.write("<p>Versao do sistema: %s</p>" % versao)
        s.wfile.write("<p>--------------------------------</p>") 
        s.wfile.write("<p>processos do sistema: </p>")
        n_processo = 0
        for i in lista_processo:
        	j = str(n_processo) + ": " + i
        	s.wfile.write("<p>%s</p>" % j)
        	n_processo += 1
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")
    
def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
        
def get_processor_speed():
  allInfo = (subprocess.check_output("cat /proc/cpuinfo", shell=True).strip()).decode()
  for line in allInfo.split("\n"):
    if "cpu MHz" in line:
      return re.sub( ".cpu MHz.:", "", line,1)
      return ""

def get_running_process():
  temp = "\n"
  for proc in psutil.process_iter():
    processName = proc.name()
    processID = proc.pid
    temp += "( " + processName + " ::: " + str(processID) + " )+"
  return temp

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

