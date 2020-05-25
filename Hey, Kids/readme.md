## Data Analysis and Machine Learning

This folder contains both the datasets and my solution code for the data analysis track from Northsec 2020.  

### Challenge 1

This scenario started with a 2GB database of students, with a note on the challenge text saying "it's about corruption in the school system", a note about finding a girl named Liz, and a question asking which one is severity high. From here we decided we either needed the most corrupt student or the most corrupt school.   

The first step was a basic examination of the data, which I did with the jupyter notebook citizen_database.py which can be used to follow along (if you want the dataset I'll put it on google drive, it's too large for github). After reading the csv, I called df.head() to get a printout of the first 5 lines. These showed each student had the following fields:  
```name 	last_name 	coord_x 	coord_y 	group 	docile 	voice_pitch 	facial_ratio 	retina_r 	retina_g 	retina_b 	humidity_index 	parent_worth 	social_index 	consumer_score 	citizen_quality_score 	prob_failure 	z_index 	school_id 	student_id 	genre_id 	grad_year 	parent_donations_k 	final_grade```  

From here we can see that there are both donations and grade fields. The next obvious thing to do is check if they're related, so we use df.corr() to see correlation between the values - it turns out there is a very low correlation. I reran the command after grouping the students by high school

```aggregated = df.groupby('school_id')[['parent_donations_k', 'final_grade']].corr().iloc[0::2][['final_grade']] ```  

After this the correlation was much more obviou - one school had a correlation of 0.8, the others hovered around 0.5. Within that school was a single student named elizebeth. The student id wasn't accepted as a flag, but the school id was, and granted the first point in this track.

### Challenge 2

The next download was a collection of students from severity high, with all the same fields except for "docile". The challenge was to identify the 3 "known agitators" in this dataset.  The obvious solution was to run a machine learning algorithm on the labelled dataset from challenge 1 to predict the labels on challenge 2. This is in the file  "sev_high_agitators.py" - jupyter notebooks are fine for basic exploration, but are not the best tool for running ML stuff. Instead I used spyder, which has similar (optional) cell based execution along with the full IDE and variable explorer.  

My first iteration used an SGD classifier to generate the labels. It identified 9 "agitators" - one was accepted as a flag, the others gave the message "refine your model for more flags".  
```3990	691aa1d3-09de-4d86-8fed-51710b2cc479```

On my second attempt, I re examined the correlation output from the dataset, and selected only the features with the highest correlation - retina_r, citizen_quality, voice_pitch and z_index. This refinement allowed me to get one more flag out of this.  

```5241	278e7b64-0347-4e7e-b7e2-6b47fef8cf97```

At this point I jumped off the deep end, and accepted that most of my weekend was going to be spent on this challenge. After some extensive trial and error, I ended up implementing a rudimentary automatic feature extractor. This is based on randomly choosing a set of features to use, randomly splitting the dataset into train/test subsets, testing and evaluating each feature set a number of times to get it's accuracy. Then the most accurate set of features was used as an input into the final model. While this was not particularly robust, it was sufficient to pass through the challenge and get the final flag. As a bonus point, the top 3 students identified by the model were the correct answers for the flags, making the challenge feel much more reasonable.  
```3728	f6622b3c-33aa-4b42-bbe7-d44cafb8b1ae```

Had this failed, the next step would have been trying polynomial combinations - I omitted it for time, but it would almost certainly increase the accuracy of the model.
###Challenge 3

The next download was an APK, with the storyline that it was a tracking app that had been defaced by hackers. My first step was running strings on it. As it turns out, there are an unbelieveable amount of strings in an android app, and it gave me 12000 hits. Some more research turned up that android apps contain a "string table", with the user defined strings in it. 

```aapt d --values strings [APK_FILE]``` 

This only had 2000 strings. This table contained a flag, but it was worth 0 points and just said "you didn't think it would be that easy". It also contained a bunch of base64 strings that decoded to questions and answers. I ran the APK using genymotion, and it popped up a series of questions - by using the encoded answers I was able to get through them at it gave me another flag.
Lastly, looking at the cert.rsa file within hte APK gives the publihser as Trolling1.0, and the rot13 flag yetz-01wx46912476x304v5y1yu71uy87285u0

### Challenge 4.

The next dataset download was a file snitches_log and a password protected zip. I had no good ideas, so asked the team for help. We ended up setting john the ripper to run on it but never got a password... it turned out to be severityhigh123. There's a lesson here about not using default dictionaries.

Once opened, it was a sqlite table. One was named secret and had a flag, the other was a list of where students were when connected to wifi. I'm assuming that by looking at the agitators in challenge 2, and then correlating locations from the wifi logs, you can pull out a mega snitch who is responsible for getting them in trouble. I'll get around to trying this eventually...
