import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

import time


def get_scientists_linked_in_page(page, limit_number = 10000):
    file_format = 'json'
    links = requests.get('https://en.wikipedia.org/w/api.php?action=query&generator=links' 
                     + '&gpllimit=' + '10000' 
                     + '&format=' + file_format
                     + '&redirects=1&titles=' + page
                     + '&prop=pageprops')
    target_json = links.json()['query']['pages']
    
    base_dataframe = pd.DataFrame(columns = ["pageid", "ns", "title", "pageprops.defaultsort", "pageprops.page_image_free", "pageprops.wikibase_item"])
    
    for i in target_json:
        new_dataframe = pd.json_normalize(target_json[i])
        base_dataframe = base_dataframe.append(new_dataframe)
    
    final_dataframe = base_dataframe.drop_duplicates()
    
    df = return_instances_of_specific_qid(final_dataframe['pageprops.wikibase_item'], "Q5")

    df_researchers = return_items_which_are_connected_to_items_from_a_subclass(df['QID'], target_property="P106", target_subclass = "Q1650915" )
    
    # Selecting only the columns we are interested in:
    
    final_dataframe = final_dataframe[final_dataframe['pageprops.wikibase_item'].isin(df_researchers['QID'])]
    final_dataframe = final_dataframe[["pageid", "title", "pageprops.wikibase_item"]]
    final_dataframe.columns = ["wikipedia_id", "wikipedia_title", "wikidata_qid"]
    
    final_dataframe['list_of_origin'] = page
    return(final_dataframe)
    

def recursive_get_scientists_linked_in_page(page):
    try:
        print('trying')
        df = get_scientists_linked_in_page(page)

        return(df)
    except:
        recursive_get_scientists_linked_in_page(page)
        
    


def get_citations_by_qid(qid):
    
    time.sleep(5)
    
    sparql_query  = """
#defaultView:Table
# Author's most cited works
SELECT ?count ?work ?workLabel 
WITH {
  SELECT (count(?citing_work) as ?count) ?work WHERE {
    ?work wdt:P50 wd:""" + qid + """.
    OPTIONAL { ?citing_work wdt:P2860 ?work . }
  }
  GROUP BY ?work
} AS %result
WHERE {
  INCLUDE %result
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,jp". }        
}  
ORDER BY DESC(?count)
"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    if results_df.empty:
        return(float('NaN'))
    else :
        result = sum(results_df["count.value"].astype(int))
        return(result)
        

def recursive_get_citations_by_qid(qid):
    try:
        citation_counts =  get_citations_by_qid(qid)
        return(citation_counts)
    except:
        recursive_get_citations_by_qid(qid)
    

def make_string_of_qids_for_sparql(array_of_qids):
    string_of_qids_for_sparql = ""
    for qid in array_of_qids:
        string_of_qids_for_sparql += "wd:" + str(qid) + " "
    return(string_of_qids_for_sparql)


def return_instances_of_specific_qid(array_of_qids, instances_of_qid) :
    
    time.sleep(5)

    string_of_qids = make_string_of_qids_for_sparql(array_of_qids)
    SPARQL_QUERY = """
    SELECT DISTINCT ?item ?itemLabel 
    WHERE {
    VALUES ?item """ + "{"+ string_of_qids +"}" + """
    ?item wdt:P31 wd:"""  +   instances_of_qid + "." +  """
   OPTIONAL {?item rdfs:label ?itemLabel. #Create a label (aka name) for the items in WikiData, without using the service query. 
    FILTER(LANG(?itemLabel) = "en").
    }
    }
"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(SPARQL_QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    
    results_df = results_df.replace(regex=r'http://www.wikidata.org/entity/(\.*)', value=r'\1')
    results_df = results_df[['item.value', 'itemLabel.value']]
    results_df.columns = ['QID', 'title']
    return(results_df)


def return_items_which_are_connected_to_items_from_a_subclass(array_of_qids, target_property, target_subclass) :
    string_of_qids = make_string_of_qids_for_sparql(array_of_qids)
    SPARQL_QUERY = """
    SELECT DISTINCT ?item ?itemLabel 
    WHERE {
    VALUES ?item """ + "{"+ string_of_qids +"}" + """
    ?item wdt:""" + target_property + " ?target_value. " + """
    ?target_value wdt:P279* """+ "wd:" +   target_subclass + "." +  """
    
        ?item wdt:P106 ?occupation.
    ?occupation wdt:P279* wd:Q1650915.
    
    OPTIONAL {?item rdfs:label ?itemLabel. #Create a label (aka name) for the items in WikiData, without using the service query. 
    FILTER(LANG(?itemLabel) = "en").
    }
    }
"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(SPARQL_QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    
    results_df = results_df.replace(regex=r'http://www.wikidata.org/entity/(\.*)', value=r'\1')
    results_df = results_df[['item.value', 'itemLabel.value']]
    results_df.columns = ['QID', 'title']
    return(results_df)

import requests




def get_number_of_edits(page_title) :

    BASE_URL = "http://en.wikipedia.org/w/api.php"
    TITLE = page_title

    parameters = { 'action': 'query',
           'format': 'json',
           'continue': '',
           'titles': TITLE,
           'prop': 'revisions',
           'rvprop': 'ids|userid',
           'rvlimit': 'max'}

    wp_call = requests.get(BASE_URL, params=parameters)
    response = wp_call.json()

    total_revisions = 0

    while True:
      wp_call = requests.get(BASE_URL, params=parameters)
      response = wp_call.json()

      for page_id in response['query']['pages']:
        total_revisions += len(response['query']['pages'][page_id]['revisions'])

      if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['rvcontinue'] = response['continue']['rvcontinue']

      else:
        break

    print(parameters['titles'])
    return(total_revisions)




def get_number_of_influential_citations_on_semantic_scholar(researcher_id):
    base_url = "http://api.semanticscholar.org/v1/author/"
    author = researcher_id
    api_call = requests.get(base_url + author)
    influential_citations = api_call.json()['influentialCitationCount']
    print(api_call.json()['aliases'])
    return(influential_citations)