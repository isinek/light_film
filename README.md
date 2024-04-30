# Light Film
## Requirements
 * Generate directory tree of project
 * Generate filenames
 * Optimize project workflow

## Additional requirements
 * Copy/rename project
 * Generate CSV file to check if everything is exported corectly

## Project Structure and Naming Conventions
### Main Folder Naming – Asset Name
#### TV
<TRT>_<Asset_Name_In_Camel_Case>
Example: 15_Treasure_Island_Cutdown

#### Social
<TRT>_<Asset_Name_In_Camel_Case>_<SizeDimension>_<AssetType>
 * TRT always comes first
 * Asset name with underscores in camel case; if it is a Revised or Cutdown that is usually at the end of the asset name
 * Dynamic after asset name, if it is an asset with dynamic subs on it
 * Size Dimension, if it is not 16x9 (which is default for TV, YT Bumper, and YT Trueview)
 * Asset Type, Either Vertical, Newsfeed, Vertical Tiktok, YT Trueview, or YT Bumper.

Example: 15_Treasure_Island_Cutdown_9x16_Vertical
Example: 15_Treasure_Island_Cutdown_4x5_Newsfeed
Example: 15_Treasure_Island_Cutdown_1x1_Newsfeed
Example: 15_Treasure_Island_Cutdown_Dynamic_9x16_Vertical
Example: 15_Treasure_Island_Cutdown_Dynamic_9x16_Vertical_ Tiktok
Example: 15_Treasure_Island_Cutdown_YT_Trueview
Example: 06_Treasure_Island_Cutdown_YT_Bumper

### Internal Folder Naming
Each asset should contain the following folders:
 * Ref_File
   * Contains the reference file, an .mp4
 * Audio_Splits
   * Contains all audio splits and mixes
 * GFX_Project
   * Contains the Graphics Project and any additional footage and notes
 * 2398fps
   * Contains the Texted, Textless, and Textless Clean (Textless clean for Social Verticals only, should be clean backplate with no Legals/Logos)
 * 25fps
   * Contains the Texted and Textless, for TV only
 * Script
   * Contains script for asset

### Filename conventions
The filename of the Texted and Textless Master files should follow this convention:

 * Filenaming convention: 
   * Filmcode_Assettype-Dimension_SpotName_Duration _Language_Texted/Textless_Resolution_Framerate_File Type
 * For a Dynamic Vertical:
   * Example: ARG_SOCIAL-9x16_Dynamic_ByYourSide_15s_OV-en-OV-TXT_1080x1920_2398_ProRes.mov
 * For a regular Vertical:
   * Example: ARG_SOCIAL-9x16_ByYourSide_15s_OV-en-OV-TXT_1080x1920_2398_ProRes.mov
 * For a Dynamic Tiktok Vertical
   * Example: ARG_SOCIAL-9x16_Dynamic_Tiktok_ByYourSide_15s_OV-en-OV-TXT_1080x1920_2398_ProRes.mov
 * For a regular Tiktok Vertical
   * Example: ARG_SOCIAL-9x16_Tiktok_ByYourSide_15s_OV-en-OV-TXTD_1080x1920_2398_ProRes.mov
 * For a 4x5 Newsfeed
   * Example: ARG_SOCIAL-4x5_Dynamic_ByYourSide_15s_OV-en-OV-TXT_1080x1350_2398_ProRes.mov

Notes:
 * For the asset name, there are underscores when it is the folder convention, but for the filename.mov, there should be no underscores. Ie folder 15_Asset_Name versus file AssetName_15.mov
 * Texted files would be TXT and Textless files would be TXTL

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

