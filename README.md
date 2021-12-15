# Sci-Hub_Scraper

Sci-Hub Scaper is a console application to download journal articles PDF from Sci-Hub based on queries made to Google Scholar.
<br/><br/>
## Getting Started

### Installation
1. Locate a green button that says **Clone or Download**, and click on the button.
![alt text](https://imgur.com/8dqFohf.png)

2. Then, in the dropdown, select **Download ZIP**. All of the files will begin downloading to your computer, usually in your Downloads folder.
![alt text](https://i.imgur.com/klBjQjg.png)

Or you can use the package manager [pip](https://pip.pypa.io/en/stable/) to install Sci-Hub_Scraper.

```bash
pip clone https://github.com/m4l0n/Sci-Hub_Scraper.git
```
<br/><br/>
### Prerequisites

Make sure to install the required libraries:

```bash
requests==2.26.0
beautifulsoup4==4.10.0
```

Or you can use the following command:

```bash
pip install -r requirements.txt
```
<br/><br/>

### Usage

After installing Sci-Hub_Scraper, all you need to do is to run the following command: 
```bash
python main.py
```

You will get a prompt where you will need to enter the title or DOI number of the journal article, depending on your preference. 

**Title**: Prompt you to select an option from a list of links that will be displayed. You will then get a prompt to choose the directory to download the file to. Entering 1 will open a file dialog, where you will need to select a directory. Leaving it empty will download the file to the current directory

**DOI**: Get a prompt to choose the directory to download the file to. Entering 1 will open a file dialog, where you will need to select a directory. Leaving it empty will download the file to the current directory.

![alt text](https://imgur.com/5VinN5R.gif)
<br/><br/>
## Contributing
Feel free to contribute by reporting bugs that you may have faced, or propose new features by opening an issue [here](https://github.com/m4l0n/Sci-Hub_Scraper/issues). Any contributions you make will benefit everybody else and are greatly appreciated.
<br/><br/>
## License
This project is licensed under the MIT license. Feel free to edit and distribute this template as you like.
