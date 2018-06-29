# Neato Custom Component For Home Assistant

## This custom component is no longer needed after 0.73 please delete before you restart to upgrade, there are additional fixes there as well.

This is a custom component designed for Home Assistant.  The changes here simply add support for the Botvac D7, some merged code for the start of persistent map cleaning (thanks @nathanfaber !) and the scanning interval has been reduced.

Previously the component would scan the robots every second and update the map every 10 seconds in Home Assistant.  The switch and vacuum itself would be updated at the standard interval.  The scanning now takes place once a minute so it should help reduce the amount of calls being made.  Don't be surprised if the on/off toggle is delayed in the UI as a result of these changes.

Steps to install.

1. Create a `custom_components` folder in your home assistant configuration directory if it does not exist already
2. Download the code here and place all the files inside the `custom_components` folder.  Make sure that `neato.py` from the root of the project is directly inside the `custom_components` folder.  Make sure the 3 folders are also included.
3. Leave Neato configured as it is in your configuration.yaml (or configure it according to the docs: https://www.home-assistant.io/components/neato/)
4. Restart Home Assistant

Enjoy using your Botvac D7 in Home Assistant!
