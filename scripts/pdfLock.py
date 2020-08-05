# -*- coding = utf-8 -*-
# python3
# usage: pdflock.py [password] -> Path default 'Documents'.
#        pdflock.py [password] [path <optional>] -> Path given as an argument.
# Be Careful.
import PyPDF2 as pdf
import sys, os, getpass, uuid

class pdfLock:
    def __init__(self):
        arguments = len(sys.argv)
        if arguments == 1:
            print('<1|2> arguments expected...')
        elif arguments == 2:
            self.pwd = sys[1]
            self.walkInto('C:\\Users\\'+ getpass.getuser() +'\\Documents')
        elif arguments == 3:
            self.pwd = sys.argv[1]
            self.walkInto(sys.argv[2])
        else:
            print('<3+> arguments given... expected <1|2>')
    
    def walkInto(self, path):
        print('Encrypting Files...')
        for root, dirs, files in os.walk(path): 
            [self.encryptPdf(root, fname) for fname in files if fname.endswith('.pdf')]
        print('Encrypted Successfully')

    def encryptPdf(self, folder, fileName):
        with open(os.path.join(folder, fileName), 'rb') as inFile:
            pdfFile = pdf.PdfFileReader(inFile)
            pdfWrite = pdf.PdfFileWriter()
            for num in range(pdfFile.numPages):
                pdfWrite.addPage(pdfFile.getPage(num))
            pdfWrite.encrypt(self.pwd)
            with open(os.path.join(folder, uuid.uuid4().hex + '.pdf'), 'wb') as outFile:
                pdfWrite.write(outFile)
        os.remove(os.path.join(folder, fileName))



if __name__ == '__main__':
    pdfLock()

