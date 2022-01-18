/** 
Smeghammer 2022
Controller code for settings popup
 */

let settings = {
	_testBtn : null,
	init : function(){
		
//		/** set fields to current values */
//		chrome.storage.sync.get(['ip_address'],function(result){
//			document.getElementById('ip_address').value = result['ip_address'];
//		});
//		chrome.storage.sync.get(['port'],function(result){
//			document.getElementById('port').value = result['port'];
//		});
		
		var _root = "http://127.0.0.1:5000/";
		let _summary = _root + "/api/summary";
		document.getElementById("is_connected").style.display="inline-block"
		try{
			
			fetch(_summary)
				.then(r => r.json())
				.then(result => {
					for(thing in result['summary']){
						document.getElementById(thing).innerHTML = result['summary'][thing];
					}
					document.getElementById("is_connected").style.display="none";
				})
				
			}
			catch(e){
				//document.getElementById("is_connected").style="display:inline-block;"
			}
		

		
		/** add event listeners */
//		this._testBtn = document.getElementById('test_connection');
//		this._testBtn.addEventListener("click",this.testHandler,false);
//		
//		this._saveBtn = document.getElementById('save_connection');
//		this._saveBtn.addEventListener("click",this.saveHandler,false);
		
	},
	
//	testHandler : function(){
//		document.getElementById('message').innerHTML = 'testing connection<br />';
////		chrome.storage.sync.get(['ip_address'],function(result){
//		chrome.storage.sync.get(null,function(result){
//			document.getElementById('message').innerHTML += 'IP: '+result['ip_address'] +'<br />';
//			document.getElementById('message').innerHTML += 'IP: '+result['port'] +'<br />';
//			let _root=result['port'] + ":" + result['port']
//			console.log("_root: "+ _root);
//			let _out = "";
//			/*for(thing in result){
//				_out += thing + " = " + result[thing]+"\n";
//			}*/
//			document.getElementById('message').innerHTML += "Testing...<br />";
//			document.getElementById('message').innerHTML += _root + "<br />";
////			fetch(_store + info.linkUrl)
//			fetch(_root)
//							.then(r => r.json())
//							.then(result => {
//								document.getElementById('message').innerHTML += r;
//							}); 
//		});
//	},
	
//	saveHandler : function(){
//		chrome.storage.sync.set({'ip_address':document.getElementById('ip_address').value},function(){
//			document.getElementById('message').value = "Settings updated";
//		});
//		chrome.storage.sync.set({'port':document.getElementById('port').value},function(){
//			document.getElementById('message').innerHTML = "Settings updated";
//		});
//	}
	
};
settings.init();
//THIS WORKS!!
//	setInterval(
//settings.init	,2000);