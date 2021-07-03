*This digital tool is part of the catalog of tools of the **Inter-American Development Bank**. You can learn more about the IDB initiative at [code.iadb.org](https://code.iadb.org/en)*

<p align="center">
  <img height="200" src="img/logo.png">
</p>

  # <img height="30" src="https://img.icons8.com/flat-round/64/000000/fire-element.png"/> burned-area-detection  
  

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/dymaxionlabs/burned-area-detection/blob/master/LICENSE.txt)



<br>
<p align="center">Detection of burned areas using deep learning from satellite images.</p>

<p align="center">
  <img height="300" widht="500" src="img/burn.jpg">
</p>

<p  align="center">
• <a  href="#-description">Description</a> •
<a  href="#notebook-notebooks">Notebooks</a> •
<a  href="#-about-dymaxion-labs">About Dymaxion Labs</a> •
<a  href="#handshake-contributing">Contributing</a> •
<a  href="#page_facing_up-license">License</a> •
</p>

## <img height="25" src="https://code.iadb.org/sites/default/files/2019-04/31227283.png"/> Description

The burned-area-detection project aims to identify and analyze the affected
areas after a fire incident. It allows us to understand incident behavior to
take action shortly.

The number of uncontrolled fires has increased significantly in the last few
years. This kind of environmental catastrophe affects habitat and community on
several levels. The impact on our environment can be evidenced in a short time
by measuring the wellness and the evacuation process of the different
communities living in affected areas. But we are also able to notice its
effects in the long term due to the impact on nature and local economies. Some
of the project's principal goals are measuring these affected areas. 

This project uses Sentinel-2 public satellite images. Sentinel-2 has high
cadence at no cost, allowing the study of the affected area's evolution across
time. These images can be download from Google Earth Engine. There are several
reflectance bands available to use, besides a combination of them can be more
sensitive to detect burn areas.

### Normalized Burn Ratio (NBR)

The Normalized Burn Ratio (NBR) is an index that highlights burnt areas in
large fire zones. The formula combines the near-infrared (NIR) and shortwave
infrared (SWIR) wavelengths.

Healthy vegetation shows a very high reflectance in the NIR, and low
reflectance in the SWIR portion of the spectrum, (see figure below). The
contrary happens for areas destroyed by fire; recently burnt areas show a low
reflectance in the NIR and high reflectance in the SWIR. Therefore, the
normalized difference between the NIR and the SWIR is a good discriminant for
this kind of phenomenon.
<p align="center">
  <img widht="500" src="img/Spectral_responses.jpg">
</p>


### Burn Severity

The difference between the pre-fire and post-fire NBR obtained from the images
is used to calculate the delta NBR. A higher value of dNBR indicates more
severe damage, while areas with negative dNBR values may indicate regrowth
following a fire.

Uses [satproc](https://github.com/dymaxionlabs/satproc) and
[unetseg](https://github.com/dymaxionlabs/unetseg) Python packages.


## 	:notebook: Notebooks

This repository contains a set of Jupyter Notebooks describing the steps for
building a semantic segmentation model based on the U-Net architecture for
detecting burned areas from fires from optical satellite imagery.

1. [Pre-process](1_Pre-process.ipynb): Image and ground truth data preprocessing and dataset generation
2. [Training](2_Training.ipynb): Model training and evaluation
3. [Prediction](3_Prediction.ipynb): Prediction
4. [Post-process](4_Post-process.ipynb): Post-processing of prediction results

## <img height="25" src="https://code.iadb.org/sites/default/files/2019-04/31227283.png"/> About Dymaxion Labs
[Dymaxion Labs](https://dymaxionlabs.com/) leverages AI and Computer Vision to analyze petabytes of geospatial data to understand the physical world. These include optical, SAR and aerial imagery, climate data, and IoT sensors.
With our grounded, data science based methodology, private companies and the public sector accelerate strategic data-driven decisions from their remote targets.
### :man_technologist: Authors
* María Roberta Devesa <ro.devesa@dymaxionlabs.com>
* Damián Silvani <damian@dymaxionlabs.com>



## :handshake: Contributing

Bug reports and pull requests are welcome on GitHub at the [issues
page](https://github.com/dymaxionlabs/burned-area-detection). This project is
intended to be a safe, welcoming space for collaboration, and contributors are
expected to adhere to the [Contributor
Covenant](http://contributor-covenant.org) code of conduct.

## :page_facing_up: License

This project is licensed under Apache 2.0. Refer to [LICENSE.txt](LICENSE.txt).
