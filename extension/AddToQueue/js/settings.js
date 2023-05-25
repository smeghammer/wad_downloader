/** 
Smeghammer 2022
Controller code for settings popup
 */

let settings = {
	_testBtn : null,
	init : function(showConnecting){
		var _root = "http://127.0.0.1:5000";
		let _summary = _root + "/api/summary";
		if(showConnecting){
			document.getElementById("is_connected").style.display="inline-block"
		}
		
		try{
			let x = fetch(_summary).then(function(r){
				console.log(r);
			})
			print(x)
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
			console.log(e)
		}
	},
};
settings.init(true);
//THIS WORKS!!
	setInterval(
settings.init	,2000);