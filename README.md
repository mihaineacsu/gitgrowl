gitgrowl
========

Github repository activity aggregator

Install
-------

<pre><code>sudo python setup.py install
</code></pre>

###### Usage:
<pre><code>gitgrowl events
</code></pre>
This creates .gitgrowl_configure, .gitgrowl.sqlite and updates
.gitignore with these 2 files. Afterwards it fetches issues 
and pull requests, updates db and displays events if rules apply.

Rules to be added in .gitgrowl_config (python dict).
