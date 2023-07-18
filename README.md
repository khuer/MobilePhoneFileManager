# MobilePhoneFileManager
A terminal based mobile phone file manager, support Android platform so far. Implementing using adb

# Feature
(cd + serial number of file) to enter a directory, (cd ..) to return upper level directory

(push + local file path) to push local file to phone

(pull + serial number of file) to pull file corresponding to serial number to local

(rm + serial number of file) to remove file corresponding to serial number

All support multiple input. Command cd is separated by '/', remaining commands are separated by ' '(space).
