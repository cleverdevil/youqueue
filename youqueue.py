import http.server
import queue
import threading
import subprocess
import time


HOST = '0.0.0.0'
PORT = 8781
DOWNLOAD_PATH = '/var/services/homes/admin/Media/Queue'
DOWNLOAD_TMPL = '%(uploader)s - %(title)s.%(ext)s'


class Downloader(threading.Thread):

    def __init__(self):
        self.queue = queue.Queue()
        self.running = True
        super().__init__()
        self.start()

    def push(self, url):
        self.queue.put(url)

    def run(self):
        while self.running:
            try:
                url = self.queue.get_nowait()
            except queue.Empty:
                time.sleep(1)
                continue

            print('Downloading ->', url)
            result = subprocess.run([
                'youtube-dl',
                '-o',
                DOWNLOAD_PATH + '/' + DOWNLOAD_TMPL,
                url
            ], text=True)
            print('Process exited with result ->', result.returncode)


downloader = Downloader()


class YouQueueServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        url = self.path[1:]
        downloader.push(url)
        self.send_response(202, message='Accepted URL for download and processing')
        self.end_headers()


if __name__ == '__main__':
    print('Starting YouQueue server on http://%s:%d' % (HOST, PORT))

    server = http.server.HTTPServer((HOST, PORT), YouQueueServer)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping YouQueue server...')

    downloader.running = False
    server.server_close()
