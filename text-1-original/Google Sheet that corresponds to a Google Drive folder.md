1. Create new Sheet
2. From the menu at the top, select `Extensions > App script`
3. Paste the below code (`https://drive.google.com/drive/folders/<folder ID>`)
```js
function myFunction() {
	updateSheetsWithSpecificFolders_mod([
			// Replace these with your folder IDs
			'<folder ID>',
			'<another folder ID>',
		]);
}

// Author: Bing Copilot; modified by writer
function updateSheetsWithSpecificFolders_mod(folderIds) {
	var ss = SpreadsheetApp.getActiveSpreadsheet();

	for (var i = 0; i < folderIds.length; i++) {
		var folder = DriveApp.getFolderById(folderIds[i]);
		var sheet = ss.getSheetByName(folder.getName()) || ss.insertSheet(folder.getName());

		// Initialize headers
		var headers = ['File Name', 'URL'];
		sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

		// Freeze the header row
		sheet.setFrozenRows(1);

		var files = folder.getFiles();
		var fileCount = 0;

		while (files.hasNext()) {
			var file = files.next();
			sheet.appendRow([file.getName(), file.getUrl()]);
			fileCount++;
		}
	}
}
```
4. Click `Run` on the Apps Script page to run the script on the Sheet

----

(Original Bing Copilot code:)
```js
// Author: Bing Copilot
function updateSheetsWithSpecificFolders() {
	var ss = SpreadsheetApp.getActiveSpreadsheet();

	// Replace these with your folder IDs
	var folderIds = ['FolderId1', 'FolderId2', 'FolderId3'];

	for (var i = 0; i < folderIds.length; i++) {
		var folder = DriveApp.getFolderById(folderIds[i]);
		var sheet = ss.getSheetByName(folder.getName()) || ss.insertSheet(folder.getName());

		// Initialize headers
		var headers = ['File Name', 'URL'];
		sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

		// Freeze the header row
		sheet.setFrozenRows(1);

		var files = folder.getFiles();
		var fileCount = 0;

		while (files.hasNext()) {
			var file = files.next();
			sheet.appendRow([file.getName(), file.getUrl()]);
			fileCount++;
		}
	}
}
```