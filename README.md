National Map CKAN Preview plugin
================================

A plugin to CKAN to use National Map as a previewer for data.gov.au.

The goal of this project is to be open source when it releases, so all work
 should be carried out with that in mind.

Uses https://github.com/mapbox/geojson-extent

### Getting Started ###

Check the [wiki](https://github.com/NICTA/nationalmap/wiki) for 
more information about how to get this working with CKAN

#### From Git Repository ####
* Log in to github
* Fork the [NationalMap](https://github.com/NICTA/nationalmap.git) repo into your personal github account using the github UI.
* Clone your forks locally so data is inside subspace at root level e.g.

### Installation ###

Move to ckan src directory. By default it `/usr/lib/ckan/default/src`
```bash
cd /usr/lib/ckan/default/src/
```
Clone master repository
```bash 
git clone https://github.com/Atmoterm/ckanext-cesiumpreview.git
```
Activate venv
```bash
. /usr/lib/ckan/default/bin/activate.sh
```
Finaly, run setup.py file with `install` key to finish prod installation
```bash 
sudo /usr/lib/ckan/default/bin/python setup.py install
```
