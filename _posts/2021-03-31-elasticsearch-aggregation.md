---
title: Elasticsearch Aggregation
categories: programming
tags:
  - analysis
  - sql
---

A few years ago, I learned to use Elasticsearch.
It took awhile for me for grok and wrap my head around, to map it to my SQL foundation.

<!-- markdownlint-disable MD033-->
<script src="https://gist.github.com/ipwnponies/9a4bbe32865b4198b6476aa36ecb22ff.js"></script>
<!-- markdownlint-enable MD033-->

## Refreshed Summary

I think this gist is still correct.
It's interesting that the interface was a REST API and the query language was a JSON blob.
This reduces the dynamic nature of it, as you couldn't spontaneously spin up a SQL cli and hand-write a fully formed SQL
query.
You needed to write or maintain the JSON query and edit it, using a JSON editor.
Because noone should have to deal with bullshit like lack of trailing commas.

### Size Key

The _size_ key is how you tell elasticsearch the limits.
Elasticsearch will happily run off to its clusters, run the query, and collect and collate a massive result set.
An orchestrator somewhere is going to make the call to cutoff and tell nodes to relax.

### Aggs Key

The _aggs_ key is how you perform aggregation functions.
It's a separate key, which doesn't jive with SQL, where aggregation functions are _projection_ components of the query.

The children of _aggs_ is the name for the new aggregate field.
Then you define the aggregation you want to perform for that term, be it _COUNT_, _DISTINCT_, _SUM_, etc.
You also define the term that the aggregation is performed on.
All this to say, it's a weird inversion and isolation of the aggregation-relevant components of a SQL query.
It might makes sense but it's been very hard to break away from my existing SQL mental model.

### Query Key

The _query_ key is the _filter_ component of a query.
You specify conditions for qualification into result set.
_Bool_ is binary qualification, which is how SQL filtering works.
The reason for calling this out is that Elasticsearch has scoring, as it's use case is for searching, especially in a
fuzzy manner.
I have not used this much but I imagine it can be powerful to find close matches.
Think matching "test" and getting results that include "test1" and "test2", with respective scoring.
You can set a score cut off and relax it as needed, if the results are sparse.

## Conclusion

I'd be interested in being able to play with elasticsearch again.
It's clearly very powerful and I feel like a toddler trying to get it to do what I want.
I think using it more for fuzzy search and results would better showcase its strength.
