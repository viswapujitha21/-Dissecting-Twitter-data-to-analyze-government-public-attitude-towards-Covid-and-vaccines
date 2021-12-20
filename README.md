# -Dissecting-Twitter-data-to-analyze-government-public-attitude-towards-Covid-and-vaccines

**IMPLEMENTATION:**
As a part of this project, we have implemented a Search Engine and performed content analysis. We have implemented the below functionalities in our web application:
Created a webpage to perform search operations on our indexed data related to covid and vaccines.
There is search page on our home similar to google search where users can search for any term related to covid.
Once the user clicks enter, he will be able to see different information on both the sides: 
Left side of our web page renders faceted search functionality which displays the tweets and the top replies. We have also displayed the overall public response for that tweet along with some top replies. 
Right side of our web page displays the graphs obtained with respect to the searched query which includes:
Sentiment Analysis of General Population Tweets
Sentiment Analysis of replies to POI tweets
There is an overview tab that displays below items :
Trending topics present in our data.
Country wise distribution of tweets
Language wise distribution of tweets
Worldcloud of vaccine hesitancy in general population tweets(it’s an image)
Covid and non-covid distribution of POI tweets

**Technologies used:**
The Web stack that we have used to implement this search engine is Python with Django Framework. Solr is used for indexing whereas Bootstrap, CSS is used for styling and several other libraries such as matplotlib, plotly, rest framework etc to aid the development.

**collecting the data:**
we have collected several tweets from multiple POIs from three different countries - India, USA and Mexico. Also collected replies for these tweets. We have used the tweets collected to power the data for this project. This Data is present in the data folder of the project.

**Indexing:**
We have indexed the data from the data folder into the solr. (The code for this is present in indexer.py / indexer-aws.py which are used for indexing data in local / remote respectively) We are using the BM25 to rank the documents for a given search term.

**Code:**
The main API that powers the backend is the search API. This API also takes care of the filtering.  Whenever the user enters a search term and clicks on enter the API will be hit and the following process takes place:
Perform Query cleaning by removing special characters, whitespace.
Performs query optimization to improve the search results. 
Prepares a Solr URL by using the search term and the filters provided by the user.
Hits the Solr with the URL and get the top results for the search term.
For each tweet, collects replies, if any, and modify the result object to incorporate the replies.
Performs sentiment analysis on the replies to understand the public response to a particular tweet. Each tweet will be assigned one value (positive, negative, neutral) which is calculated by considering all the replies.
Modify the result and send the result object which contains tweets and related information.
Result Object will contain a list of tweet objects. 


**METHODOLOGY:**
Evaluation Methodology: 
We are using the BM25 to rank the documents for a given search term. BM25 (BM is an abbreviation of best matching) is a ranking function used by search engines to estimate the relevance of documents to a given search query. It is based on the probabilistic retrieval framework.




