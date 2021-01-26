# Application DnD Manager

A python web application to organize, plan and comment on your d&d game with
friends or new friends.

## No need a high charisma to show your good profile

On your profile you can manage and show (or not) :
 - Your info
 - Your statue 
 - Your characters
 - Your campaigns
 - Your sessions

Your statue can show if you are available as a player or dungeon master, if you
actively search a party to play or master and the number of campaigns you
already are in.

Each character's profile has their base info (name race class lvl) and can have
a pdf version of the sheet, the link to the digital version (D&D Beyond, Embers
RPG Vault, Reroll or other). You can indicate if this character follows some
creation rule (PHB+1 or other) and if it uses a homebrew. Your character page
keeps track of which campaign it’s in and passed one shot, finished campaign
and session it has been played with.

The campaign profile allows you to manage which players and characters play in.
It also manages the date of sessions and what virtual table you use. You can
add a resume to give context on this campaign and link your Wordanvil or other
info on your campaign.


## Investigation check with advantage

Characters, campaigns or sessions can be joined to your post to keep your
player updated, ask others their opinion, make people know that you need a DM
or anything else.

You can create a post at the creation of a character with a default “welcome to
the word” message or you can personalize it. Same concept with campaign.

Some posts can be more interactive than simple messages. Some sessions posts
can ask players to confirm their participation, and some campaigns posts can 
permit players to send their character.


## An academic project.
This repository is one of the deliverable for the 13th project from the
Openclassrooms’s paths
[“Développeur d'application - Python”](https://openclassrooms.com/fr/paths/68/projects/162/assignment)
.

The project, which is the final project of this parkour, is limited to 120h,
so some functionality will stay as "won't have" due to limited time.

## Setup.
This project uses a django framework.

After installing the requirements using pip install -r requirements.txt or by
author means, you can use the manage.py migrate then the manage.py
sample command before the runserver command to set up the website. 

If you wish to test the code you can do it using manage.py test followed by
the name of the app you want to test. The functional_tests contains the
functional test and only works on local with an Edge web browser.
