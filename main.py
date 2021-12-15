import traceback
from bs4 import BeautifulSoup
import requests
import os
import re
from tkinter import filedialog,Tk
import random

doi_regex = re.compile(r'10.\d{4,9}/[-._;()/:a-z0-9A-Z]+')    # Regex for parsing DOI Number
pdfurl_regex = re.compile("^(https?://)?www.([\\da-z.-]+).([a-z.]{2,6})/[\\wz.-]+?.pdf$")   # Regex for a PDF URL
proxies = {
    'http': os.getenv('HTTP_PROXY')
}
sess = requests.Session()
headers = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
adapter = requests.adapters.HTTPAdapter(max_retries = 2)
adapter.max_retries.respect_retry_after_header = False
sess.mount('https://', adapter)


# Generate random int for file name if none can be found
def randint(min=10000,max=99999):
    a = random.randint(min,max)
    return a


# Remove invalid characters from file name
def fix_string(string):
    special_char = re.compile(r'[~#%&*{}\\:<>?/+=|]')
    return re.sub(special_char, "_", string)


def search_scholars(query):
    params = {
        "as_vis": "1",
        "q": query,
        "hl": "en",
    }
    html = requests.get('https://scholar.google.com/scholar', headers = headers, params = params,
                        proxies = proxies).text     # Search Google Scholars for links matching the query
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    i = 1
    print("Select one of the following to download:\n")
    for result in soup.select('.gs_ri'):    # Display all the results from Scholar Search
        title = result.select_one('.gs_rt').text
        title_link = result.select_one('.gs_rt a')['href']
        data[i] = [title_link, title]
        print(str(i) + ". " + title + ": " + title_link)
        i += 1
    option = int(input("\nYour Option (Enter 0 to exit): "))
    try:
        if (option == 0):
            return
        link = data[option][0]
        return link     # Return link of selected option
    except KeyError:
        print("Invalid option!")
        return


# Parse DOI Number from Publisher website
def search_doi(link):
    try:
        html = requests.get(link, headers = headers, proxies = proxies)
        doi = doi_regex.search(html.text).group(0)
        return doi
    except AttributeError as e:     # Website has WAF Protection
        if (html.status_code != 200):
            print("Website access denied. Please enter the DOI number manually.")
        else:
            with open("error.txt", 'a') as f:
                f.write(str(e))
                f.write(traceback.format_exc())


def search_sci_hub(doi):
    try:
        sci_hub = "https://sci-hubtw.hkvisa.net/" + doi
        html = sess.get(sci_hub, headers = headers).text
        soup = BeautifulSoup(html, 'lxml')
        link = soup.find_all('iframe')[0]['src']
        unparsed_title = soup.find("div", id = "citation", onclick = "clip(this)")      # Get title of Journal
        title_pattern = re.compile(r'(<i>)([a-zA-Z0-9\s.-:]+)([.])')
        fname = fix_string(title_pattern.search(str(unparsed_title)).group(2)) + ".pdf"
        pdf = sess.get(link, headers = headers)     # Get PDF content in bytes
        return pdf, fname
    except IndexError as e:     # Journal article not available in Sci Hub database
        print("Link not found!")
        with open("error.txt", 'a') as f:
            f.write(str(e))
            f.write(traceback.format_exc())


def download_pdf(pdf_content, fname):
    with open(fname, 'wb') as f:
        f.write(pdf_content.content)        # Write PDF contents to file
    print("Downloaded " + fname)
    return True


def ask_directory():
    dir_option = int(input("Enter 1 to select file directory to download to, leave empty for current directory: ") or 0)
    if (dir_option == 1):
        Tk().withdraw()
        dirname = filedialog.askdirectory(initialdir = "/", title = 'Please select a directory')
        return dirname
    elif (dir_option == 0):
        return os.path.dirname(os.path.realpath(__file__))      # Return the current directory
    else:
        print("Invalid option.")
        return


def main():
    query = input("Enter the article title or DOI number: ")
    if (doi_regex.search(query) is not None):   # If the provided query is already a DOI Number
        pdf_content, fname = search_sci_hub(doi_regex.search(query).group(0))
        fname = ask_directory() + "\\" + fname
        if download_pdf(pdf_content, fname):
            input()
        else:
            print("File cannot be downloaded!")
    else:
        link = search_scholars(query)
        if link:
            if (pdfurl_regex.search(link) is not None):     # If the URL returned is not a PDF URL
                if (doi_regex.search(link)):
                    doi = doi_regex.search(link).group(0)
                else:
                    doi = search_doi(link)
                if (doi is not None):
                    pdf_content, fname = search_sci_hub(doi)
                    fname = ask_directory() + "\\" + fname
                    if download_pdf(pdf_content, fname):
                        input()
                    else:
                        print("File cannot be downloaded!")
            else:   # If the URL returned is already a PDF URL, there's no need to get the DOI Number
                pdf_response = sess.get(link, headers = headers)    # Get PDF content in bytes
                try:
                    pdf_headers = pdf_response.headers['Content-Disposition']   # Get PDF file name from headers
                    fname = re.findall("filename=\"(.+)\"", pdf_headers)[0]
                except KeyError:
                    fname = str(randint()) + ".pdf"     # If headers is not available, generate a random integer
                finally:
                    fname = ask_directory() + "\\" + fname
                    download_pdf(pdf_response, fname)
        else:
            return


if __name__ == "__main__":
    main()

