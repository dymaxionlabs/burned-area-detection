# burned-area-detection


The burned-area-detection project aims to identify and analyze the affected areas after a fire incident. It allows us to understand incident behavior to take action shortly.

The number of uncontrolled fires has increased significantly in the last few years. This kind of environmental catastrophe affects habitat and community on several levels. The impact on our environment can be evidenced in a short time by measuring the wellness and the evacuation process of the different communities living in affected areas. But we are also able to notice its effects in the long term due to the impact on nature and local economies. Some of the project's principal goals are measuring these affected areas. 
This project uses Sentinel-2 public satellite images. Sentinel-2 has high cadence at no cost, allowing the study of the affected area's evolution across time. These images can be download from Google Earth Engine. There are several reflectance bands available to use, besides a combination of them can be more sensitive to detect burn areas.
## Normalized Burn Ratio (NBR)
The Normalized Burn Ratio (NBR) is an index that highlights burnt areas in large fire zones. The formula combines the near-infrared (NIR) and shortwave infrared (SWIR) wavelengths.
Healthy vegetation shows a very high reflectance in the NIR, and low reflectance in the SWIR portion of the spectrum, (see figure below). The contrary happens for areas destroyed by fire; recently burnt areas show a low reflectance in the NIR and high reflectance in the SWIR. Therefore, the normalized difference between the NIR and the SWIR is a good discriminant for this kind of phenomenon.

![Spectral_responses](https://gitlab.com/dymaxionlabs/incendios-forestales/-/blob/master/img/Spectral_responses.jpg)

## Burn Severity
The difference between the pre-fire and post-fire NBR obtained from the images is used to calculate the delta NBR. A higher value of dNBR indicates more severe damage, while areas with negative dNBR values may indicate regrowth following a fire.
