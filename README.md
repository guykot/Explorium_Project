# OSM Project
This document defines all the processes I have done through the OSM project.<br>
**Project's Goal:** Report amenities from Open Street Map (OSM) aggregated by street name for south America.<br>
<br>
**Data Processing and Algorithm:** <br>
OSM defines 3 types of data elements: Nods, Relations and Ways.<br>
All the definitions can be found here:<br>
https://wiki.openstreetmap.org/wiki/Elements<br>
To aggregate the amenity nodes by the street name I used two different algorithms:<br>
<br>
Ways - Base algorithm.<br>
Relation - Base algorithm.<br>

**Relation - Base Algorithm:**<br>
An algorithm which is using all the 3 elements of OSM.<br>
From the relation elements, it generates the street names by filtering only the data which has a role index as ‘street’. This guarantees that only the relations of street are filtered.<br>
In the next step the algorithm joins the ‘ways’ table to ‘relations’ on the way-Id column.<br>
By these we can get all the ways and their nodes which defines the street.<br>
From the node table, the algorithm selects only the Node ID and filters only the ones tagged as ‘amenity’.<br>
The final step is to join the table/relation with the nodes table so we can get all the nodes that are tagged as amenity with their street name.<br>
To get aggregated data we just group the table and import it to a CSV file.<br>
 <br>
**Ways-Base Algorithm:**<br>
In the OSM link: https://wiki.openstreetmap.org/wiki/Way there is an example of how to define a “street” element as a vector.<br>
The ways-base algorithm is querying all the ways that have the same struct as shown in the example: A way with a tag’s key of ‘name’ and a tag with a value of ‘residential’.<br>
It is important to note that the above assumptions are very easy and not all streets will meet the above criteria.<br>
From the nodes table, the algorithm exude the same process as Relation-base, it selects the node ID which is tagged as ‘amenity’.<br>
Finally, the algorithm joins the two tables and group the result.<br>
 <br>
**Exploring The Data And Analyzing The Results:**<br>
Relation-base algorithm:<br>
This algorithm executed 7 nodes which is clearly not a good result.<br>
To understand the cause of it we can explore the data and understand the quality of it:<br>
The number of overall ways that were tagged to a street is 22777 (from relation df.coumt()).<br>
The number of overall ways in South America is 22441879.<br>
Meaning, just 0.1% of the ways in South America were tagged in a relation connection and received a street name.<br>
In addition, the number of overall nodes is 266629614, and 509745 of them were tagged as ‘amenity’.<br>
It’s less than 0.2%.<br>
Conclusion:<br>
Not enough nodes were tagged as amenity and not enough ways connected to a street relation.<br>
With such a low presence of valid data, we can say that the relation-base algorithm is not a valid process to establish this aggregate task.<br>
Way-base algorithm:<br>
Results of 753 of nodes connected to streets.<br>
Out of 509745 of total amenity node, that is less than 0.14 %.<br>
Conclusion:<br>
Again, not enough linked data (from ways to nodes) so the algorithm will execute good results. <br>
<br>
**Recommendations to continue:**<br>
Of all of the above, my suggestion for optimizing the results is to aggragte nodes by geographically relationship.<br>
Meaning nodes that were tagged with a street name can link to all the others nodes around them by their geographical proximity.<br>
For example, we can take all the nodes from streets, create a table of them with their lat/long columns.<br>
For each node in the general nodes table (which are tagged only as amenity), we can check if their positions is in 200 meters radios around the nodes which already tagged in the street, and if they do we can tag them in same street.<br>
This is a heavy process, O (n^2) , but it will optimize the results.<br>
