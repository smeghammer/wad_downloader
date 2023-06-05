''' application view '''

import argparse
from urllib.parse import urlparse
from flask import Flask
from flask import jsonify,request
from flask.templating import render_template
from libs.database import MongoConnection
from libs.sqlite_database import ServerDatabaseActions
app = Flask(__name__)

@app.route('/')
def index():
    ''' HTML default view '''
    print(request.args)
    return render_template('index.html',args = request.args)

# see https://stackoverflow.com/questions/33241050/trailing-slash-triggers-404-in-flask-path-rule
@app.route('/api/')
def api():
    ''' API root '''
    if request.args.get('test'):
        #https://stackabuse.com/get-request-query-parameters-with-flask/
        return(jsonify({'arg': request.args.get('test')}))
    return jsonify({'message':'REST API for Doom WAD downloader'})

@app.route('/api/list_all/')
def list_all():
    ''' return all queued items.
    fucking pymongo 4!!! https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection '''
    # TODO: needs to paginate!
    return jsonify( list(  mongo_wrapper.db['downloads'].find({},{"_id":False})))

@app.route('/api/summary/')
def summary():
    ''' return a quick summary of the queued items '''
    # dbServer = args.dbserver
    _out = {'summary':{
            'db_address':args.dbserver,
            'total':mongo_wrapper.db['downloads'].count_documents({}),
            'downloaded':mongo_wrapper.db['downloads'].count_documents({'state':'FETCHED'}),
            'queued':mongo_wrapper.db['downloads'].count_documents({'state':'NOTFETCHED'}),
            'in_progress':mongo_wrapper.db['downloads'].count_documents({'state':'LOCKED'})
            }}
    return jsonify(_out)

@app.route('/api/exists/')
def exists():
    ''' check whether a URL exists in the database. optionally(?) filter by source '''
    _out = {'status':'ok','exists':False}
    if request.args.get('url',False):
        query = {'url' : request.args.get('url')}
        if request.args.get('source',False):
            query['source'] = request.args.get('source')
        _out = {'status':'ok','exists':True,'data': list(mongo_wrapper.db['downloads'].find(query,{'_id':False}))}
    return jsonify(_out)

@app.route('/api/store/')
def store():
    ''' store contents of requested URL '''
    _out = {'status':'warning','inserted':False}
    _url =  request.args.get('url')
    if _url:
        url_parsed = urlparse(_url)
        print(url_parsed)
        filename = None
        # The URL may be a direct link or may be parameterised. Therefore, we cannot rely on urlparse to reliably obtain the filename.
        if not url_parsed.query:
            # test direct URL
            filename = url_parsed.path.split('/')[len( url_parsed.path.split('/'))-1]
            # or test for paramerised filename
        else:
            # we cannot know in advance what the parameter is, so test for '.' and work form that. There may be exceptions...
            _params = url_parsed.query.split('&')
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
        _result = mongo_wrapper.db['downloads'].insert_one(_in)

        if _result.acknowledged:
            _out = {'status':'ok','inserted':True,'data': {'url': _url}}
        print(_out)
    return jsonify(_out)

# routes specific to certain crawlers:

#
# Doomworld By Author
#
@app.route('/api/idgames/mapcount_by_author/')
def get_dw_counts_by_author():
    ''' retrieve mapcount for a given author, ignoring case '''
    author =  request.args.get('author',False)
    return sqlite_wrapper.get_dw_counts_by_author(author)

@app.route('/api/idgames/maps_by_author/')
def get_dw_maps_by_author():
    ''' retrieve map details for a given author, ignoring case '''
    author =  request.args.get('author',False)
    return sqlite_wrapper.get_dw_maps_by_author(author)

if __name__ == '__main__':
    # capture CLI args:
    parser = argparse.ArgumentParser(description='Start metadata collection with startnode, db server, db port and DB name')
    parser.add_argument( '-d', '--dbserver', help='Mongo DB server IP [string]', type=str, required=True)
    parser.add_argument( '-p', '--dbport', help='Mongo DB port [int]', required=False, type=int, default=27017)
    parser.add_argument( '-n', '--database', help='Mongo database name [string]', type=str, required=False,default='DoomWadDownloader')
    parser.add_argument( '-m', '--metadatadb', help='Metadata database name [string]', type=str, required=False,default='metadata.db')
    args = parser.parse_args()
    mongo_wrapper = MongoConnection(args.dbserver,args.dbport,args.database)
    sqlite_wrapper = ServerDatabaseActions(args.metadatadb)
    #see https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network
    app.run(host="0.0.0.0")
