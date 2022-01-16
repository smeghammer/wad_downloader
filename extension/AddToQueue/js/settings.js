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
		document.getElementById('message').innerHTML = 'testing connection<br />';
//		chrome.storage.sync.get(['ip_address'],function(result){
		chrome.storage.sync.get(null,function(result){
			document.getElementById('message').innerHTML += 'IP: '+result['ip_address'] +'<br />';
			document.getElementById('message').innerHTML += 'IP: '+result['port'] +'<br />';
			let _root='http://'+result['ip_address'] + ":" + result['port']
			console.log("_root: "+ _root);
			let _out = "";
			/*for(thing in result){
				_out += thing + " = " + result[thing]+"\n";
			}*/
			document.getElementById('message').innerHTML += "Testing...<br />";
			document.getElementById('message').innerHTML += _root + "<br />";
//			fetch(_store + info.linkUrl)
			try{
				fetch(_root).then(r => r.json()).then(result => {
					document.getElementById('message').innerHTML += result;
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