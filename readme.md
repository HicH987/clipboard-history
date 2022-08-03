# Clipboard History

## Description
This project is clone of the standard windows clipboard. It saves each item placed on the clipboard allowing access to any of those items at a later time.

<p align="center">
  <img src="./assets/images/image1.png "/>
</p>

## Installation

Run command line below to install all requirements
```console
pip install -r requirements.txt
```  

## Usage

Run command line below to start the programme
```console
python main.py
```

### Main window

- The keyboard shortcut to show main windows is by default &nbsp; **`alt + <`**

- To copy any text from the clipboard history list just click on one of the available text, it will be added to the current clipboard.

- Any copied text is automatically added to the clipboard history list.

- The main window hides automatically when it's out of focus.

### Search bar 

- To search for any specific text use **searchbar**, just add text or a portion of it in text entry and start searching with `Search` button

- After search to return to the full list uses the `Reset` button

### Menu bar
- To clean all clipboard database uses **menubar** option **`Edit\Clear DB`**

- To change show window shortkey uses **menubar** option **`Edit\Keyboard Shortcut`**
  
- To show database file in windows explorer uses **menubar** option **`Edit\Show Db File`**
  
- To exit the programme uses **menubar** option **`Edit\Exit`**

### Keyboard Shortcut

<p align="center">
  <img src="./assets/images/image2.png "/>
</p>

- The current pressed key will be shown next to label **Current key**

- To confirm the pressed key clicks on **`confirm key`** button
  
- The confirmed keys will be shown below **Shorcut** label

- To save the shortcut clicks on **`Save`** button
  
## License

Distributed under the MIT License. See `license.md` for more information.