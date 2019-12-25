from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings

class FDFSStorage(Storage):
    def __init__(self, client_conf=None, base_url=None):
        if not client_conf:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf
        if not base_url:
            base_url = settings.FDFS_BASE_URL
        self.base_url = base_url
        
    def _open(self, name, mode = 'rb'):
        pass

    def _save(self, name, content):
        #{
        #    'Group name'      : group_name,
        #    'Remote file_id'  : remote_file_id,
        #    'Status'          : 'Upload successed.',
        #    'Local file name' : '',
        #    'Uploaded size'   : upload_size,
        #    'Storage IP'      : storage_ip
        #}
        client = Fdfs_client(self.client_conf)
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise Exception('upload file to fastDFS fail')
        
        filename = res.get('Remote file_id')
        return filename

    def exists(self, name):
        '''判断django服务器，名字是否可用'''
        return False

    def url(self,name):
        return name
        #return self.base_url+name
