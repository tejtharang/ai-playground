# In my own words

### Model Inference
Model Inference refers to the process of extracing insights from a trained model. 
1. We input new data into the model
2. The model makes predictions
3. Predictions can be numerical, images, text etc. 

### Langchain's Document Loader
Document loader is a mechanism to load documents into Langchain's ecosystem from various integrations - Slack, Google Drive etc.

### Vector Store

### Embedding
Embeddings are vector representations of Sentences and words. Representing these "tokens" as vectors lets us compute the similarity of the sentences using something like a cosine similarity
https://python.langchain.com/docs/concepts/embedding_models/#measure-similarity

### Retrieval Augmented Generation (RAG)

### Text Splitters
Text Splitting is used to break up large chunks of text into smaller bytes. There are several reasons for doing this. 
1. Models have input size limits
2. Splitting up text might help with keeping relavant information intact i.e. not diluting it.
3. Keeping input document lengths uniform
