# Triskelion: A Python Based Software Keylogger for Vulnerability Assessment in the Cyberspace.

The rapid evolution of technology, driven by innovative solutions, research, and market demands, has significantly advanced communication, networking, hardware, and software sectors. However, these advancements have also facilitated the rise of cybercrimes, with keylogger attacks being a notable threat to data security and privacy. This project aims to address gaps in effective detection mechanisms for and the knowledge availed to the public about software keyloggers. 

The objective is to design and develop a Python-based software keylogger named Triskelion, which will be used to assess vulnerabilities in cyberspace through an offensive approach. Triskelion will capture keystrokes, clipboard data, and screenshots from a target machine, operating in an ethically controlled environment to ensure legitimate use. The collected data will be analyzed to gain insights into keylogger evasion techniques, functionalities, and threat scope. The expected outcome is to enhance the understanding of keylogger behaviour, which will inform the development of more robust and dynamic detection mechanisms. These findings will also aid in raising user awareness about the risks posed by keyloggers and the importance of protecting sensitive information. 

Ultimately, this research aims to contribute to the cybersecurity field by providing solutions that mitigate the impact of keylogger attacks and uphold data integrity and user privacy.


## Repository Structure
- `Documentation` : Contains the project documentation, which so far is the proposal document.
- `System Diagrams` : Contains the analyis and design diagrams for the project.
- `main.py` : This is the actual keylogger program. 
- `triskelion_server.py` : This is the remote server file created using Flask to handle the storage of received files form the victim's machine.
- `requirements.txt` : This is a text file containing the python modules needed for the project.
- `README.md` : This is the README file for the project.

## Documentation
The documentation so far at this stage is the Project Proposal. It contains 3 chapters i.e.
- Introduction: This is the first chapter. It contains the bulk of the proposal as it brings the project to life highlighting the background information, problem statement, objectives, research questions, the justifications, scope, limitations and delimitations of the project. It serves the purpose of lating the foundation for the research to give an understanding on what is known about keyloggers, what the project aims to achieve and its contribution to existing knowledge in the field of cybersecurity.
- Literature Review - This is the second chapter which contains a summary of related literature involving keyloggers. It reviews the literature and reveals gaps and conflicts in prior research and places the research of Triskelion within the context of the existing literature.
- Methodology. This is the third chapter of the project proposal. It highlights the methodology and its justification, the methodology diagram, project deliverables and the tools and techniques to be employed for the project.

The documentation for the project can be found [here.](https://github.com/arnold7800x3d/Triskelion_Python_Keylogger/tree/master/Documentation)

## System Diagrams
The analysis and design diagrams drawn for the project are:
- `Use Case Diagram` : This is a diagram which provides a visual representation of how users interact with the system.
- `State Transition Diagram` : A diagram to indicate the various states the machine undergoes, the events under the changes from one state to another and the triggers from one state to another.
- `System Flowchart` : This is a visual representation of various processes, inputs, outputs and decisions that comprise a system.
- `Sequence Diagram` : This is a visual illustration of the interactions between the various components, objects or actors in a system.
- `Misuse case Diagram` : This is a diagram which stems from the use case diagram but shows the use cases that can be performed by outside actors in order to harm the system.
- `System architecture` : Conceptual model that defines the structure, behaviours and the formal representation of the system. 

The analysis and design diagrams for the project can be found [here.](https://github.com/arnold7800x3d/Triskelion_Python_Keylogger/tree/master/System%20Diagrams)

## Tools
The tools used in the development of Triskelion include:
- `Python` :  Python is a popular high-level interpreted programming language that is easy to understand, easy to learn, and very flexible. It is the language used to develop Triskelion. [https://www.python.org/](https://www.python.org/)
- `Flask` : Flask is a lightweight Python web framework used to develop Python-based webapplications as well as Application Programming Interfaces. It is used in the development of the server that handles the storage of data captured from the victim's machine [https://flask.palletsprojects.com/en/3.0.x/](https://flask.palletsprojects.com/en/3.0.x/)

## Installation
To install the required libraties for the project, run
```
pip install -r requirements.txt
```

## Testing
On the attacking device, execute the `main.py` program.
```
python main.py
```
On the remote server, which in my case is a Kali Linux Virtual Machine, run 
```
python3 triskelion.py
```
Then in the Windows Command Prompt Window check for the "success" messages indicating the successfull capture of data and sending of the files. If the files are sent successfully, they can be seen in the directory chosen to store the files. Further analysis is then carried out.

## Project Demo
For the project demo, the keylogger executable will be sent as a link to the victim device. Upon clicking the link, the keylogger executes in the user's background and captures the keystrokes, copied clipboard data and screenshots at set intervals. The data will be stored in files and then sent to a remote server for storage and analysis.

## Authors
"Triskelion: A Python Based Software Keylogger for Vulnerability Assessment in the Cyberspace" was undertaken by Arnold Ochieng' for CNS 3104: Computer Networks Project I at Strathmore University in 2024. For any questions or additional information about this project, contact the author.
- [Arnold Ochieng'](https://github.com/arnold7800)
