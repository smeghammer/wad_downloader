from libs.database import MongoConnection
from flask import Flask
from flask import jsonify,request
from urllib.parse import urlparse
import requests
import argparse

app = Flask(__name__)

@app.route('/api/')
def root():
    if request.args.get('test'):
        #https://stackabuse.com/get-request-query-parameters-with-flask/
        return(jsonify({'arg': request.args.get('test')}))
    return(jsonify({'message':'REST API for Doom WAD downloader'}))

@app.route('/api/list_all')
def list_all():
    ''' fucking pymongo 4!!! https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection '''
    _result = list(dbWrapper.db['downloads'].find({},{"_id":False}))
    return(jsonify(_result))

@app.route('/api/summary')
def summary():
    return(jsonify({'summary':{
            'total':dbWrapper.db['downloads'].count_documents({}),
            'downloaded':dbWrapper.db['downloads'].count_documents({'state':'FETCHED'}),
            'queued':dbWrapper.db['downloads'].count_documents({'state':'NOTFETCHED'}),
            'in_progress':dbWrapper.db['downloads'].count_documents({'state':'LOCKED'}),
            }
        }))
    
@app.route('/api/exists')
def exists():
    _out = {'status':'ok','exists':False}
    if request.args.get('url') and dbWrapper.db['downloads'].find_one({'url' : request.args.get('url')},{'_id':False}):
        _out = {'status':'ok','exists':True,'data': dbWrapper.db['downloads'].find_one({'url' : request.args.get('url')},{'_id':False})}
    return(jsonify(_out))

@app.route('/api/store')
def store():
    _out = {'status':'warning','inserted':False}
    _url =  request.args.get('url')
    if _url:
        _urlParsed = urlparse(_url) 
        print(_urlParsed)
        filename = None
        ''' The URL may be a direct link or may be parameterised. Therefore, we cannot rely on urlparse to reliably obtain the filename. '''
        if not _urlParsed.query:
            ''' test direct URL '''
            filename = _urlParsed.path.split('/')[len( _urlParsed.path.split('/'))-1]
            ''' or test for paramerised filename '''
        else:
            ''' we cannot know in advance what the parameter is, so test for '.' and work form that. There may be exceptions... '''
            _params = _urlParsed.query.split('&')
            for entry in _params:
                if len(entry.split('=')[1].split('.')) == 2:
                    filename = entry.split('=')[1]
        _in = {
            'url' :_url,
            'state':'NOTFETCHED',
            'source':'api',
            'metadata' :{
                'filename':filename,
                'dir':'api/'
                }
            }
        _result = dbWrapper.db['downloads'].insert_one(_in)

        if _result.acknowledged:
            _out = {'status':'ok','inserted':True,'data': {'url': _url}}
        print(_out)
        
    return(jsonify(_out))

    
if __name__ == '__main__':
    '''
    capture CLI args:
    '''
    parser = argparse.ArgumentParser(description='Start metadata collection with startnode, db server, db port and DB name')
    parser.add_argument( '-d', '--dbserver', help='Mongo DB server IP [string]', type=str, required=True)  
    parser.add_argument( '-p', '--dbport', help='Mongo DB port [int]', required=False, type=int, default=27017)  
    parser.add_argument( '-n', '--database', help='Mongo database name [string]', type=str, required=False,default='DoomWadDownloader')
    args = parser.parse_args()
    dbWrapper = MongoConnection(args.dbserver,args.dbport,args.database)
    #see https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network
    app.run(host="0.0.0.0")
    