# LYD.IA

Basic chatbot written in Python which purpose a flight after taking in account conversation-based details about user's speech. The conversation is in french only.
Please note that the Chatbot is still in developpement, thus resulting in some incomplete features and word's recognition not being optimal, and some features might be upcoming to complete it.

![image1](https://github.com/thewozn/LYD.IA/blob/master/img/Lydia.PNG)

## Getting Started

Provided in french only. In order to use the chatbot, you have to run the file **main.py** from command line/terminal or from Python console, then chose the display mode which fits you the best. Once started, you  just have to answer naturally to bot's questions printed on the screen. Note that **dates have to be entered in MM/JJ or MM JJ format**.


### Important note

In order to use full features of our chatbot, please verify that your **src/mode_3/GraphicalContent contains 1369 files**. If not, you will not be able to use graphical features. If so, you have to download the archive from https://www.dropbox.com/s/ejns8qhmhybjh42/GraphicalContent.zip?dl=0 and replace GraphicalContent by the GraphicalContent's folder from the downloaded archive.
Provided code is fully commented.


### Prerequisites

* Python 3
* pygame
* standard Python libraries (sqlite3, requests...)

### Files
* **Airports.py** containing all methods relative to database creation. The database created by the script contains a list of airports and informations relative to them, suchas their code and location (city).

* **Graphical_content.py** containing graphic methods and loop for graphic mode. This mode is uncomplete and is just a **demo** for now. This file is the main file of this mode.

* **Interface.py** contains functions relative to response generation in console mode. This file is the main file of this mode.

* **IOpy.py** contains all functions concerning the data loading and writing.

* **lexical_analysis.py** contains all data analysis methods, suchas tokenization and a very basic semantic analysis. Note that some phase-3 (end of algorithm) functions have to be reworked.

* **main.py** which is a simple selector launching either graphic or console mode.

* **scrape.py** contains all functions and class concerning obtention of data from a website. Some parts of this file are based on @AchintyaAshok's work https://github.com/AchintyaAshok/Kayak-Scraper/tree/aef1f8f29f8c586e5ad8f644b2f6490c3d87501c

* **textbox.py** contains a class and its methods regarding the creation of a textbox. This file is written by Mekire and can be found here: https://github.com/Mekire/pygame-textbox

* **utils.py** containing all non purpose-specific methods used in the chatbot.

![image2](https://github.com/thewozn/LYD.IA/blob/master/img/Lydia2.PNG)

## Authors
* **Anthony WOZNICA**
