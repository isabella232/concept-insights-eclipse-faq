Sample for Watson Concept Insights - Eclipse FAQ
================================================================================

The [concept-insights-eclipse-faq](https://github.com/IBM-Bluemix/concept-insights-eclipse-faq) project contains sample code that shows how to use the [Watson Concept Insights](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/concept-insights.html) service and the [Watson Document Conversion](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/document-conversion.html) service with data from the official [Eclipse FAQ](https://wiki.eclipse.org/The_Official_Eclipse_FAQs).

Rather than limiting findings to traditional text matching, Concept Insights explores information based on the concepts behind your input. Let's use the Eclipse FAQ and the email client [Lotus Notes](https://en.wikipedia.org/wiki/IBM_Notes) as an example. Lotus Notes leverages the Rich Client Platform from Eclipse. The term 'Lotus Notes' is not mentioned in the Eclipse FAQs. With search functionality that use only text matching you wouldn't find any documents.

The Concept Insights service however uses concepts and graphs of concepts. It leverages the concept graph of the English version of Wikipedia. The service also creates concept maps for the input data you provide, in this case the Eclipse FAQs. Via the graph the service can find potentially related documents. For example in the Wikipedia article for Lotus Notes it is mentioned that it uses the Eclipse Rich Client Platform. Since there are documents in the Eclipse FAQ with this concept they are returned when searching for the term Lotus Notes.

![alt text](https://raw.githubusercontent.com/IBM-Bluemix/concept-insights-eclipse-faq/master/screenshots/conceptinsights3.png "Concept Insights Sample")

Another example is a search for 'Ginni Rometty' who is not mentioned in the Eclipse FAQ but the search results contain documents that are associated with the concept 'IBM'.

![alt text](https://raw.githubusercontent.com/IBM-Bluemix/concept-insights-eclipse-faq/master/screenshots/conceptinsights6.png "Concept Insights Sample")

Check out the [screenshots](https://github.com/IBM-Bluemix/concept-insights-eclipse-faq/tree/master/screenshots) for more samples. 

Authors: Niklas Heidloff [@nheidloff](http://twitter.com/nheidloff) and Hiroaki Komine (hkomine@jp.ibm.com)

Thanks a lot to Hiro for providing OfficialEclipseFAQs.csv, download.py and convert.py!


Setup
================================================================================

Make sure the following tools are installed and on your path.

* [python](https://www.python.org/downloads/)
* [curl](http://curl.haxx.se/download.html)
* [git](https://git-scm.com/downloads)

Invoke the following command to download the project.

```sh
$ git clone https://github.com/IBM-Bluemix/concept-insights-eclipse-faq.git
```


Download Eclipse FAQs
--------------------------------------------------------------------------------

In order to download the Eclipse FAQs as HTML files invoke these commands.

```sh
$ mkdir html
$ python download.py -c OfficialEclipseFAQs.csv -o html
```


Convert HTML Files
--------------------------------------------------------------------------------

In order to extract the content from the HTML files the [Document Conversion](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/document-conversion.html) service is used. You need to create an instance of this service on [Bluemix](https://console.ng.bluemix.net/catalog/services/document-conversion/) to receive credentials.

After this invoke these commands. Replace 'username:password' with your credentials.

```sh
$ mkdir converted
$ python convert.py -u username:password -c OfficialEclipseFAQs.csv -i html -o converted
```


Upload Documents to Watson
--------------------------------------------------------------------------------

For the next steps you need to create an instance of the [Concept Insights](https://console.ng.bluemix.net/catalog/services/concept-insights/) service on Bluemix to get a second set of credentials.

After this you need to get your account_id via the following command. Check out the [API Explorer](https://watson-api-explorer.mybluemix.net/apis/concept-insights-v2) to find out more. Replace 'username:password' with your credentials.

```sh
$ curl -u username:password 'https://gateway.watsonplatform.net/concept-insights/api/v2/accounts'
```

Next you need to create your own corpus 'eclipseFAQCorpus'. Replace 'username:password' with your credentials and enter your account_id.

```sh
$ curl -u username:password -X PUT -d '{}' 'https://gateway.watsonplatform.net/concept-insights/api/v2/corpora/your-account_id/eclipseFAQCorpus'
```

In the last step invoke the following command to upload the data to Watson. Replace 'username:password' with your credentials and enter your account_id.

```sh
$ python upload.py -u username:password -a your-account_id -c OfficialEclipseFAQs.csv -i converted
```


Try the Sample
================================================================================

Open the dashboard of your Concept Insights service instance in Bluemix and pick your Eclipse corpus in the combobox. On the Conceptional Search tab you can invoke searches.