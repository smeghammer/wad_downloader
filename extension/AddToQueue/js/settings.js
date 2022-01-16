/** 
Smeghammer 2022
Controller code for settings popup
 */

let settings = {
	_testBtn : null,
	init : function(){
		
		/** set fields to current values */
		chrome.storage.sync.get(['ip_address'],function(result){
			document.getElementById('ip_address').value = result['ip_address'];
		});
		chrome.storage.sync.get(['port'],function(result){
			document.getElementById('port').value = result['port'];
		});
		
		
		/** add event listeners */
		this._testBtn = document.getElementById('test_connection');
		this._testBtn.addEventListener("click",this.testHandler,false);
		
		this._saveBtn = document.getElementById('save_connection');
		this._saveBtn.addEventListener("click",this.saveHandler,false);
		
	},
	
	testHandler : function(){
		document.getElementById('message').innerHTML = 'testing connection...<br />';
		chrome.storage.sync.get(null,function(result){
			/** build link to API */
			let APIRoot= 'http://' + result['ip_address'] + ":" + result['port'] + '/api/';

			document.getElementById('message').innerHTML += APIRoot + "<br />";
			//see https://developer.mozilla.org/en-US/docs/Web/API/fetch
			//and https://github.com/mdn/fetch-examples/blob/master/fetch-request/index.html
			try{
				fetch(APIRoot)
					.then(function(response){
						document.getElementById('message').innerHTML += response.status+"<br />";
						return response.json()
						})
					.then(function(data){
						for(a in data){
							document.getElementById('message').innerHTML += a+"="+data[a]+"<br />";
						}
					}
					).catch(function(error){
						document.getElementById('message').innerHTML += error.message;
					}); 
			}
			catch(e){
				document.getElementById('message').innerHTML += e;
			}
		});
	},
	
	saveHandler : function(){
		chrome.storage.sync.set({'ip_address':document.getElementById('ip_address').value},function(){
			document.getElementById('message').value = "Settings updated";
		});
		chrome.storage.sync.set({'port':document.getElementById('port').value},function(){
			document.getElementById('message').innerHTML = "Settings updated";
		});
	}
}

settings.init();