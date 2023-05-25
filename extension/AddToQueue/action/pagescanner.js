/**
A service worker is the new version of background pages:
https://developer.chrome.com/docs/extensions/mv3/migrating_to_service_workers/
*/

/** register listeners on load */
chrome.runtime.onInstalled.addListener(() => {
  console.log('background script onload');
  /* see https://stackoverflow.com/questions/32718645/google-chrome-extension-add-the-tab-to-context-menu/32719354#32719354 */
	

	/* TODO: setup config with test for DB availability (copy grey google) 
	https://developer.chrome.com/docs/extensions/mv3/content_scripts/
	*/
	chrome.contextMenus.create({
		id:"add-wad",
		title: 'Add to download queue',
		contexts: ['link']
	});
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
	console.log('Adding listener for link right click:',info,tab);
    if (info.menuItemId == "add-wad") {
		
		/*
		so here, I want to see whether the link is valid as a download link - probably blunt checking for extension?
		And then I need to do some checks against the database (to be configured with popup script and local storage)
		 - is teh database connection configured? (perhaps only show the right-click option if it is?)
		 - Are we connected to the database?
		 - Is the current URL present in the database? 
		 - what is its status? */
		var _root = "http://127.0.0.1:5000";
		let _summary = _root + "/api/summary";
		let _check = _root + "/api/exists?url=" + info.linkUrl;
		let _store = _root + "/api/store?url=";
		
		
		//TODO - need to reset the above to include the modified _root as per the 'var _root' above
		//get all keys at once:
		//https://stackoverflow.com/questions/18150774/get-all-keys-from-chrome-storage
//		chrome.storage.sync.get(null,function(result){
//			_root=result['ip_address'] + ":" + result['port']
		
			//see https://stackoverflow.com/questions/53405535/how-to-enable-fetch-post-in-chrome-extension-contentscript
			/* let's use ES6
			https://stackoverflow.com/questions/25107774/how-do-i-send-an-http-get-request-from-a-chrome-extension*/
		test = 	fetch(_check)
		console.log(test);
		fetch(_check)
				.then(r => r.json())
				.then(result => {
					console.log(result);
					if(result && result['status'] && result['status'] === 'ok'){
						if(result['exists'] === false){
							console.log('URL ' + info.linkUrl + ' is not stored');
							/** store it */	
							fetch(_store + info.linkUrl)
								.then(r => r.json())
								.then(result => {
									console.log(result);
								});
						}
						else{
							if(result['data']['fetched'] === 'NOTFETCHED'){
								/** don't 'store it */
								console.log('URL ' + info.linkUrl + ' is stored but not fetched');
							}
							if(result['data']['fetched'] === 'FETCHED'){
								/** don't 'store it */	
								console.log('URL ' + info.linkUrl + ' is already fetched');
							}
						}
					}
			})
			.catch((error)=>{
				console.log(error);
				
			});	
//		})
    }
});