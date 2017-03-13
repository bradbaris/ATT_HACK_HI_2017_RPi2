The RPi2 was not in the original scope, but needed to send a POST request and couldn't find support for HTTPS on Arduino Uno WiFi. I had wanted to have it all on the Arduino Uno WiFi, but it being a Developer Edition meant it had a lot of new changes in the firmware and did not support existing community code. The pre-installed Ciao library took up too much space, and I couldn't figure out another way to get it to work in time. 

Previously, we had also tried using an Arduino Yún and an RPi3, but the Yún required sautering edits to the PN532 chip amongst other changes, and the RPi3 needed [a bunch of extra config](https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3/45571#45571) that didn't quite work the first few tries, and possibly some UART weirdness.  

Setup:

1. [Adafruit Guide for RFID/NFC PN532 chip](https://learn.adafruit.com/adafruit-nfc-rfid-on-raspberry-pi/overview)
  * Free UART on RPi2
  * Download, config, and build `libnfc` on the RPi2
  * Make sure the right device is set up, likely `dev/ttyACM0`
    * If device num keeps changing, may have to mess with `/etc/udev` rules, but should not be necessary. Use `dmesg` and `lsusb` to debug.
  * Test connectivity with the freshly-installed `nfc-list` and `nfc-poll` to activate. If needed, set `log_level=3` (debug) in `/etc/nfc/devices.d/pn532_on_uart_rpi.conf` file.

Notes:

[1] https://raspberrypi.stackexchange.com/questions/51498/sending-data-to-a-raspberry-pi-over-serial-connection?rq=1
