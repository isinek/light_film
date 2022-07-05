# Light Film
## Requirements
 * Generate directory tree of project
 * Generate filenames
 * Optimize project workflow

## Additional requirements
 * Copy/rename project
 * Generate CSV file to check if everything is exported corectly

## Project data

**Filename example**: `TR2_NewsfeedSpots_Treat_30s_ComingSoon_UK_en_OV_TXTD_1080x1080_2398_ProRes`

| Entity						| Description							| Example			|
|-------------------------------|---------------------------------------|-------------------|
| project code					| 3 letter code representing film title | TR2				|
| project type					| Asset type category					| SocialMedia		|
| asset type					| Description of creative type			| NewsfeedSports	|
| asset name					| Individual asset or concept name		| Treat				|
| dimensions or video length	| Banner size (WxH) or video length in seconds	| 30s		|
| variation						| Differentiating description (eg. Out Now)	| CommingSoon	|
| market						| Primary country for asset to run in	| UK				|
| language						| Language of video						| en				|
| dubbed or subtitled			| Label to indicate if dubbing or subtitle has been applied	| OV |
| texted or textless			| Details on text information for the creative asset 	| TXTD	|
| resolution					| Video resolution for primary asset	| 1080x1080			|
| frame rate					| Video frame rate for primary asset	| 23.98				|
| format						| Video file type						| ProRes			|
| local asset name				| Localised / translated asset name		| 					|

## ~~Solution 1~~
 1. Entering project data
 2. Generate directory structure
 3. Export video to generated directory

### Pros
 * clear directory structure from the begining
 * if empty files are generated, there's no need to generate filenames again

### Cons
 * search for file directory manually
 * only difference between empty and final video is file size

## Solution 2
 1. Entering project data
 2. Export all videos with generated filenames to single directory
 3. Generate directory structure from filenames and move files there

### Pros
 * export everything to one place, no need to search for right directory
 * possible to generate directory structure for multiple projects at once

### Cons
 * strict file naming rules

## Open questions
 * Clearly define usage of - and _ in filenames
	* `TR2_NewsfeedSpots_Treat_30s_ComingSoon_`**UK-en-OV-TXTD**`_1080x1080_2398_Prores_[Local]`
 * Tool preferences
	* ~~Google sheet~~
	* ~~script~~
	* python app

## Working hours
| Description	| Current	| Expected	|
|---------------|-----------|-----------|
| Meetings		| 	 8 h	| 	10 h	|
| POC			| 	 5 h	| 	 5 h	|
| Development	| 	35 h	| 	25 h	|
| Documentation	| 	 2 h	| 	 2 h	|
