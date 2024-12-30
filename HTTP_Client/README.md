# hget - HTTP Client

**hget** is a Python 3 client application that allows you to retrieve a web page from a server and save it locally as a file. It utilizes the HTTP protocol for establishing communication with the server and sending requests.

To use the program, simply execute the `hget.py` file and provide a URL as an argument. The program will then contact the corresponding server, send the request, and wait for the response. The obtained web page will be saved as a file named `download.html` in the current directory.

If you wish to specify a different file name, you can use the `-o` option followed by the desired name when running the program. For example: `python3 hget.py http://www.example.com -o output.html` will save the web page as a file named `output.html`.

This application serves as a practical exercise for students to apply client/server communication through socket programming. It also helps in gaining familiarity with the HTTP application protocol and its corresponding RFC.