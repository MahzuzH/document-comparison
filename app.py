import streamlit as st
import streamlit.components.v1 as stc
import docx
import pandas as pd
from PyPDF2 import PdfReader
from PyPDF2 import PdfFileReader
import string
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.probability import FreqDist

import math

# def extract_pdf(path):
#     with open(path, 'rb') as f:
#         pdf = PdfFileReader(f)
#         # get the first page
#         page = pdf.getPage(1)
#         print(page)
#         print('Page type: {}'.format(str(type(page))))
#         text = page.extractText()
#         print(text)
   
def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()
    
    return all_page_text

def preprocessing(text):
    #penghilangan white space
    whitespace = text.translate(str.maketrans('','',string.punctuation)).replace("\t", "").replace("\n", "").replace("\r", "").strip()
    #mengubah menjadi lowercase
    lowercase = whitespace.lower()
    #menghapus angka
    removed_angka = re.sub(r"\d+", "", lowercase)
    hasil = removed_angka
    return hasil

def tokenizing(text):
    #melakukan tokenizing, yaitu memisahkan kata perkata
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


# fungsi stopwording/filtering yaitu menghilangkan kata-kata yang tidak penting
def stopwords(text):
    #list stopword bahasa indonesia dari library nltk
    listStopword = nltk.corpus.stopwords.words('indonesian')
    #penambahan kata stopword
    addstop = ['ku', 'pel', 'uru', 'mem', 'astikan', 's', 'iapa', 'koyak']
    listStopword.extend(addstop)
    #proses filtering
    filtering = [words for words in text if not words in listStopword] 
    return filtering
    
def stemming(list):
    # stemming mengubah kata menjadi kata dasarnya
    stemmer = StemmerFactory().create_stemmer()
    sentence_doc = ' '.join(map(str, list))
    stemming_doc = stemmer.stem(sentence_doc)
    result_doc = nltk.tokenize.word_tokenize(stemming_doc)
    return result_doc
 

def main():
    st.title("IR Apps - Mencari data query")
    st.subheader("Kelompok 2")
    menu = ["Upload Dokumen", "Pencarian Query","About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Upload Dokumen":
        st.write("Upload Dokumen Ekstensi PDF dan DOCX")
        upload_dokumen = st.file_uploader("Pilih file pdf dan docx:", 
            accept_multiple_files=True, type=['pdf','docx'])
        if st.button("Ekstrak"):
            for upload_dokumen in upload_dokumen:
                file_details = {"FileName":upload_dokumen.name,"FileType":upload_dokumen.type,"FileSize":upload_dokumen.size}
                st.write(file_details)
                if upload_dokumen.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = docx.Document(upload_dokumen)
                    all_parag_doc = doc.paragraphs
                    st.subheader("Hasil ekstrak DOCX:")
                    for parag in all_parag_doc:
                        st.write(parag.text)
                        pr = preprocessing(parag.text)
                        st.text_area("Hasil Preprocessing: ", pr, disabled=True)
                        token = tokenizing(pr)
                        st.text_area("Hasil Tokenizing: ", token, disabled=True)
                        hasil_stopword = stopwords(token)
                        st.text_area("Hasil Stopword: ", hasil_stopword, disabled=True)
                        hasil_stemming = stemming(hasil_stopword)
                        st.text_area("Hasil Stemming: ", hasil_stemming, disabled=True)
                    
                        
                        
                        
                elif upload_dokumen.type == "application/pdf":
                    # pdfRead = PyPDF2.PdfReader(upload_dokumen)
                    # pageObj = pdfRead.pages(0)
                    # text_file2 = pageObj.extractText()
                    # st.write(text_file2)
                    raw_text = read_pdf(upload_dokumen)
                    st.subheader("Hasil ekstrak PDF:")
                    st.write(raw_text)
                    
                    pr = preprocessing(raw_text)
                    st.text_area("Hasil Preprocessing: ", pr, disabled=True)
                    token = tokenizing(pr)
                    st.text_area("Hasil Tokenizing: ", token, disabled=True)
                    hasil_stopword = stopwords(token)
                    st.text_area("Hasil Stopword: ", hasil_stopword, disabled=True)
                    hasil_stemming = stemming(hasil_stopword)
                    st.text_area("Hasil Stemming: ", hasil_stemming, disabled=True)
                
                
    elif choice == "Pencarian Query":
        query = st.text_input("Input query")
        
        
    elif choice == "About":
        st.write("aku kelompok 2")
        
    
    
if __name__ == '__main__':
    main()