#Synopsis
#CraftWiz
A project written in python to search websites and extract  relevant Kid's Craft information based on a search criteria

# Motivation
As parents, won't it be nice if we could have some trusted recommendations for where to find specific kid activities?
The project consists of 3 components:
 * A crawler (python)
 * A Data Model (Sqlite)
 * A UI (CLI)

 The crawler reads a json for configurations, crawls the web starting at your favorite Craft site, populates a SQL Data model,
  Ranks websites based on in-degree , and provide a UI to query the data out.

 It also features a restart capability, you can kill the crawler , and when you run it again, it will pick up where it left.


# PreRequisite:

* [Python][https://www.python.org/downloads/] (2.7.x at least)
* [Sqlite][http://sqlitebrowser.org/]


# Installation

Clone/Fork code base .
Following files are needed:
* ./config/config.json (see sample config.json.sample)
* ./data/craftdb.sqlite (only create a new database, no objects)

Run ./src/crawler.py . This should crawl based on the configuration specified and populate the data model. Process can be
killed at anytime using any keyboardinterrupt. To restart, simple re-run. Tt should pick where it stopped.

Once you have enough data, run the ./src/displayCraft.py

# Usage
<pre><code>$ displayCraft.py
Enter the text to search :chalk
Enter how many max links do you want :4
crafts matching chalk : http://tinkerlab.com/blending-chalk-pastels/
crafts matching chalk : http://www.playbasedlearning.com.au/2011/05/sugar-chalk/
crafts matching chalk : http://www.smallfriendly.com/small-friendly/2011/10/chalkboard-pumpkins.html
rafts matching chalk : http://www.readingconfetti.com/2013/05/ice-chalk.html

</code></pre>




