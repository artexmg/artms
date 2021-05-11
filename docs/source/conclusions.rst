Conclusions
===============

While this was a relatively quick implementation (~80 hrs), the results are far more than
a POC. I was able to develop a fully capable framework that can be used as it is, but also it
is expandable due to its modular design.

Its capabilities of remote monitoring and data collection without having to use propietary
software could represent a great advantage for new players in the industry, or
for individuals interested in the field but with limited budget.

Also, this system is not limited to reading ventilator data, but it is capable to acquire
any serial data being injected via serial port, in that regard it can be used as an general purpose IoT
platform.

Lessons Learned
###############

**Multiprocessing** and Multithreading are not implemented as parallel processing by default.
I needed to implement a daemon in order to make my processes work asynchronously

**Atomicity Rules!** Processing in a atomic fashion is a powerful artifact that can be expanded
from file to batches. It is an efficient way to offer warranties to transactions being completed.

**Real-time visualization is challenging:**
Refresh rates are critical, but delays are not allowed in the critical care medical business!
For realtime plots on Django, I used chart.js and nagix real time plugin

**Dependency Hell is real!** Django channels latest release (3.x) established a different connection mode, but many tutorials are still using Django2/Channels 2. Plus, Websocket library has an extra dependency ... what a pain!



Next Steps
############

- Add more channels to allow more sensors

- Add option for serial reader be triggered as a daemon

- Implement a Django App to wrap up the Admin layer, instead of using Environment variables

- Implement a garbage collection daemon to take care of the files generated
