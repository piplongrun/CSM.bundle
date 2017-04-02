Common Sense Media
==================
<img src="https://img.shields.io/github/release/piplongrun/CSM.bundle.png?style=flat-square">

What is Common Sense Media?
---------------------------
Common Sense Media is a metadata agent for Plex Media Server that adds their recommended age as content rating. It will optionally add a short description as tagline and the Common Sense movie review to reviews.

Requirements
------------
A Plex movie library with the _Plex Movie_ agent or _The Movie Database_ agent set as primary agent.

How do I install Common Sense Media?
------------------------------------
You can install Common Sense Media:

 - From within the Unsupported AppStore, or:
 - Manually: See the support article "[How do I manually install a channel?](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-)" over at the Plex support website.

Don't forget to activate the agent in *Settings* > *Server* > *Agents* after installing. Drag it all the way to the top of the list to prevent other agents from overruling the content rating.

Where do I download Common Sense Media?
---------------------------------------
If you want to install the agent manually or if you are interested in the source code, you can download the latest copy of the agent from Github: [releases](https://github.com/piplongrun/CSM.bundle/releases)

Limitations and Known Issues
----------------------------
 - Due to not being able to grab certain data directly I had to build a small API that takes IMDb ids and returns required data. This API is still a bit slow due to a number of http requests it has to do. Lots of requests are cached, so the more the agent gets used, the faster it will become.

Where do I report issues?
-------------------------
Create an [issue on Github](https://github.com/piplongrun/CSM.bundle/issues) and add as much information as possible:
 - Plex Media Server version
 - Primary agent and order of any secondary agents
 - Log files, `com.plexapp.agents.csm.log`

<img src="https://raw.githubusercontent.com/piplongrun/CSM.bundle/master/Contents/Resources/icon-default.jpg" width="150">
