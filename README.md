# Triskelion: A Python Based Software Keylogger for Vulnerability Assessment in the Cyberspace.

The rapid evolution of technology, driven by innovative solutions, research, and market demands, has significantly advanced communication, networking, hardware, and software sectors. However, these advancements have also facilitated the rise of cybercrimes, with keylogger attacks being a notable threat to data security and privacy. This project aims to address gaps in effective detection mechanisms for and the knowledge availed to the public about software keyloggers. 

The objective is to design and develop a Python-based software keylogger named Triskelion, which will be used to assess vulnerabilities in cyberspace through an offensive approach. Triskelion will capture keystrokes, clipboard data, and screenshots from a target machine, operating in an ethically controlled environment to ensure legitimate use. The collected data will be analyzed to gain insights into keylogger evasion techniques, functionalities, and threat scope. The expected outcome is to enhance the understanding of keylogger behaviour, which will inform the development of more robust and dynamic detection mechanisms. These findings will also aid in raising user awareness about the risks posed by keyloggers and the importance of protecting sensitive information. 

Ultimately, this research aims to contribute to the cybersecurity field by providing solutions that mitigate the impact of keylogger attacks and uphold data integrity and user privacy.


## Repository Structure
- `Documentation` : Contains the project documentation, which so far is the proposal document.
- `System Diagrams` : Contains the analyis and design diagrams for the project.
- `templates` : Contains the server's webpage.
- `windows-x64-npu-updater.py` : This is the actual keylogger program.
- `windows.ico` : This is the icon for the keylogger executable.
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
- `Flask` : Flask is a lightweight Python web framework used to develop Python-based webapplications as well as Application Programming Interfaces. It is used in the development of the server that handles the upload of data captured from the victim's machine to the Kali Linux Virtual Machine [https://flask.palletsprojects.com/en/3.0.x/](https://flask.palletsprojects.com/en/3.0.x/)
- `HTML/CSS` : For development of the simple webpage served by the server.
- `Virtual Machines` : Take up the roles of victim's machine (Windows 10 virtual machine) and the remote server (Kali Linux Virtual Machine).
- `Oracle VirtualBox` : Hypervisor for hosting the virtual machines.

## Installation
To install the required libraries for the project, run
```
pip install -r requirements.txt
```

## Testing
On the attacking device, execute the `main.py` program.
```
python windows-x64-npu-updater.py
```
On the remote server, which in my case is a Kali Linux Virtual Machine, run 
```
python3 triskelion_server.py
```
Then in the Windows Command Prompt Window check for the "success" messages indicating the successfull capture of data, encryption and sending of the files. If the files are sent successfully, they can be seen in the directory chosen to store the files. Further analysis is then carried out.

## Results
1) If Python is not installed, Python version 3.10.0 is installed on the system.
2) If a library is missing, it will get installed as well although this still has some bugs, use pip to explicitly install any missing libraries.
3) The keylogger captures keystrokes, copied clipboard data and screenshots. This data is saved in files of type .txt, .txt and .png respectively.
4) An encryption key is generated and used to encrypt these files.
5) The files as well as the encryption key are sent to the remote server.
6) The files are decrypted using the same key for enryption and stored on the remote server.
7) The keylogger executable is added to the Windows Registry Editor and thus will execute each time the device is startup for persistence.
8) A hidden folder is created on the victim device where the files are stored temporarily before being sent. After they are sent they are then deleted.

## Project Demo
For the project demo, the keylogger executable will be sent as a link to the victim device. Upon clicking the link, the keylogger executes in the user's background and captures the keystrokes, copied clipboard data and screenshots at set intervals. The data will be stored in files and then sent to a remote server for storage and analysis. Below is a walkthrough of the project demo:
1) Clone the project by running
   ```
   git clone https://github.com/arnold7800x3d/Triskelion_Python_Keylogger.git
   ```
2) Convert the keylogger program into an executable. Before this, ensure the IP address defined in this code is that for the Kali Linux Virtual Machine which is the actor for the remote server. This is what will be sent to a victim to download on their device. Make sure you have pyinstaller installed. To install it, run 
```pip install pyinstaller```
There are two ways to go about this second step:
   (i) Convert the program into an executable which runs in the background with no console window. This is primarily the keylogger's design. To achieve this, open a terminal in the program's directory and run
   ```
   pyinstaller --onefile --windowed --icon=windows.ico windows-x64-npu-updater.py
   ```
  (ii) Convert the program into an executable which runs in the background but has a console window. This is especially for testing and debugging. For this, run
  ```
  pyinstaller --onefile --console --icon=windows.ico windows-x64-npu-updater.py
  ```
3) Upload the file on a file hosting software. I recommend Dropbox since it generates a link which quickly initiates a download when clicked. Upload the file and generate a link which will be shared to the victim device. The link generated ends with the value 0, i.e https://dropbox.xxxxxxxxxx=0. Change the 0 to 1 for automatic download when the link is clicked.
4) Send the link to the victim's device. Windows Defender will flag the executable as malicious, thus head over to Virus and Threat Protection settings and add the Downloads directory into the exclusion list such that Windows Defender won't search for malware in that directory.
5) Download and run the keylogger executable. On the remote server, ensure the code for the server is running before running the keylogger executable.

## Authors
"Triskelion: A Python Based Software Keylogger for Vulnerability Assessment in the Cyberspace" was undertaken by Arnold Ochieng' for CNS 3104: Computer Networks Project I at Strathmore University in 2024. For any questions or additional information about this project, contact the author.
- [Arnold Ochieng'](https://github.com/arnold7800)
