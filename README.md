# Amazon-AWS-Textract-Checkbox-Selection-Detection
The Purpose of this Repo is to make people fimiliarize with Amazon Text Detect Checbox selection feature. I had a hard time figuring this one out as this is based on json key value pairs, I hope my effort will save others time. 

For more information refer to this link: https://docs.aws.amazon.com/textract/latest/dg/how-it-works-selectables.html

![image](https://user-images.githubusercontent.com/120024887/218654571-d054ce09-14f4-4e79-8fb3-1e06c77a569a.png)


For Hint This is the working which is in order to extract text along with checkbox 

```
Get TEXT TYPE Selected 
It will be child of X Element, 
Get ID of Child Element
It will have other Child elements linked with it
FIND Block TYPE of LINE in which one of child found above is present. 

``` 
