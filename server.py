from http.server import SimpleHTTPRequestHandler, HTTPServer
import subprocess
import os


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/run_script':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(result.stdout.encode())
            except Exception as e:
                self.send_error(500, f"Server Error: {str(e)}")
        else:
            # 其他请求返回静态文件
            super().do_GET()

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)

    print(f"服务器已启动，访问 http://localhost:{port}/index.html")

    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()