# Sightings Upload Tool
The Sightings Uploader tool will validate and upload ATT&CK Sightings.

---

## Usage
The tool accepts a list of absolute and relative filepaths to your Sightings data. 

> It will recursively crawl through subdirectories.  
> It will log the status for validation and uploads.  

### Syntax: 
```
sightings-upload filepaths...

  filepath args[]
  	Specify as a space-separated list of absolute or relative file or directory paths to Sightings data
```

### Example:
```
./sightings-upload sample_data/
```

### Interpreting the validation log:

#### Example: 
```
Sighting at: ./sample_data/invalid/Directory/test_data.json

	is not valid. see errors:

			- 23.techniques.0.start_time: Does not match format 'date-time'
```
#### Interpretation:
- `23.` = At the 23rd index of the array of 'sightings' is a 'sighting' object
- `techniques.` = In this 'sighting' object is an array of 'techniques'
- `0.` = At the 0th index of this array of 'techniques' is a 'technique' object
- `start_time` = In this 'technique' object is a 'start_time' value
- `Does not match format 'date-time'` = This 'start_time' value is not a 'date-time'; see schema for details.

---