# MobilePhoneFileManager
A terminal based mobile phone file manager, support Android platform so far. Implementing using adb

# Feature
  1.Enter 'n' to go to next page, 'b' to go to previous page, 'q' to exit the program

  2.(cd + serial number of file) to enter a directory, (cd ..) to return upper level directory

  3.(push + local file path) to push local file to phone

  4.(pull + serial number of file) to pull file corresponding to serial number to local

  5.(rm + serial number of file) to remove file corresponding to serial number

  All support multiple input. Command cd is separated by '/', remaining commands are separated by ' '(space).
