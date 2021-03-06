# Data Science Project - CS 839
## Team Members
* Sri Harshal Parimi (sparimi@wisc.edu)
* Shebin Roy Yesudhas (royyesudhas@wisc.edu)
* Sankarshan Umesh Bhat (sbhat6@wisc.edu)
 
### Stage-1: Information Extraction from natural text
* [Set B](https://github.com/harshal95/CS839/tree/master/stage_1/set-B)
  * [README](https://github.com/harshal95/CS839/tree/master/stage_1/set-B/README.md)
* [Set I](https://github.com/harshal95/CS839/tree/master/stage_1/set-I)
* [Set J](https://github.com/harshal95/CS839/tree/master/stage_1/set-J)
* [Source code](https://github.com/harshal95/CS839/tree/master/stage_1/code)
* [Compressed file](https://github.com/harshal95/CS839/tree/master/stage_1/compressed_file.zip)
* [Stage 1 Report](https://github.com/harshal95/CS839/tree/master/stage_1/Stage1-Report.pdf)

### Stage-2: Crawling and Extracting Structured data from web-pages
* [Data](https://github.com/harshal95/CS839/tree/master/stage_2/data)
* [Source code](https://github.com/harshal95/CS839/tree/master/stage_2/code/cs839)
* [Report](https://github.com/harshal95/CS839/blob/master/stage_2/Stage%202%20-%20Report.pdf)

### Stage-3: Entity-matching
#### Matching Fodors and Zagats
* UserId: Avengers
* ProjectId: endgame
* [Screenshot](https://github.com/harshal95/CS839/blob/master/Sample_Data_set_Cloud_Matcher_output.png)

#### Blocking Results
* UserId: Avengers
* ProjectId: MoviesMatcher
* [Screenshot](https://github.com/harshal95/CS839/blob/master/Learned_Blocking_Rules.png)

#### Matching Results
* UserId: Avengers
* ProjectId: MoviesMatcher
* [Screenshot](https://github.com/harshal95/CS839/blob/master/match_results_all_ds_839.JPG)

#### Estimating accuracy
* [Candidate set](https://github.com/harshal95/CS839/blob/master/stage_3/data/downloaded_data/candidate_set) - 72165 tuple pairs
* [Prediction list](https://github.com/harshal95/CS839/blob/master/stage_3/data/downloaded_data/prediction_list)
* [Table A](https://github.com/harshal95/CS839/blob/master/stage_3/data/downloaded_data/imdb)
* [Table B](https://github.com/harshal95/CS839/blob/master/stage_3/data/downloaded_data/rotton_tom)

* Candidate set size is 72165 which is greater than 500
 * [Report for blocking rules](https://github.com/harshal95/CS839/blob/master/stage_3/data/Stage%203-%20Blocking%20rules%20and%20estimating%20precision%2C%20recall.pdf)
 * [Code for blocking rules](https://github.com/harshal95/CS839/blob/master/stage_3/code/blocking_rules.ipynb)
 * [Reduced candidate set](https://github.com/harshal95/CS839/blob/master/stage_3/data/downloaded_data/cand_set_after_blocking)
* [Labeled Tuple pairs](https://github.com/harshal95/CS839/blob/master/stage_3/data/downloaded_data/labeled_pairs.csv)
* Recall = \[0.9371096866388409 - 0.9910340259360095\]
* Precision = \[0.9186143717366582 - 0.9782780006778256\]
