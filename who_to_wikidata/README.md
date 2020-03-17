# Who to Wikidata

The goal of this project is to enable automatic conversion of Who reports about the COVID-19 situation to Quickstatements compatible referenced batches. 

* The '''scraping_who_table_to_pandas''' script makes a table of cases out of a WHO report.
* The '''generating_dict_of_countries_to_outbreaks''' script makes a table of matched country names and outbreak items.
* The '''generating_dict_of_countries_to_outbreaks''' script makes a table of matched country names and outbreak items.

The '''matching_who_table_to_wikidata'''

## Structure of the Quickstatements V1 Command generated 

For each row in the who_table_with_qids.csv table:

    print(
    outbreak_qid +'|P1120|' + total_deaths + "|S585|" + who_report_date + "|S248|" + who_report_qid +  '\n' +
    outbreak_qid +'|P1603|' + total_cases + "|S585|" + who_report_date + "|S248|" + who_report_qid +  '\n' )

## How to contribute 

Do you want to contribute? Great!

Raise an issue about the topic you want to improve and feel free to make pull requests at any time.
