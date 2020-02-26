# Election Extension

This where the core of election system is being specialized in to different types of elections. 
This where how the election is organized with areas. tally sheets and reports. 

## Goal to be

The goal here is to make this extension able to define any kind of an election satisfying the need.

## Structure

- Each sub directory is an extension
- It has to export a python class extending `ext.ExtendedElection.ExtendedElection` class.
  - Define the area structure (Electoral districts, Polling stations, etc.)
  - Define the tally sheet templates and mappings
  - Assign tally sheet to areas as required.
  - Define report layout etc.
- `sample-config-data` folder in each extension folder provides test config data sets to create the particular election type.
