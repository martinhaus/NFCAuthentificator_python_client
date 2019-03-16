# NFCAuthentificator_python_client

Host module for NFC authentication using Android device. The module enables usage of encrypted communication using NFC between Android device and NFC reader.

## Requirements

* Android NFC authenticator (To be installed on Android device) [2] 
* pyscard [3]
* pycrypto [4]


## Usage 

The module needs its Android counterpart running on Android enabled NFC device [2].

```
com = APDUCommunicator('asymmetric', False)
# Messages are encrypted from now on
response_data = com.send_message([0x00, 0x15, 0x00, 0x00], 'Hello World!')
```

## References

This repository is part of my diploma thesis - Authentication using smartphone.

[1] PAM module - https://github.com/martinhaus/NFCAuthentificator_pam_module
 
[2] Android communication module - https://github.com/martinhaus/NFCAuthentificator_android_client

[3] Pyscard library - https://pyscard.sourceforge.io/

[4] PyCrypto library - https://pypi.org/project/pycrypto/