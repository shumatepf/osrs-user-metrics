# Old School Runescape User Metrics
osrs-user-metrics is a Python Flask application in front of an InfluxDB time series database. On a regular basis, select Old School Runescape hiscores are scraped and dumped into InfluxDB. 
The data is interfaced through the Flask application and prepared for various (planned) graphs and diagrams for user analysis. osrs-user-metrics is Docker ready and can be launched locally
in only a few steps.

## Purpose
Old School Runescape is an MMORPG with a heavy focus on tedious exp grinds. Player exp data is published to the hiscores page (if that players' level is high enough), which can be compared 
against all other players on the hiscores. Currently, the hiscores page only displays the most up-to-date character exp. This app aims to provide historic access to hiscores via a 
time series database. 
