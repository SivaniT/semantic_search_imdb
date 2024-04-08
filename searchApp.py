import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
#using the same index created in semantic.ipynb file
indexName = "all_m10s"
#checking for connection
try:
    es= Elasticsearch("https://localhost:9200",
                  basic_auth=('elastic', 'UXjHr=I*dSOPFsfM3rIJ'),
                  verify_certs=False)

except ConnectionError as e:
    print("Connection Error:", e)
#throwing an exception to  check if there is a network issue or not
if es.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")



# function for search
def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)
    #querying the data from ES 
    query = {
        "field": "Embedded_vectors",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 998,
    }
    # using knn to return the results from the elastic search db and all the columns of the documents related to it
    res = es.knn_search(index="all_m10s"
                        , knn=query 
                        , source=["Series_Title","Overview","Cast","Genre","Released_Year","IMDB_Rating","Runtime"]
                        )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search IMDB Top 1000 movies")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = search(search_query)

            # Display search results and the related information
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['Series_Title']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Overview: {result['_source']['Overview']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Cast: {result['_source']['Cast']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Genre: {result['_source']['Genre']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Released Year: {result['_source']['Released_Year']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"IMBD Rating: {result['_source']['IMDB_Rating']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Runtime: {result['_source']['Runtime']}")
                        except Exception as e:
                            print(e)
                        st.divider()

                    
if __name__ == "__main__":
    main()
