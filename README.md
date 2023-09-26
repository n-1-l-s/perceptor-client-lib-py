# perceptor-client-lib-py

## Installing package

to be described here


## Usage

Create the client first:

```python
import perceptor_client_lib.perceptor as perceptor

API_KEY = "your_api_key"

perceptor_client = perceptor.Client(api_key=API_KEY)

```

optionally, another url can be specified:
```python
perceptor_client = perceptor.Client(api_key="your_key",request_url="another_url")
```

### Sending instructions for text

```python
result = perceptor_client.ask_text("text_to_process",
                                       instructions=[
                                           "Question 1?",
                                           "Question 2",
                                       ])

```

### Sending instructions for an image

Following image formats are supported: "_jpg_", "_png_".

From image file:
```python
result = perceptor_client.ask_image("path_to_image_file",
                                       instructions=[
                                           "Question 1?",
                                           "Question 2",
                                       ])

```

or from image file:
```python

reader = open("image_path", 'rb')
with reader:
    result = perceptor_client.ask_image(reader,
                                       instructions=[
                                           "Question 1?",
                                           "Question 2",
                                       ], file_type='jpg')
```

or from bytes:
```python

reader = open(_image_path, 'rb')
with reader:
    content_bytes = reader.read()
    result = perceptor_client.ask_image(content_bytes,
                                       instructions=[
                                           "Question 1?",
                                           "Question 2",
                                       ], file_type='jpg')
```

Table queries can be performed as following:
```python

result = perceptor_client.ask_table_from_image("path_to_image_file",
                                       instruction="GENERATE TABLE Column1, Column2, Column3 GUIDED BY Column3",
                                               )
```

### Sending instructions for a pdf document
From document file:
```python
result = perceptor_client.ask_document("path_to_document_file",
                                       instructions=[
                                           "Question 1?",
                                           "Question 2",
                                       ])

```

