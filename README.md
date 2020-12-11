# Neato Custom Component For Home Assistant

This is a custom component designed for Home Assistant to test new Neato features.

Currently testing: Neato Oauth

Steps to install.

1. Create a `custom_components` folder in your home assistant configuration directory if it does not exist already
2. Download the code here and place entire `neato` directory and all the files inside it into the `custom_components` folder.
3. Navigate to: https://developers.neatorobotics.com/applications
4. Create and/or login to your Neato account
5. Proceed to create an application
6. Give the application a name (can be anything)
7. Give the application a description (can be anything)
8. Enter your externally facing URL,  if you use `https://hass.example.com` then you will use the following URI: `https://hass.example.com/auth/external/callback` It must have SSL and be externally facing.
9. Check all 3 scope check boxes
10. Save the application
11. Modify the neato configuration to match the below. You will need to replace `CLIENT_SECRET` and `CLIENT_ID` with the ones proviced by Neato after completing step 10:

```
neato:
  client_secret: CLIENT_SECRET
  client_id: CLIENT_ID
```
12. Restart Home Assistant
13. Setup Neato via the integration panel
14. When prompted sign back into Neato and accept the scopes for the application.
15. Navigate back to Home Assistant and your entities will start to reappear.
16. If you previously had Neato configured you may need to remove the integration and add it back, may not be necessary but mentioning it in case anyone has an issue.

Enjoy using your Botvac in Home Assistant!
