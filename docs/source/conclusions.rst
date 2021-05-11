Conclusions
===============

While this was a relatively quick implementation (80 hrs), the results are
beyond a POC, implementing a fully capable tool that can be used as it is
and expanded in the future.

In particular, the capabilities of remote monitoring using exclusively opensource
tools could represent a great advantage for new players in the industry, or
for individuals interested in the field but with limited budget

Lesson Learned
###############

**Multiprocessing** and Multhread are not implemented as parallel processing by default.
I needed to implement a daemon in order to make my processes work asyncronously

**Atomicity Rules** processing in a atomic fashion is a powerfull artifact that can be expanded
from file to batches. It is an efficient way to offer warranties to transactions being completed.

**Real-time visualization is challengin:**
Refresh rates are critical, but delays are not allowed in the critical care medical business!
For realtime plots on Django, I used chart.js and nagix real time plugin

**Dependency Hell** is real! Django channels latest release (3.x) stablished a different connection mode, but many tutorials are still using Django2/Channels 2. Plus, Websocket library has an extra dependency ... what a pain!



Next Steps
############

- Add more channels to allow more sensors

- Add option for serial reader be triggered as a daemon

- Implement a Django App to wrap up the Admin layer, instead of using Environment variables

- Implement a garbage collection daemon to take care of the files generated
