#!/usr/bin/env python
# coding: utf-8

# # Table of Contents
#  <p><div class="lev1 toc-item"><a href="#Libraries-and-Variables" data-toc-modified-id="Libraries-and-Variables-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Libraries and Variables</a></div><div class="lev1 toc-item"><a href="#Functions" data-toc-modified-id="Functions-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Functions</a></div><div class="lev1 toc-item"><a href="#Test-The-Process" data-toc-modified-id="Test-The-Process-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Test The Process</a></div><div class="lev1 toc-item"><a href="#Results" data-toc-modified-id="Results-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Results</a></div><div class="lev1 toc-item"><a href="#Write-Results-to-File" data-toc-modified-id="Write-Results-to-File-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Write Results to File</a></div>

# # Libraries and Variables

# In[1]:


import os
import re
from spellchecker import SpellChecker
from pprint import pprint
import json

XML_FILE_PAREN = 'C:\\Users\\mehmet.ergun\\Documents\\Temporary\\dc-law-xml\\dc\\council\\code'
FIRST_XML = XML_FILE_PAREN + '\\index.xml'
RESULTS_FILE = 'spellcheck_results.json'


# # Functions

# In[2]:


def list_files(source_dir: str = XML_FILE_PAREN, file_patterns: tuple = ('.xml', )) -> list:
    """
    List files recursively in directory
    """
    file_list = []
    for root, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.endswith(file_patterns):
                file_list.append(os.path.join(root, filename))
    return file_list


assert list_files()[0] == FIRST_XML


# In[3]:


def spellcheck(word_list: tuple = ('something', 'is', 'hapenning', 'here', 'xml')
               , levenshtein_dist = 2
               , acceptables = [
                   'xml', 'utf', 'href', 'dccouncil'
                   , 'xinclude', 'www', 'xmlns', 'subheading', 'http', 'https'
                   , 'subchapter', 'codification', 'codifications', 'subpart', 'subsec'
               ]
              ) -> list:
    """
    Spellcheck words and produce potential corrections as list of (misspelled, correction) tuples
    """
    word_list = [w for w in word_list]
    speller = SpellChecker(distance=levenshtein_dist)
    misspelled = speller.unknown(word_list)
    spellings = []
    for word in misspelled:
        if word not in acceptables:
            if not (re.match(r'^\d+.*', word) or re.match(r'.*\d+$', word)):  # word does not start or end with a digit
                most_likely_correction = speller.correction(word)
                if word != most_likely_correction:
                    print(f'"{word}" => "{most_likely_correction}"')
                    spellings.append((word, most_likely_correction))
    return spellings


assert spellcheck() == [('hapenning', 'happening')]


# In[4]:


def split_text_to_words(text: str = 'hello worlda I exist nows'):
    speller = SpellChecker()
    words = speller.split_words(text)
    return words


assert split_text_to_words() == ['hello', 'worlda', 'i', 'exist', 'nows']


# In[5]:


def read_file(filepath: str = FIRST_XML) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

assert read_file()[0:13] == '<?xml version'


# In[6]:


def batch_spellcheck_files(file_list: list, testme=True):
    cnt = 1
    debug_test = True
    output = []
    for filepath in file_list:
        if testme and cnt > 5:
            break
        if cnt % 50 == 0:
            print(f'******Processing file {cnt} of {len(file_list)}*******')
        print(f'======={filepath}=======')
        spelled = spellcheck(word_list=split_text_to_words(text=read_file(filepath)))
        output.append((filepath, spelled))
        cnt += 1
    return output


# # Test The Process

# In[7]:


file_list=list_files()
spell_results_files_test = batch_spellcheck_files(file_list=file_list, testme=True)
print('===Done===')


# In[8]:


pprint(json.dumps(spell_results_files_test, indent=4))


# In[9]:


# with open(RESULTS_FILE, 'w') as f:
#     json.dump(obj=spell_results_files_test, fp=f, indent=4)


# # Results

# In[10]:


file_list=list_files()
spell_results_files = batch_spellcheck_files(file_list=file_list, testme=False)
print('===Done===')


# # Write Results to File

# In[11]:


with open(RESULTS_FILE, 'w') as f:
    json.dump(obj=spell_results_files, fp=f, indent=4)
print(f'Findings are written to JSON file: {RESULTS_FILE}')

