# Neato Custom Component For Home Assistant

This is a custom component designed for Home Assistant to test new Neato features.

Currently testing: cleaning additional floorplans using `map` in the service call

Steps to install.

1. Create a `custom_components` folder in your home assistant configuration directory if it does not exist already
2. Download the code here and place entire `neato` directory and all the files inside it into the `custom_components` folder.
3. Leave Neato configured as it is in your configuration.yaml (or configure it according to the docs: https://www.home-assistant.io/components/neato/)
4. Restart Home Assistant

Enjoy using your Botvac in Home Assistant!

Service call: `vacuum.neato_custom_cleaning`

Service data for cleaning with a map only, see official docs for all other accepted parameters:  
`
{
"entity_id":"vacuum.neato",
"map": "<map name from neato app>"
}
`
